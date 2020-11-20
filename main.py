from get_data_dataframe_2 import load_data
from user_download import get_table_download_link
import streamlit as st
import pandas as pd
import altair as alt

# VERY GOOD REFERENCE 
# https://github.com/streamlit/demo-self-driving/blob/master/streamlit_app.py

# Adds the sidebar and gets the user's options
with st.sidebar:
    playername = st.text_input("Enter your Xbox Live username here", "Cording Xx")
    platform = st.radio("Pick a platform", ["Xbox", "Playstation", "PC"])
    ekia_or_kia = st.radio("Use EKIA or Kills?", ["EKIA", "Kills"])

    # ADD DROPDOWN FOR THIS?
    st.info("**Kills** are enemies that you dealt final damange to resulting in their death. "
            "\n\n**EKIA** includes kills, as well as any other enemies who were killed by another player shortly "
            "after you dealt damage to them.")

    show_data = st.checkbox("Show raw data")

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
st.cache()


def data_load_sequence(plyr, pltf):
    base_df = load_data(plyr, pltf)
    return base_df


try:
    # player_data = load_data(playername, platform_picked)
    player_data = data_load_sequence(playername, platform_picked)
    player_data["Index"] = player_data.reset_index().index
    error_collector = 0
except:
    error_collector = 1

if playername == "":
    st.error("Please enter your username/gamertag")
elif error_collector == 1:
    st.error("Unable to generate data. Please check you typed the name correctly and selected the right platform "
             "before trying again.")
else:
    # Begins writing to the main page
    st.title("Call of Duty: Cold War")
    st.text(f"Showing player data for {playername} on {platform}.")

    # ==== KD component ==== #
    average_kd = player_data[kd_ratio].mean()
    rounded_kd = "%0.2f" % average_kd

    st.subheader(f"Average {kd_type_str} is {rounded_kd}")

    # Sets the chart base
    base = alt.Chart(player_data).encode(
        alt.X("Index:T", axis=alt.Axis(title=None))
    )

    # Figures out whether to use EKIA or Kills for titles
    if kills_type == "ekia":
        kills_type_title = "EKIA"
    elif kills_type == "kills":
        kills_type_title = "Kills"

    # Configures the area portion of the chart
    kills_area = alt.Chart(player_data).mark_area(opacity=0.3, color="#052BF9").encode(
        alt.X("Index", title="Match number"),
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
        player_stats_chart_data_df = player_data[["map_name", "mode", "ekia", "ekiadratio", "kills", "kd", "deaths"]]
        st.write(player_stats_chart_data_df)
        st.markdown(get_table_download_link(player_stats_chart_data_df), unsafe_allow_html=True)

    # ==== Accuracy component ==== #
    average_accuracy = player_data["accuracy"].median()
    rounded_accuracy = "%0.2f" % average_accuracy

    st.subheader(f"Average player accuracy is {rounded_accuracy}%")

    acc_chart_base = alt.Chart(player_data).encode(
        alt.X("Index:T",
              title="Match no.",
              axis=alt.Axis)
    )

    acc_chart = acc_chart_base.mark_area(opacity=0.3, color="#052BF9").encode(
        alt.X("Index:T"),
        alt.Y("accuracy:Q", title="Accuracy"),
        tooltip=[alt.Tooltip("accuracy", format="0.3"),
                 alt.Tooltip("kills"),
                 alt.Tooltip("deaths")],
    )

    kills_chart = acc_chart_base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
        alt.X("Index:T"),
        alt.Y("kills",
              title="Kills",
              axis=alt.Axis(grid=False)
              ),
        tooltip=["accuracy", "kills", "deaths"],
    )

    layered_chart = alt.layer(acc_chart, kills_chart).resolve_scale(
        y="independent").interactive()

    st.altair_chart(layered_chart, use_container_width=True)

    with st.sidebar:
        # Forces the info to the bottom
        st.header("")
        st.header("")

        st.header("Important app notes")
        st.info(
            "Data provided in this app is on a 30 minute lag and hence may not be "
            "the most up-to-date. Only the Xbox platform is currently supported.\n\n"
            "[Jon Cording](https://www.linkedin.com/in/jon-cording) maintains this app."
        )
