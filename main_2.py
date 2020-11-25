from get_cw_dataframe import load_data
from get_bo4_dataframe import load_data_bo4
from user_download import get_table_download_link
from chart_theme import streamlit_theme, streamlit_theme_alt
from resources.custom_html import \
    html_custom_title,\
    assign_id, \
    set_background_image_fill_overlay
#
from jinja2 import Environment, FileSystemLoader
import streamlit.components.v1 as components
#

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import colours

# Initialise the sidebar and gets the user's options
with st.sidebar:
    playername = st.text_input("Enter your platform username here", "Cording Xx")
    platform = st.radio("Pick a platform", ["Xbox", "Playstation"])
    ekia_or_kia = st.radio("Use EKIA or Kills?", ["EKIA", "Kills"])
    compare_data = st.radio("Compare with previous CoD data?", ["Yes", "No"], 1)

# Converts platform to required string for API call
if platform == "Xbox":
    platform_picked = "xbl"
else:
    # Can test playstation username with SeanEDawgz
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


# Passes the user choices to the load_data function and returns a dataframe
@st.cache(allow_output_mutation=True, show_spinner=False)
def data_load_sequence(plyr, pltf):
    base_df = load_data(plyr, pltf)
    return base_df


@st.cache(allow_output_mutation=True, show_spinner=False)
def data_load_sequence_bo4(plyr, pltf):
    base_df_bo4 = load_data_bo4(plyr, pltf)
    return base_df_bo4


