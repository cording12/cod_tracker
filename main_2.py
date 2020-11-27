from user_download import get_table_download_link
from resources.chart_theme import streamlit_theme
from resources.custom_html import assign_id
from resources.custom_html import set_background_image_fill_overlay
from resources.custom_html import custom_table
from resources.data_processer import load_cw_data
from resources.data_processer import load_bo4_data
from resources.data_processer import load_bo4_data_short
from resources.data_processer import load_mw_data
from resources.data_processer import load_mw_data_short
from resources.data_processer import map_stats
from resources.data_processer import map_img_url
from resources.data_processer import best_map
from resources.data_processer import mode_stats
from resources.data_processer import mode_img_url
import pandas as pd
import altair as alt
import numpy as np
import streamlit as st

# Initialise the sidebar and gets the user's options
with st.sidebar:
    playername = st.text_input("Enter your platform username here", "Cording Xx")
    platform = st.radio("Pick a platform", ["Xbox", "Playstation"])
    ekia_or_kia = st.radio("Use EKIA or Kills?", ["EKIA", "Kills"])
    compare_data = st.radio("Compare with previous CoD data?", ["Yes", "No"], 1)

    st.write("Compare with previous Call of Duty games")
    games = ["Black Ops 4", "Modern Warfare"]
    comp_bo4 = st.checkbox("Black Ops 4")
    comp_mw = st.checkbox("Modern Warfare")
    st.markdown("---")

# Converts platform to required string for API call
if platform == "Xbox":
    platform_picked = "xbl"
else:
    platform_picked = "psn"

