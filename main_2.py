"""The streamlit app"""
import streamlit as st

import pandas as pd
import altair as alt
import numpy as np

from charts.accuracy import accuracy_compare_chart
from charts.chart_theme import streamlit_theme
from charts.kills import kills_compare_chart

from datafetch.data_processer import (
    best_map,
    load_bo4_data_short,
    load_cw_data,
    load_mw_data_short,
    map_img_url,
    map_stats,
    mode_img_url,
    mode_stats,
)

from resources.user_download import get_table_download_link

from static.css.custom_theme import (
    block_format,
    bootstrap_css,
    page_format,
    sidebar_format,
    hero,
)

from static.html.custom_html import (
    assign_id,
    central_col_size_adjust,
    custom_table,
    data_widget_master_css,
    data_widget_1_col,
    data_widget_2_col,
    data_widget_3_col,
    data_widget_5_col,
    format_para_size,
    grid_test,  ##########
    set_background_image_fill_overlay,
    st_info_custom,
)

# Uses the full page instead of narrow central column and configures page info
st.set_page_config(
    layout="wide",
    page_title="CoD: Stat Tracker",
    page_icon="https://s3.us-west-2.amazonaws.com/secure.notion-static.com/40fd8e49-bf55-4954-81d3-09a5e732ec61"
              "/240x240_icon.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAT73L2G45O3KS52Y5%2F20201130"
              "%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20201130T144907Z&X-Amz-Expires=86400&X-Amz-Signature"
              "=9f5658353e68555e3efa0da1f31542c0bbea42410b5a3d9eb07abc9313ff5736&X-Amz-SignedHeaders=host&response"
              "-content-disposition=filename%20%3D%22240x240_icon.jpg%22",
    initial_sidebar_state="expanded"
)

# Set the central column width
st.markdown(central_col_size_adjust("main", 55), unsafe_allow_html=True)
# Load CSS #
st.markdown(bootstrap_css(), unsafe_allow_html=True)  # Load Bootstrap
st.markdown(sidebar_format(), unsafe_allow_html=True)  # Format sidebar
st.markdown(page_format(), unsafe_allow_html=True)  # Format page
st.markdown(block_format(), unsafe_allow_html=True)  # Format StBlock elements
st.markdown(data_widget_master_css(), unsafe_allow_html=True)  # Format data widgets

# Initialise the sidebar and gets the user's options
with st.sidebar:
    playername = st.text_input("Enter your platform username here", "Cording Xx")
    platform = st.radio("Pick a platform", ["Xbox", "Playstation"])
    ekia_or_kia = st.radio("Use EKIA or Kills?", ["EKIA", "Kills"])
    comp_text = "Compare with previous games:"

    # Reduces spacing between check boxes to closer match spacing of radio buttons
    st.markdown("<style>.Widget.row-widget.stCheckbox{margin-bottom: -15px;}", unsafe_allow_html=True)

    # Adds the prompt text for game comparison and formats it similary to radio text
    st.markdown(format_para_size(0.8, comp_text), unsafe_allow_html=True)

    comp_bo4 = st.checkbox("Black Ops 4")
    comp_mw = st.checkbox("Modern Warfare")

    st.header("")
    comp_text = "View all raw data?"
    st.markdown(format_para_size(0.8, comp_text), unsafe_allow_html=True)
    show_data = st.checkbox("Show data")

# Converts platform to required string for API call
if platform == "Xbox":
    platform_picked = "xbl"
else:
    platform_picked = "psn"

# Passes relevant values for EKIA/KIA
if ekia_or_kia == "EKIA":
    kills_type = "ekia"
    kd_ratio = "ekiadratio"
    kd_type_str = "EKIA ratio"
elif ekia_or_kia == "Kills":
    kills_type = "kills"
    kd_ratio = "kd"
    kd_type_str = "KD ratio"


