from get_cw_dataframe import load_data
from get_bo4_dataframe import load_data_bo4
from user_download import get_table_download_link
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
elif platform == "Playstation":
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
@st.cache(allow_output_mutation=True)
def data_load_sequence(plyr, pltf):
    base_df = load_data(plyr, pltf)
    return base_df


@st.cache(allow_output_mutation=True)
def data_load_sequence_bo4(plyr, pltf):
    base_df_bo4 = load_data_bo4(plyr, pltf)
    return base_df_bo4


try:
    player_data = data_load_sequence(playername, platform_picked)
    # player_data["index_col"] = player_data.reset_index().index
    player_data["match_number"] = np.arange(1, len(player_data)+1)
    player_data["Game"] = "Cold War"
    error_collector = 0
except:
    error_collector = 1

# Checks to see if user wants to load comparator data
if compare_data == "Yes":
    try:
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
else:
    # Begins writing to the main page
    with st.sidebar:
        # Add option to show data
        show_data = st.checkbox("Show raw data")

    st.title("Call of Duty: Cold War")
    st.text(f"Showing player data for {playername} on {platform}.")

    # Checks if there is any Bo4 data loaded
    if player_data_bo4.empty:
        all_data_frame = player_data
    else:
        # bo4_recent_matches_df = player_data_bo4.head(recent_matches + 1)
        frames = [player_data, player_data_bo4]
        all_data_frame = pd.concat(frames, keys=["CW", "BO4"])

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
                        # st.write("Maps in both dataframes")
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
        else:
            final_data_frame = filtered_df.head(recent_matches)

    # Uncomment here to see the resulting dataframe after adding/removing filters
    # st.write(final_data_frame)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # KD component
    average_kd = final_data_frame[kd_ratio].mean()
    rounded_kd = "%0.2f" % average_kd

    st.subheader(f"Average {kd_type_str} is {rounded_kd}")

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
    kills_area = alt.Chart(final_data_frame).mark_area(opacity=0.3, color="#052BF9").encode(
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
    kd_line = base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
        alt.Y(kd_ratio,
              axis=alt.Axis(title=kd_ratio_title, titleColor='#000000'))
    ).interactive()

    area_plot = alt.layer(kills_area, kd_line).resolve_scale(
        y="independent").interactive()

    # Plots the data as a chart
    st.altair_chart(area_plot, use_container_width=True)

    if show_data:
        st.write("Player data:")
        final_data_frame_show = final_data_frame[["map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]
        st.write(final_data_frame_show)
        st.markdown(get_table_download_link(final_data_frame_show), unsafe_allow_html=True)

    # ==== Accuracy component ==== #
    average_accuracy = filtered_df["accuracy"].median()
    rounded_accuracy = "%0.2f" % average_accuracy

    st.subheader(f"Average player accuracy is {rounded_accuracy}%")

    acc_chart_base = alt.Chart(filtered_df).encode(
        alt.X("Index:T",
              title="Match no.",
              axis=alt.Axis)
    )

    acc_chart = acc_chart_base.mark_area(opacity=0.3, color="#052BF9").encode(
        # alt.X("Index:T"),
        alt.X("Index", title="Match number"),
        alt.Y("accuracy:Q", title="Accuracy"),
        tooltip=[alt.Tooltip("accuracy", format="0.3"),
                 alt.Tooltip("kills"),
                 alt.Tooltip("deaths")],
    )

    layered_chart = alt.layer(acc_chart, kd_line).resolve_scale(
        y="independent").interactive()

    st.altair_chart(layered_chart, use_container_width=True)

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
        alt.X("Index", title="Match number"),
        alt.Y("kills", title="Total kills"),
        color="Game"
    )

    st.altair_chart(kills_chart, use_container_width=True)

    # BO4 data
    # st.write(player_data_bo4)

    # Sidebar footer
    with st.sidebar:
        # Forces the info to the bottom
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
        st.header("")
        st.info(
            "[Jon Cording](https://www.linkedin.com/in/jon-cording) maintains this app."
        )