# Passes relevant values for EKIA/KIA to charts
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
            else:
                all_data_frame = player_data
                key_cw = "CW"
            error_collector = 0
    except:
        st.error("Unable to generate Cold War player data. Please check you typed the name correctly and selected the "
                 "right platform before trying again.")
        error_collector = 1
        st.stop()

    # Checks there is a username entered before continuing
    if playername == "":
        st.error("Please enter your username/gamertag")
        st.stop()
    elif error_collector == 1:
        st.error("Unable to generate Cold War player data. Please check you typed the name correctly and selected the "
                 "right platform before trying again.")
        st.stop()
    else:
        dataframes = {"CW": pd.DataFrame(player_data)}
        player_data_bo4 = pd.DataFrame()

        if comp_bo4:
            # player_data_bo4 = load_bo4_data(playername, platform_picked)
            n_rows_to_load = len(player_data.index)
            player_data_bo4 = load_bo4_data_short(playername, platform_picked, n_rows_to_load)
            dataframes["BO4"] = pd.DataFrame(player_data_bo4)
            if player_data_bo4.empty:
                st.error(
                    f"Could not find any previous Black Ops 4 data. Data can only be loaded if you played Black Ops 4"
                    f" on {platform} using the gamertag {playername}.")

        if comp_mw:
            # player_data_mw = load_mw_data(playername, platform_picked)
            n_rows_to_load = len(player_data.index)
            player_data_mw = load_mw_data_short(playername, platform_picked, n_rows_to_load)
            dataframes["MW"] = pd.DataFrame(player_data_mw)
            if player_data_mw.empty:
                st.error(
                    f"Could not find any previous Modern Warfare data. Data can only be loaded if you played Modern "
                    f"Warfare on {platform} using the gamertag {playername}.")

        # Generate final dataframe with all options included
        all_data_frame = pd.concat(dataframes)

        # Begins writing to the main page
        with st.sidebar:
            # Add option to show data
            show_data = st.checkbox("Show raw data")

        # Page title and text
        st.title("Call of Duty: Cold War")
        st.write(f"Showing player data for {playername} on {platform}.")

        # Define two columns
        col1, col2 = st.beta_columns(2)

        with col1:
            # Load data from functions
            map_table_top3 = map_stats(player_data, kills_type, kd_ratio, 3)
            best_map_name = best_map(player_data, kd_ratio)
            best_map_image = map_img_url(player_data, best_map_name)

            st.subheader("Map summary")
            # Assigns unique ID to the div so we can style it
            st.markdown(assign_id("col_1_map_summary"), unsafe_allow_html=True)

            # Styles the above named Div with given BG image
            st.markdown(set_background_image_fill_overlay("col_1_map_summary", best_map_image), unsafe_allow_html=True)

            # Declare variables to pass to custom HTML table
            h1 = "Map"
            h2 = "Kills"
            h3 = kd_type_str

            map1 = map_table_top3.loc[0, "map_name"]
            map2 = map_table_top3.loc[1, "map_name"]
            map3 = map_table_top3.loc[2, "map_name"]
            map1k = "%0.0f" % map_table_top3.loc[0, kills_type]
            map2k = "%0.0f" % map_table_top3.loc[1, kills_type]
            map3k = "%0.0f" % map_table_top3.loc[2, kills_type]
            map1kd = "%0.2f" % map_table_top3.loc[0, kd_ratio]
            map2kd = "%0.2f" % map_table_top3.loc[1, kd_ratio]
            map3kd = "%0.2f" % map_table_top3.loc[2, kd_ratio]

            # Draws the custom table
            st.markdown(custom_table(
                h1=h1, h2=h2, h3=h3,
                map1=map1, map2=map2, map3=map3,
                map1k=map1k, map2k=map2k, map3k=map3k,
                map1kd=map1kd, map2kd=map2kd, map3kd=map3kd
            ), unsafe_allow_html=True)

        with col2:
            # Load data from functions
            mode_table_top3 = mode_stats(player_data, kills_type, kd_ratio, 3)
            best_mode_image = mode_img_url()

            st.subheader("Mode summary")
            st.markdown(assign_id("col_2_mode_summary"), unsafe_allow_html=True)
            st.markdown(set_background_image_fill_overlay("col_2_mode_summary", best_mode_image), unsafe_allow_html=True)

            # Declare variables to pass to custom HTML table
            h1 = "Mode"
            h2 = "Kills"
            h3 = kd_type_str

            mode1 = mode_table_top3.loc[0, "mode"]
            mode2 = mode_table_top3.loc[1, "mode"]
            mode3 = mode_table_top3.loc[2, "mode"]
            mode1k = "%0.0f" % mode_table_top3.loc[0, kills_type]
            mode2k = "%0.0f" % mode_table_top3.loc[1, kills_type]
            mode3k = "%0.0f" % mode_table_top3.loc[2, kills_type]
            mode1kd = "%0.2f" % mode_table_top3.loc[0, kd_ratio]
            mode2kd = "%0.2f" % mode_table_top3.loc[1, kd_ratio]
            mode3kd = "%0.2f" % mode_table_top3.loc[2, kd_ratio]

            # Draws the custom table
            st.markdown(custom_table(
                h1=h1, h2=h2, h3=h3,
                map1=mode1, map2=mode2, map3=mode3,
                map1k=mode1k, map2k=mode2k, map3k=mode3k,
                map1kd=mode1kd, map2kd=mode2kd, map3kd=mode3kd
            ), unsafe_allow_html=True)

        # Begin main content
        st.markdown("---")
        st.title("Player statistics")

        # Map and mode filters
        filter_expander = st.beta_expander("Filter data", expanded=False)
        with filter_expander:
            # Lists all the unique maps
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
                # filtered_df["match_number"] = np.arange(1, len(filtered_df) + 1)
                filtered_df.loc[:, "match_number"] = np.arange(1, len(filtered_df) + 1)
            else:
                filtered_df = map_df[map_df["mode"].isin(mode_filter)]
                # filtered_df["match_number"] = np.arange(1, len(filtered_df) + 1)
                filtered_df.loc[:, "match_number"] = np.arange(1, len(filtered_df) + 1)

            # Adds the slider. Uses maximum of Cold War matches for comparison purposes
            count_col = len(filtered_df[filtered_df["Game"] == "Cold War"])
            if count_col == 0:
                slider_max_val_int = 1
            else:
                slider_max_val_int = int(count_col)

            # Added the slider into a 99% width column
            # without the column, the end of the slider clips inside the dropdown
            col1_test, col_empty = st.beta_columns((0.99, 0.01))
            with col1_test:
                recent_matches = st.slider("Show the most recent matches:",
                                           min_value=0,
                                           max_value=slider_max_val_int,
                                           value=slider_max_val_int)

            # Check whether to return N rows for multiple games or only Cold War
            if compare_data == "Yes":
                # Checks if a map filter is picked
                if map_filter:
                    # Checks the map filter value is in the Cold War dataframe
                    if not player_data[player_data["map_name"].isin(map_filter)].empty:
                        # If it is in Cold War dataframe, check now to see if in Bo4 dataframe
                        if not player_data_bo4[player_data_bo4["map_name"].isin(map_filter)].empty:
                            # Maps in both dataframes
                            # GET CW DATA
                            cw_data = filtered_df.loc["CW"]
                            cw_filtered = cw_data.head(recent_matches)
                            # cw_filtered["match_number"] = np.arange(1, len(cw_filtered) + 1)
                            cw_filtered.loc[:, "match_number"] = np.arange(1, len(cw_filtered) + 1)

                            # GET BO4 DATA
                            bo4_data = filtered_df.loc["BO4"]
                            bo4_filtered = bo4_data.head(recent_matches)
                            # bo4_filtered["match_number"] = np.arange(1, len(bo4_filtered) + 1)
                            bo4_filtered.loc[:, "match_number"] = np.arange(1, len(bo4_filtered) + 1)

                            # Final dataframe
                            final_data_frame = pd.concat([cw_filtered, bo4_filtered], keys=["CW", "BO4"])
                        else:
                            # Map only in CW
                            cw_data = filtered_df.loc["CW"]
                            cw_filtered = cw_data.head(recent_matches)
                            cw_filtered.loc[:, "match_number"] = np.arange(1, len(cw_filtered) + 1)
                            final_data_frame = cw_filtered.head(recent_matches)

                    # If the picked map is not in the Cold War dataframe, returns a BO4 dataframe
                    elif not player_data_bo4[player_data_bo4["map_name"].isin(map_filter)].empty:
                        # Map only in Bo4 dataframe
                        bo4_data = filtered_df.loc["BO4"]
                        bo4_filtered = bo4_data.head(recent_matches)
                        bo4_filtered.loc[:, "match_number"] = np.arange(1, len(bo4_filtered) + 1)
                        final_data_frame = bo4_filtered.head(recent_matches)

                # Check if we do have player data for BO4 first
                elif player_data_bo4.empty:
                    final_data_frame = filtered_df.head(recent_matches)

                # If map filter isn't picked, default to combine the two dataframes for output
                else:
                    # GET CW DATA
                    cw_data = filtered_df.loc["CW"]
                    cw_filtered = cw_data.head(recent_matches)

                    # Swapped to the below after receiveing terminal warnings.
                    # Can swap back to the commentend below this if necessary
                    cw_filtered.loc[:, "match_number"] = np.arange(1, len(cw_filtered) + 1)
                    # cw_filtered["match_number"] = np.arange(1, len(cw_filtered) + 1)

                    # GET BO4 DATA
                    bo4_data = filtered_df.loc["BO4"]
                    bo4_filtered = bo4_data.head(recent_matches)

                    # Swapped to the below after receiveing terminal warnings.
                    # Can swap back to the commentend below this if necessary
                    bo4_filtered.loc[:, "match_number"] = np.arange(1, len(bo4_filtered) + 1)
                    # bo4_filtered["match_number"] = np.arange(1, len(bo4_filtered) + 1)

                    # Final dataframe
                    final_data_frame = pd.concat([cw_filtered, bo4_filtered], keys=["CW", "BO4"])

            else:
                final_data_frame = filtered_df.head(recent_matches)

        # Converts below columns to Float64 from Object types
        final_data_frame.loc[:, "accuracy"] = pd.to_numeric(final_data_frame["accuracy"])
        final_data_frame.loc[:, "shotslanded"] = pd.to_numeric(final_data_frame["shotslanded"])
        final_data_frame.loc[:, "shots_missed"] = pd.to_numeric(final_data_frame["shots_missed"])
        final_data_frame.loc[:, "shots_fired"] = pd.to_numeric(final_data_frame["shots_fired"])

        # Uncomment here to see the resulting dataframe after adding/removing filters
        # st.write(final_data_frame)
        # st.write(final_data_frame.dtypes)

        # Imports and applies Altair theme from chart_theme.py
        # This will apply to all charts on the page
        alt.themes.register("streamlit", streamlit_theme)
        alt.themes.enable("streamlit")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # KD component
        # average_kd = final_data_frame[kd_ratio].mean()
        # rounded_kd = "%0.2f" % average_kd

        st.header("Player kills")
        # st.write(f"Average {kd_type_str} is {rounded_kd}")

        # Defines columns
        kills_col_1, kills_col_2 = st.beta_columns(2)

        # Decides what to display depending on if comparison data is enabled
        if compare_data == "Yes":
            with kills_col_1:
                # Converts the accuracy dataframe to a float64 type from object
                # average_kd = final_data_frame[kd_ratio].mean()
                # filtered_df["accuracy"] = pd.to_numeric(filtered_df["accuracy"])
                game_kd_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", kd_ratio].mean()
                st.write(f"Average {kd_type_str} in Cold War is **{game_kd_cw:0.2f}**")

            with kills_col_2:
                # filtered_df["accuracy"] = pd.to_numeric(filtered_df["accuracy"])
                game_kd_bo4 = filtered_df.loc[filtered_df["Game"] == "Black Ops 4", kd_ratio].mean()
                st.write(f"Average {kd_type_str} in Black Ops 4 is **{game_kd_bo4:0.2f}**")
        else:
            game_kd_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", kd_ratio].mean()
            st.write(f"Average {kd_type_str} in Cold War is **{game_kd_cw:0.2f}**")

        # Figures out whether to use EKIA or Kills for axis titles
        if kills_type == "ekia":
            kills_type_title = "EKIA"
        elif kills_type == "kills":
            kills_type_title = "Kills"

        # Configures the area portion of the chart
        kills_area = alt.Chart(final_data_frame).transform_fold(
            [kills_type, kd_ratio]
        ).mark_area().encode(
            alt.X("match_number:Q", title="Match number"),
            alt.Y(kills_type, title=kills_type_title),
            tooltip=[alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2")
                     ],
        )

        # Figures out whether to use EKIAKDR or KDR for titles
        if kd_ratio == "kd":
            kd_ratio_title = "KD Ratio"
        elif kd_ratio == "ekiadratio":
            kd_ratio_title = "EKIA Ratio"

        # Configures the line portion of the chart
        # kd_line = base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
        kd_line = alt.Chart(final_data_frame).mark_line(interpolate="monotone").encode(
            alt.X("match_number:Q"),
            alt.Y(kd_ratio, title=kd_ratio_title),
        ).interactive()

        area_plot = alt.layer(kills_area, kd_line).resolve_scale(
            y="independent").interactive()

        # Plots the data as a chart
        st.altair_chart(area_plot, use_container_width=True)

        # Test linear regression plot

        kd_points = alt.Chart(final_data_frame).mark_point().encode(
            x="match_number",
            y="deaths",
        )

        kd_reg_line = kd_points.transform_loess("match_number", "deaths").mark_line()

        # kd_reg = kd_points + kd_points.transform_regression("match_number", kd_ratio).mark_line()
        lyr = alt.layer(kd_points, kd_reg_line)
        st.altair_chart(kd_reg_line, use_container_width=True)

        if show_data:
            st.write("Player data:")
            final_data_frame_show = final_data_frame[
                ["map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]
            st.write(final_data_frame_show)
            st.markdown(get_table_download_link(final_data_frame_show), unsafe_allow_html=True)

        # ==== Accuracy component ==== #
        st.markdown("---")
        st.header("Player accuracy")

        # Defines columns
        accuracy_col_1, accuracy_col_2 = st.beta_columns(2)

        # Decides what to display depending on if comparison data is enabled
        if compare_data == "Yes":
            with accuracy_col_1:
                # Converts the accuracy dataframe to a float64 type from object
                filtered_df["accuracy"] = pd.to_numeric(filtered_df["accuracy"])
                game_accuracy_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", "accuracy"].mean()
                st.write(f"Average accuracy in Cold War is **{game_accuracy_cw:0.2f}%**")

            with accuracy_col_2:
                filtered_df["accuracy"] = pd.to_numeric(filtered_df["accuracy"])
                game_accuracy_bo4 = filtered_df.loc[filtered_df["Game"] == "Black Ops 4", "accuracy"].mean()
                st.write(f"Average accuracy in Black Ops 4 is **{game_accuracy_bo4:0.2f}%**")

            # Draws the accuracy chart comparing Games
            selector = alt.selection_multi(
                fields=["Game"],
                bind="legend"
            )

            st.info("You can isolate each game by clicking the game's name in the chart legend")

            acc_chart = alt.Chart(final_data_frame).mark_area(line=True).transform_fold(
                fold=["Game"],
            ).encode(
                alt.X("match_number", title="Match number"),
                alt.Y("accuracy", title="Accuracy"),
                color="Game",
                order=alt.Order("Game", sort="descending"),
                tooltip=[alt.Tooltip("Game"),
                         alt.Tooltip("accuracy", format="0.3", title="Accuracy"),
                         alt.Tooltip(kills_type, title=kills_type_title),
                         alt.Tooltip(kd_ratio, format="0.2", title=kd_ratio_title),
                         alt.Tooltip("map_name", title="Map name"),
                         alt.Tooltip("mode", title="Mode"),
                         alt.Tooltip("match_number", title="Match number")
                         ],
                opacity=alt.condition(selector, alt.value(0.8), alt.value(0.2))
            ).add_selection(
                selector
            ).interactive()

            final_data_frame_show = final_data_frame[
                ["Game", "accuracy", "map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]

        else:
            average_accuracy = final_data_frame["accuracy"].mean()
            st.write(f"Average player accuracy is **{average_accuracy:0.2f}%**")

            # Draws the accuracy chart without
            acc_chart = alt.Chart(final_data_frame).mark_area(line=True).encode(
                alt.X("match_number", title="Match number"),
                alt.Y("accuracy:Q", title="Accuracy"),
                tooltip=[alt.Tooltip(kills_type),
                         alt.Tooltip("deaths"),
                         alt.Tooltip("map_name"),
                         alt.Tooltip("mode"),
                         alt.Tooltip(kd_ratio, format="0.2"),
                         alt.Tooltip("match_number")
                         ]
            ).interactive()

            final_data_frame_show = final_data_frame[
                ["accuracy", "map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]

        st.altair_chart(acc_chart, use_container_width=True)

        if show_data:
            st.write("Player data:")
            st.write(final_data_frame_show)
            st.markdown(get_table_download_link(final_data_frame_show), unsafe_allow_html=True)

        # BO4 data
        # st.write(player_data_bo4)

        # Sidebar footer
        with st.sidebar:
            st.markdown("---")
            st.subheader("FAQ")
            kia_ekia_expander = st.beta_expander("Differences between EKIA and Kills", expanded=False)
            with kia_ekia_expander:
                st.write("**Kills** are enemies which you dealt the final damage to, resulting in their death. "
                         "\n\n**EKIA** includes kills, as well as any other enemies who were killed by another player shortly "
                         "after you dealt damage to them.")

            data_delay = st.beta_expander("Data information", expanded=False)
            with data_delay:
                st.write(
                    "Data provided in this app is on a 30 minute lag and hence may not be "
                    "the most up-to-date."
                )

            # Blank headers used as a cheap spacer
            st.header("")
            st.info(
                "[Jon Cording](https://www.linkedin.com/in/jon-cording) maintains this app."
            )


# Render custom HTML
# st.markdown(html_custom_title("Page title"), unsafe_allow_html=True)

main()

# Draws the button on the sidebar which generates all the data
# This method will only let the main function re-run once
# the user clicks. This prevents data from attempting to
# load while picking different options

# if st.sidebar.button("Generate data"):
#     main()