def main():
    try:
        with st.spinner("Loading Cold War player data. \n\n**Please note**:  this may take a while the first time "
                        "you load the data."):
            player_data = load_cw_data(playername, platform_picked)
            if player_data.empty:
                st.stop()
    except:
        st.error("Unable to generate Cold War player data. Please check you typed the name correctly and selected the "
                 "right platform before trying again.")
        st.stop()

    if playername == "":
        st.error("Please enter your username/gamertag")
        st.stop()
    else:
        dataframes = {"CW": pd.DataFrame(player_data)}
        player_data_bo4 = pd.DataFrame()
        player_data_mw = pd.DataFrame()

        if comp_bo4:
            n_rows_to_load = len(player_data.index)
            player_data_bo4 = load_bo4_data_short(playername, platform_picked, n_rows_to_load)
            dataframes["BO4"] = pd.DataFrame(player_data_bo4)
            if player_data_bo4.empty:
                st.error(
                    f"Could not find any previous Black Ops 4 data. Data can only be loaded if you played Black Ops 4"
                    f" on {platform} using the gamertag {playername}.")

        if comp_mw:
            n_rows_to_load = len(player_data.index)
            player_data_mw = load_mw_data_short(playername, platform_picked, n_rows_to_load)
            dataframes["MW"] = pd.DataFrame(player_data_mw)
            if player_data_mw.empty:
                st.error(
                    f"Could not find any previous Modern Warfare data. Data can only be loaded if you played Modern "
                    f"Warfare on {platform} using the gamertag {playername}.")

        # Generate final dataframe with all options included
        all_data_frame = pd.concat(dataframes)

        # Page hero
        st.markdown(hero(playername, platform), unsafe_allow_html=True)

        # Check if comparing data to draw a select box if so
        if comp_mw or comp_bo4:
            games_picked = all_data_frame["Game"].unique()
            games_to_compare = st.selectbox("Game summary data", games_picked)
        else:
            games_to_compare = "Cold War"

        # Temporarily create new vars for kills_type and kd_ratio as
        # Modern Warfare doesn't have EKIA/EKIADR data. Forces us to
        # use kills/kd ratio even if EKIA is picked for MW
        if games_to_compare == "Modern Warfare":
            if ekia_or_kia == "EKIA":
                st.info("***Please note:*** EKIA/EKIA Ratio data is not available for Modern Warfare. "
                        "\n\nShowing kills and KD ratio instead.")
                kills_type_2 = "kills"
                kd_ratio_2 = "kd"
            else:
                kills_type_2 = kills_type
                kd_ratio_2 = kd_ratio
        else:
            kills_type_2 = kills_type
            kd_ratio_2 = kd_ratio

        # # Define two columns
        # col1, col2 = st.beta_columns(2)
        # data_comp_df = all_data_frame.loc[(all_data_frame.Game == games_to_compare)]
        #
        # with col1:
        #     # Load data from functions
        #     map_table_top3 = map_stats(data_comp_df, kills_type_2, kd_ratio_2, 3)
        #     best_map_name = best_map(map_table_top3, kd_ratio_2)
        #     best_map_image = map_img_url(data_comp_df, best_map_name)
        #
        #     st.markdown(grid_test(best_map_name, "Column 2", "Column 3"), unsafe_allow_html=True)
        #
        #     st.subheader("Map summary")
        #     # Assigns unique ID to the div so we can style it
        #     st.markdown(assign_id("col_1_map_summary"), unsafe_allow_html=True)
        #
        #     # Styles the above named Div with given BG image
        #     st.markdown(set_background_image_fill_overlay("col_1_map_summary", best_map_image), unsafe_allow_html=True)
        #
        #     # Declare variables to pass to custom HTML table
        #     h1 = "Map"
        #     h2 = "Kills"
        #     h3 = kd_type_str
        #
        #     map1 = map_table_top3.loc[0, "map_name"]
        #     map2 = map_table_top3.loc[1, "map_name"]
        #     map3 = map_table_top3.loc[2, "map_name"]
        #     map1k = "%0.0f" % map_table_top3.loc[0, kills_type_2]
        #     map2k = "%0.0f" % map_table_top3.loc[1, kills_type_2]
        #     map3k = "%0.0f" % map_table_top3.loc[2, kills_type_2]
        #     map1kd = "%0.2f" % map_table_top3.loc[0, kd_ratio_2]
        #     map2kd = "%0.2f" % map_table_top3.loc[1, kd_ratio_2]
        #     map3kd = "%0.2f" % map_table_top3.loc[2, kd_ratio_2]
        #
        #     # Draws the custom table
        #     st.markdown(custom_table(
        #         h1=h1, h2=h2, h3=h3,
        #         map1=map1, map2=map2, map3=map3,
        #         map1k=map1k, map2k=map2k, map3k=map3k,
        #         map1kd=map1kd, map2kd=map2kd, map3kd=map3kd
        #     ), unsafe_allow_html=True)
        #
        # with col2:
        #     # Load data from functions
        #     mode_table_top3 = mode_stats(data_comp_df, kills_type_2, kd_ratio_2, 3)
        #     best_mode_image = mode_img_url()
        #
        #     st.subheader("Mode summary")
        #     st.markdown(assign_id("col_2_mode_summary"), unsafe_allow_html=True)
        #     st.markdown(set_background_image_fill_overlay("col_2_mode_summary", best_mode_image),
        #                 unsafe_allow_html=True)
        #
        #     # Declare variables to pass to custom HTML table
        #     h1 = "Mode"
        #     h2 = "Kills"
        #     h3 = kd_type_str
        #
        #     mode1 = mode_table_top3.loc[0, "mode"]
        #     mode2 = mode_table_top3.loc[1, "mode"]
        #     mode3 = mode_table_top3.loc[2, "mode"]
        #     mode1k = "%0.0f" % mode_table_top3.loc[0, kills_type_2]
        #     mode2k = "%0.0f" % mode_table_top3.loc[1, kills_type_2]
        #     mode3k = "%0.0f" % mode_table_top3.loc[2, kills_type_2]
        #     mode1kd = "%0.2f" % mode_table_top3.loc[0, kd_ratio_2]
        #     mode2kd = "%0.2f" % mode_table_top3.loc[1, kd_ratio_2]
        #     mode3kd = "%0.2f" % mode_table_top3.loc[2, kd_ratio_2]
        #
        #     # Draws the custom table
        #     st.markdown(custom_table(
        #         h1=h1, h2=h2, h3=h3,
        #         map1=mode1, map2=mode2, map3=mode3,
        #         map1k=mode1k, map2k=mode2k, map3k=mode3k,
        #         map1kd=mode1kd, map2kd=mode2kd, map3kd=mode3kd
        #     ), unsafe_allow_html=True)

        # Begin main content
        # st.markdown("---")
        # st.title("Player statistics")

        # Map and mode filters
        filter_container = st.beta_container()

        with filter_container:
            st.markdown("<h4>Player statistics</h4>", unsafe_allow_html=True)
            filter_expander = st.beta_expander("Filter data", expanded=False)
            with filter_expander:
                # Lists all the maps
                map_names_unique = all_data_frame["map_name"].unique()
                map_filter = st.multiselect("Map", sorted(map_names_unique))

                # Configures dataframe with or without map filter
                if not map_filter:
                    map_df = all_data_frame
                    map_df.loc[:, "match_number"] = np.arange(1, len(map_df) + 1)
                else:
                    map_df = all_data_frame[all_data_frame["map_name"].isin(map_filter)]
                    map_df.loc[:, "match_number"] = np.arange(1, len(map_df) + 1)

                # Configures game modes available based on map selected
                game_modes_unique = map_df["mode"].unique()
                mode_filter = st.multiselect("Game mode", sorted(game_modes_unique))

                # Configures dataframe with or without the mode filter
                if not mode_filter:
                    filtered_df = map_df
                    filtered_df.loc[:, "match_number"] = np.arange(1, len(filtered_df) + 1)
                else:
                    filtered_df = map_df[map_df["mode"].isin(mode_filter)]
                    filtered_df.loc[:, "match_number"] = np.arange(1, len(filtered_df) + 1)

                # Added the slider into a 99% width column
                # without the column, the end of the slider clips inside the dropdown
                col1_slider, col_empty = st.beta_columns((0.9999, 0.0001))
                with col1_slider:
                    # Adds the slider using maximum number of Cold War matches for comparison purposes
                    count_col = len(filtered_df[filtered_df["Game"] == "Cold War"])
                    if count_col == 0:
                        slider_max_val_int = 1
                    else:
                        slider_max_val_int = int(count_col)

                    recent_matches = st.slider("Show the most recent matches:",
                                               min_value=0,
                                               max_value=slider_max_val_int,
                                               value=slider_max_val_int)

                dataframes_2 = {}

                try:
                    update_match_numbers_mw = filtered_df[filtered_df["Game"] == "Modern Warfare"]
                    update_match_numbers_mw.loc[:, "match_number"] = np.arange(1, len(update_match_numbers_mw) + 1)
                    dataframes_2["MW2"] = pd.DataFrame(update_match_numbers_mw.head(recent_matches))
                except:
                    update_match_numbers_mw = pd.DataFrame()

                try:
                    update_match_numbers_bo4 = filtered_df[filtered_df["Game"] == "Black Ops 4"]
                    update_match_numbers_bo4.loc[:, "match_number"] = np.arange(1, len(update_match_numbers_bo4) + 1)
                    dataframes_2["BO42"] = pd.DataFrame(update_match_numbers_bo4.head(recent_matches))
                except:
                    dataframes_2["BO4"] = pd.DataFrame()

                try:
                    update_match_numbers_cw = filtered_df[filtered_df["Game"] == "Cold War"]
                    update_match_numbers_cw.loc[:, "match_number"] = np.arange(1, len(update_match_numbers_cw) + 1)
                    dataframes_2["CW2"] = pd.DataFrame(update_match_numbers_cw.head(recent_matches))
                except:
                    dataframes_2["CW"] = pd.DataFrame()

                remerge = pd.concat(dataframes_2)

                # Our final DF with all data after filtering etc.
                final_data_frame = remerge

                # Splitting the DF into the respective games for use in charts/tables etc.
                final_data_frame_cw = final_data_frame[final_data_frame["Game"] == "Cold War"]
                final_data_frame_mw = final_data_frame[final_data_frame["Game"] == "Modern Warfare"]
                final_data_frame_bo4 = final_data_frame[final_data_frame["Game"] == "Black Ops 4"]

            total_kills = final_data_frame["kills"].sum()
            total_deaths = final_data_frame["deaths"].sum()
            calculated_kd = total_kills / total_deaths
            average_kd = final_data_frame[kd_ratio_2].mean()
            average_accuracy = final_data_frame["accuracy"].mean()

            st.markdown(data_widget_5_col("Total kills", f"{total_kills:,.0f}",
                                          "Total deaths", f"{total_deaths:,.0f}",
                                          f"Overall {kd_type_str}", f"{calculated_kd:0.2f}",
                                          f"Average {kd_type_str}", f"{average_kd:0.2f}",
                                          "Average accuracy", f"{average_accuracy:0.1f}%"), unsafe_allow_html=True)

        # Imports and applies Altair theme from chart_theme.py
        # This will apply to all charts on the page
        alt.themes.register("streamlit", streamlit_theme)
        alt.themes.enable("streamlit")

        # # Defines columns
        # kills_col_1, kills_col_2 = st.beta_columns(2)
        #
        # # Decides what to display depending on if comparison data is enabled
        # if comp_mw or comp_bo4:
        #     with kills_col_1:
        #         game_kd_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", kd_ratio].mean()
        #         st.write(f"Average {kd_type_str} in Cold War is **{game_kd_cw:0.2f}**")
        #
        #     with kills_col_2:
        #         game_kd_bo4 = filtered_df.loc[filtered_df["Game"] == "Black Ops 4", kd_ratio].mean()
        #         st.write(f"Average {kd_type_str} in Black Ops 4 is **{game_kd_bo4:0.2f}**")
        # else:
        #     game_kd_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", kd_ratio].mean()
        #     st.write(f"Average {kd_type_str} in Cold War is **{game_kd_cw:0.2f}**")

        # ==== Kills component ==== #
        container_kills = st.beta_container()
        with container_kills:
            st.markdown("<h4>Player kills</h4>", unsafe_allow_html=True)

            get_chart = kills_compare_chart(
                comp_mw, comp_bo4,
                final_data_frame,
                kills_type_2, kd_ratio_2
            )

            kd_average = final_data_frame[kd_ratio_2].mean()
            kd_max = final_data_frame[kd_ratio_2].max()

            acc_col1, acc_col2 = st.beta_columns((0.25, 0.75))
            with acc_col1:
                rounded_kd = "%0.2f" % kd_average
                rounded_kd_best = "%0.2f" % kd_max
                st.markdown(data_widget_1_col(f"Average {kd_type_str}", rounded_kd,
                                              f"Highest {kd_type_str}", rounded_kd_best),
                            unsafe_allow_html=True)

            with acc_col2:
                st.altair_chart(get_chart, use_container_width=True)

        # ==== Accuracy component ==== #
        container = st.beta_container()
        with container:
            st.markdown("<h4>Player accuracy</h4>", unsafe_allow_html=True)

            # Pass data and variables to chart function
            get_chart = accuracy_compare_chart(
                comp_mw, comp_bo4,
                final_data_frame,
                kills_type_2, kd_ratio_2
            )

            # Get accuracy avg and max for Cold War
            accuracy_average = final_data_frame_cw["accuracy"].mean()
            accuracy_max = final_data_frame_cw["accuracy"].max()

            acc_col1, acc_col2 = st.beta_columns((0.75, 0.25))
            with acc_col1:
                st.altair_chart(get_chart, use_container_width=True)

            with acc_col2:
                # Check for comparison
                if comp_mw or comp_bo4:
                    # If comparing both games
                    if comp_mw and comp_bo4:
                        accuracy_average_mw = final_data_frame_mw["accuracy"].mean()
                        accuracy_max_mw = final_data_frame_mw["accuracy"].max()

                        accuracy_average_bo4 = final_data_frame_bo4["accuracy"].mean()
                        accuracy_max_bo4 = final_data_frame_bo4["accuracy"].max()

                        st.markdown(data_widget_3_col("Cold War", "Black Ops 4", "Modern Warfare",
                                                      f"{accuracy_average:0.1f}%",
                                                      f"{accuracy_average_bo4:0.1f}%",
                                                      f"{accuracy_average_mw:0.1f}%",
                                                      f"{accuracy_max:0.1f}%",
                                                      f"{accuracy_max_bo4:0.1f}%",
                                                      f"{accuracy_max_mw:0.1f}%",
                                                      ), unsafe_allow_html=True)
                    # If only comparing one game, isolate which one
                    else:
                        if comp_mw:
                            accuracy_average_comp = final_data_frame_mw["accuracy"].mean()
                            accuracy_max_comp = final_data_frame_mw["accuracy"].max()
                            comparison_game = "Modern Warfare"
                        else:
                            accuracy_average_comp = final_data_frame_bo4["accuracy"].mean()
                            accuracy_max_comp = final_data_frame_bo4["accuracy"].max()
                            comparison_game = "Black Ops 4"

                        st.markdown(data_widget_2_col("Cold War", comparison_game,
                                                      f"{accuracy_average:0.1f}%",
                                                      f"{accuracy_average_comp:0.1f}%",
                                                      f"{accuracy_max:0.1f}%",
                                                      f"{accuracy_max_comp:0.1f}%"
                                                      ), unsafe_allow_html=True)
                # Comparing neither game
                elif not comp_mw or comp_bo4:
                    st.markdown(data_widget_1_col("Average accuracy", f"{accuracy_average:0.1f}%",
                                                  "Highest accuracy", f"{accuracy_max:0.1f}%"),
                                unsafe_allow_html=True)

        # ==== Raw data component ==== #
        if show_data:
            container_data = st.beta_container()
            with container_data:
                st.markdown("<h4>Raw data</h4>", unsafe_allow_html=True)
                st.write(final_data_frame)
                st.markdown(get_table_download_link(final_data_frame), unsafe_allow_html=True)

        # Sidebar footer
        with st.sidebar:
            st.header("")
            st.subheader("Data note:")
            st.write(
                "Data provided in this app is on a 30 minute lag and hence may not be "
                "the most up-to-date."
            )

            st.header("")
            st.markdown(st_info_custom("maintains this app.", "Jon Cording", "https://www.linkedin.com/in/jon-cording"),
                        unsafe_allow_html=True)


main()