def main():
    try:
        with st.spinner("Loading player data. Note: This may take a while the first time you load your data."):
            player_data = data_load_sequence(playername, platform_picked)
            player_data["match_number"] = np.arange(1, len(player_data) + 1)
            player_data["Game"] = "Cold War"
            error_collector = 0
    except:
        st.error("Unable to generate Cold War player data. Please check you typed the name correctly and selected the "
                 "right platform before trying again.")
        error_collector = 1
        st.stop()

    # Checks to see if user wants to load comparator data
    if compare_data == "Yes":
        try:
            with st.spinner("Loading Black Ops 4 player data. Note: This may take a while the first time you load "
                            "your data"):
                player_data_bo4 = data_load_sequence_bo4(playername, platform_picked)
                player_data_bo4["match_number"] = np.arange(1, len(player_data_bo4) + 1)
                player_data_bo4["Game"] = "Black Ops 4"
                error_collector = 0
        except:
            error_collector = 2
    else:
        player_data_bo4 = pd.DataFrame()

    # If data couldn't load, returns empty dataframe
    if error_collector == 2:
        player_data_bo4 = pd.DataFrame()

    # Checks there is a username entered before continuing
    if playername == "":
        st.error("Please enter your username/gamertag")
    elif error_collector == 1:
        st.error("Unable to generate Cold War player data. Please check you typed the name correctly and selected the "
                 "right platform before trying again.")
        st.stop()
    else:
        # Begins writing to the main page
        with st.sidebar:
            # Add option to show data
            show_data = st.checkbox("Show raw data")

        # Checks if there is any Bo4 data loaded
        if player_data_bo4.empty:
            all_data_frame = player_data
        else:
            frames = [player_data, player_data_bo4]
            all_data_frame = pd.concat(frames, keys=["CW", "BO4"])

        # Page title and text
        st.title("Call of Duty: Cold War")
        st.text(f"Showing player data for {playername} on {platform}.")

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # Adds the user performance boxes

        # # # # # # # # # # # # Map # # # # # # # # # # # #
        # Group dataframe based on map name; values as averages
        map_mean_df = player_data.groupby(["map_name"]).mean()
        map_mean_df = map_mean_df.reset_index()

        # Get the largest KD value
        max_kd_value = map_mean_df[kd_ratio].max()
        max_kd_value_formatted = "%0.2f" % max_kd_value

        # Get the index position of largest KD value
        max_kd_index_pos = map_mean_df[kd_ratio].idxmax()

        # Get the map name based off index position
        best_map_name = map_mean_df.loc[max_kd_index_pos, "map_name"]

        # Use the map name to get the map URl
        map_img_index_pos = player_data[player_data["map_name"] == best_map_name].index.values
        # Just added the .min to get the first value from the list of values
        map_img_url = player_data.loc[map_img_index_pos.min(), "map_img"]

        # # # # # # # # # # # # Mode # # # # # # # # # # # #
        # Group dataframe based on game mode; value as averages
        mode_mean_df = player_data.groupby(["mode"]).mean()
        mode_mean_df = mode_mean_df.reset_index()

        # Get largest KD values
        max_kd_value_mode = mode_mean_df[kd_ratio].max()
        max_kd_value_formatted_mode = "%0.2f" % max_kd_value_mode

        # Get the index position of largest KD value
        max_kd_index_pos_mode = mode_mean_df[kd_ratio].idxmax()

        # Get the mode name based off index position
        best_mode_name = mode_mean_df.loc[max_kd_index_pos_mode, "mode"]

        # No mode image generated through the API so using the same as tracker.gg
        mode_img_url = "https://trackercdn.com/cdn/cod.tracker.gg/modern-warfare/images/top-weapons-bg.jpg"

        # Create table for top 3 map results
        map_table_data = map_mean_df[["map_name", kills_type, kd_ratio]]
        map_table = map_table_data.sort_values(by=[kd_ratio], ascending=False)
        map_table = map_table.set_index("map_name")

        # Get top 3 only
        map_table_top3 = map_table.head(3)

        # Format the table results
        map_table = map_table_top3.style.format({
            kd_ratio: '{:,.2f}'.format,
            kills_type: '{:,.0f}'.format,
        })

        # Create table for top 3 game mode results
        mode_table_data = mode_mean_df[["mode", kills_type, kd_ratio]]
        mode_table = mode_table_data.sort_values(by=[kd_ratio], ascending=False)
        mode_table = mode_table.set_index("mode")

        # Get top 3 only
        mode_table_top3 = mode_table.head(3)

        # Format the table results
        mode_table = mode_table_top3.style.format({
            kd_ratio: '{:,.2f}'.format,
            kills_type: '{:,.0f}'.format,
        })

        # Define two columns
        col1, col2 = st.beta_columns(2)

        with col1:
            st.subheader("Map summary")
            # Assigns unique ID to the div so we can style it
            st.markdown(assign_id("col_1_map_summary"), unsafe_allow_html=True)

            # Styles the above with given BG image
            st.markdown(set_background_image_fill_overlay("col_1_map_summary", map_img_url), unsafe_allow_html=True)

            st.table(map_table)
            st.info(f"**Best map by KD**"
                    f"\n\n{best_map_name}"
                    f"\n\nKD: {max_kd_value_formatted}"
                    )

        with col2:
            st.subheader("Mode summary")
            st.markdown(assign_id("col_2_mode_summary"),unsafe_allow_html=True)
            st.markdown(set_background_image_fill_overlay("col_2_mode_summary", mode_img_url), unsafe_allow_html=True)

            st.table(mode_table)
            st.info(f"**Best game mode by KD**"
                    f"\n\n{best_mode_name}"
                    f"\n\nKD: {max_kd_value_formatted_mode}"
                    )

        # Map and mode filters
        filter_expander = st.beta_expander("Filter data", expanded=False)
        with filter_expander:
            # Lists all the unique maps
            map_names_unique = all_data_frame["map_name"].unique()
            map_filter = st.multiselect("Map", sorted(map_names_unique))

            # Configures dataframe with or without map filter
            if not map_filter:
                map_df = all_data_frame
                map_df["match_number"] = np.arange(1, len(map_df) + 1)
            else:
                map_df = all_data_frame[all_data_frame["map_name"].isin(map_filter)]
                map_df["match_number"] = np.arange(1, len(map_df) + 1)

            # Configures game modes available based on map selected
            game_modes_unique = map_df["mode"].unique()
            mode_filter = st.multiselect("Game mode", sorted(game_modes_unique))

            # Configures dataframe with or without the mode filter
            if not mode_filter:
                filtered_df = map_df

                filtered_df["match_number"] = np.arange(1, len(filtered_df) + 1)
            else:
                filtered_df = map_df[map_df["mode"].isin(mode_filter)]
                filtered_df["match_number"] = np.arange(1, len(filtered_df) + 1)

            # Adds the slider. Uses maximum of Cold War matches for comparison purposes
            count_col = len(filtered_df[filtered_df["Game"] == "Cold War"])
            if count_col == 0:
                slider_max_val_int = 1
            else:
                slider_max_val_int = int(count_col)

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
                            cw_filtered["match_number"] = np.arange(1, len(cw_filtered) + 1)

                            # GET BO4 DATA
                            bo4_data = filtered_df.loc["BO4"]
                            bo4_filtered = bo4_data.head(recent_matches)
                            bo4_filtered["match_number"] = np.arange(1, len(bo4_filtered) + 1)

                            # Final dataframe
                            final_data_frame = pd.concat([cw_filtered, bo4_filtered], keys=["CW", "BO4"])
                        else:
                            # st.write("Map only in CW")
                            cw_data = filtered_df.loc["CW"]
                            cw_filtered = cw_data.head(recent_matches)
                            cw_filtered["match_number"] = np.arange(1, len(cw_filtered) + 1)
                            final_data_frame = cw_filtered.head(recent_matches)

                    # If the picked map is not in the Cold War dataframe, returns a BO4 dataframe
                    elif not player_data_bo4[player_data_bo4["map_name"].isin(map_filter)].empty:
                        # st.write("Map only in Bo4 dataframe")
                        bo4_data = filtered_df.loc["BO4"]
                        bo4_filtered = bo4_data.head(recent_matches)
                        bo4_filtered["match_number"] = np.arange(1, len(bo4_filtered) + 1)
                        final_data_frame = bo4_filtered.head(recent_matches)

                # If map filter isn't picked, default to combine the two dataframes for output
                else:
                    # GET CW DATA
                    cw_data = filtered_df.loc["CW"]
                    cw_filtered = cw_data.head(recent_matches)
                    cw_filtered["match_number"] = np.arange(1, len(cw_filtered) + 1)

                    # GET BO4 DATA
                    bo4_data = filtered_df.loc["BO4"]
                    bo4_filtered = bo4_data.head(recent_matches)
                    bo4_filtered["match_number"] = np.arange(1, len(bo4_filtered) + 1)

                    # Final dataframe
                    final_data_frame = pd.concat([cw_filtered, bo4_filtered], keys=["CW", "BO4"])

                    # Converts below columns to Float64 from Object types
                    final_data_frame["accuracy"] = pd.to_numeric(final_data_frame["accuracy"])
                    final_data_frame["shotslanded"] = pd.to_numeric(final_data_frame["shotslanded"])
                    final_data_frame["shots_missed"] = pd.to_numeric(final_data_frame["shots_missed"])
                    final_data_frame["shots_fired"] = pd.to_numeric(final_data_frame["shots_fired"])


            else:
                final_data_frame = filtered_df.head(recent_matches)

                # Converts below columns to Float64 from Object types
                final_data_frame["accuracy"] = pd.to_numeric(final_data_frame["accuracy"])
                final_data_frame["shotslanded"] = pd.to_numeric(final_data_frame["shotslanded"])
                final_data_frame["shots_missed"] = pd.to_numeric(final_data_frame["shots_missed"])
                final_data_frame["shots_fired"] = pd.to_numeric(final_data_frame["shots_fired"])

        # Uncomment here to see the resulting dataframe after adding/removing filters
        # st.write(final_data_frame)

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # KD component
        average_kd = final_data_frame[kd_ratio].mean()
        rounded_kd = "%0.2f" % average_kd

        st.subheader(f"Average {kd_type_str} is {rounded_kd}")

        # Imports and applies Altair theme from chart_theme.py
        # This will apply to all charts on the page
        alt.themes.register("streamlit", streamlit_theme)
        alt.themes.enable("streamlit")

        # Sets the chart base
        base = alt.Chart(final_data_frame).encode(
            alt.X("match_number:T", axis=alt.Axis(title=None))
        )

        # Figures out whether to use EKIA or Kills for axis titles
        if kills_type == "ekia":
            kills_type_title = "EKIA"
        elif kills_type == "kills":
            kills_type_title = "Kills"

        # Configures the area portion of the chart
        # kills_area = alt.Chart(final_data_frame).mark_area(opacity=0.3, color="#052BF9").encode(
        kills_area = alt.Chart(final_data_frame).mark_area(opacity=1).encode(
            alt.X("match_number", title="Match number"),
            alt.Y(kills_type, title=kills_type_title),
            tooltip=[alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2")
                     ]
        )

        # Figures out whether to use EKIAKDR or KDR for titles
        if kd_ratio == "kd":
            kd_ratio_title = "KD Ratio"
        elif kd_ratio == "ekiadratio":
            kd_ratio_title = "EKIA Ratio"

        # Configures the line portion of the chart
        # kd_line = base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
        kd_line = base.mark_line(interpolate="monotone").encode(
            alt.Y(kd_ratio,
                  axis=alt.Axis(title=kd_ratio_title, titleColor='#000000'))
        ).interactive()

        area_plot = alt.layer(kills_area, kd_line).resolve_scale(
            y="independent").interactive()

        # Plots the data as a chart
        st.altair_chart(area_plot, use_container_width=True)

        if show_data:
            st.write("Player data:")
            final_data_frame_show = final_data_frame[
                ["map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]
            st.write(final_data_frame_show)
            st.markdown(get_table_download_link(final_data_frame_show), unsafe_allow_html=True)

        # ==== Accuracy component ==== #
        st.markdown("---")
        st.header("Player accuracy")

        average_accuracy = filtered_df["accuracy"].mean()
        rounded_accuracy = "%0.2f" % average_accuracy

        # Defines columns
        accuracy_col_1, accuracy_col_2 = st.beta_columns(2)

        # Decides what to display depending on if comparison data is enabled
        if compare_data == "Yes":
            with accuracy_col_1:
                # Converts the accuracy dataframe to a float64 type from object
                filtered_df["accuracy"] = pd.to_numeric(filtered_df["accuracy"])
                game_accuracy_cw = filtered_df.loc[filtered_df["Game"] == "Cold War", "accuracy"].mean()

                # game_accuracy_cw_df = filtered_df[filtered_df["Game"] == "Cold War"]
                # st.write(game_accuracy_cw_df)
                # game_accuracy_cw_mean = game_accuracy_cw_df["accuracy"].mean(skipna=True)
                # st.write(game_accuracy_cw)

                # game_accuracy_cw = filtered_df["Game"] == "Cold War"
                # game_accuracy_bo4 = filtered_df["Game"] == "Black Ops 4"
                # st.write(game_accuracy_cw)
                # game_accuracy_mean_cw = filtered_df.loc[game_accuracy_cw, "accuracy"].mean()
                # # game_accuracy_mean_bo4 = filtered_df.loc[game_accuracy_bo4, "accuracy"].mean()

                # average_accuracy_bo4 = filtered_df["accuracy"].median()
                # rounded_accuracy_bo4 = "%0.2f" % average_accuracy_bo4

                st.write(f"Average accuracy in Cold War is {game_accuracy_cw}%")

            with accuracy_col_2:
                st.write(f"Average accuracy in Black Ops 4 is {game_accuracy_mean_bo4}%")
        else:
            st.subheader(f"Average player accuracy is {rounded_accuracy}%")

        acc_chart_1 = alt.Chart(final_data_frame).mark_area(line=True).transform_fold(
            fold=["Game"],
        ).encode(
            alt.X("match_number", title="Match number"),
            alt.Y("ekiadratio:Q", title="Accuracy"),
            color="Game",
            tooltip=[alt.Tooltip("Game"),
                     alt.Tooltip(kills_type),
                     alt.Tooltip("deaths"),
                     alt.Tooltip("map_name"),
                     alt.Tooltip("mode"),
                     alt.Tooltip(kd_ratio, format="0.2"),
                     alt.Tooltip("match_number")
                     ]
        ).interactive()

        st.altair_chart(acc_chart_1, use_container_width=True)

        # acc_chart_base = alt.Chart(filtered_df).encode(
        #     alt.X("match_number:T",
        #           title="Match no.",
        #           axis=alt.Axis)
        # )
        #
        # # acc_chart = acc_chart_base.mark_area(opacity=0.3, color="#052BF9").encode(
        # acc_chart = acc_chart_base.mark_area().encode(
        #     alt.X("match_number", title="Match number"),
        #     alt.Y("accuracy:Q", title="Accuracy"),
        #     tooltip=[alt.Tooltip("accuracy", format="0.3"),
        #              alt.Tooltip("kills"),
        #              alt.Tooltip("deaths")],
        # )
        #
        # layered_chart = alt.layer(acc_chart, kd_line).resolve_scale(
        #     y="independent").interactive()
        #
        # st.altair_chart(layered_chart, use_container_width=True)

        # # # # # # # # # # # # # # # # # # # # # # # #

        # st.subheader("KD compared with Black Ops 4")
        # st.write(bo4_recent_matches_df)
        #
        # bo4_average_kd = bo4_recent_matches_df[kd_ratio].mean()
        # bo4_rounded_kd = "%0.2f" % bo4_average_kd
        #
        # st.write(f"Average {kd_type_str} Cold War: {rounded_kd}")
        # st.write(f"Average {kd_type_str} BO4: {bo4_rounded_kd}")
        #
        # kd_line_layr1 = alt.Chart(recent_matches_df).transform_fold(
        #     ["kd"],
        # ).mark_line(interpolate="monotone").encode(
        #     alt.X("Index", title="Match number"),
        #     alt.Y("kd:Q"),
        #     color=alt.value(purple_hex),
        # ).interactive()
        #
        # kd_area_layr1 = alt.Chart(recent_matches_df).transform_fold(
        #     ["kd"],
        # ).mark_area(opacity=0.3).encode(
        #     alt.X("Index", title="Match number"),
        #     alt.Y("kd:Q"),
        #     color=alt.value(blue_hex),
        #     tooltip=[alt.Tooltip("Game"),
        #              alt.Tooltip(kills_type),
        #              alt.Tooltip("deaths"),
        #              alt.Tooltip("map_name"),
        #              alt.Tooltip("mode"),
        #              alt.Tooltip(kd_ratio, format="0.2")
        #              ]
        # ).interactive()
        #
        # kd_point_layr1 = alt.Chart(recent_matches_df).transform_fold(
        #     ["kd"],
        # ).mark_line(opacity=0.8).encode(
        #     alt.X("Index", title="Match number"),
        #     alt.Y("kd:Q"),
        #     color=alt.value(blue_hex),
        #     tooltip=[alt.Tooltip("Game"),
        #              alt.Tooltip(kills_type),
        #              alt.Tooltip("deaths"),
        #              alt.Tooltip("map_name"),
        #              alt.Tooltip("mode"),
        #              alt.Tooltip(kd_ratio, format="0.2")
        #              ]
        # ).interactive()
        #
        # bo4_kd_chart = alt.Chart(bo4_recent_matches_df).transform_fold(
        #     ["kd"],
        # ).mark_line(interpolate="monotone", strokeWidth=2).encode(
        #     alt.X("Index"),
        #     alt.Y("kd:Q", title="KD Ratio"),
        #     color=alt.value(purple_hex),
        #     tooltip=[alt.Tooltip("Game"),
        #              alt.Tooltip("kd"),
        #              alt.Tooltip("deaths"),
        #              alt.Tooltip("map_name"),
        #              alt.Tooltip("mode"),
        #              alt.Tooltip(kd_ratio, format="0.2")
        #              ]
        # ).interactive()
        #
        # layered_chart_4 = alt.layer(kd_area_layr1, kd_point_layr1, bo4_kd_chart)
        # st.altair_chart(layered_chart_4, use_container_width=True)
        # # # # # # # # # # # # # # # # # # # # # # # #

        kills_chart = alt.Chart(all_data_frame).mark_line(strokeWidth=2).encode(
            alt.X("match_number", title="Match number"),
            alt.Y("kills", title="Total kills"),
            color="Game"
        )

        st.altair_chart(kills_chart, use_container_width=True)

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



# Draws the button on the sidebar which generates all the data
# This method will only let the main function re-run once
# the user clicks. This prevents data from attempting to
# load while picking different options

# TODO remove the below in production?
main()

if st.sidebar.button("Generate data"):
    main()
