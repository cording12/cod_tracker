from get_all_csv import load_data
from user_download import get_table_download_link
import streamlit as st
import pandas as pd
import altair as alt

# The below gets new data as a CSV
# load_data()


def get_data():
    df = pd.read_csv("output.csv")
    del df["Match ID"]
    df["Index"] = df.reset_index().index
    return df


with st.sidebar:
    playername = st.text_input("Enter your Xbox Live username here")
    platform = st.radio("Pick a platform", ["Xbox", "Playstation", "PC"])



# Gets the data from the function
with st.spinner("Loading data"):
    # data_load_state = st.text("Loading data...")
    player_stats = get_data()
    # data_load_state = st.text('Loading data...done!')


st.title("Call of Duty:Cold War")
st.text(f"Showing data for player {playername} for {platform}.")

average_kd = player_stats["KD Ratio"].mean()
rounded_kd = "%0.2f" % average_kd

st.subheader(f"Average KD is {rounded_kd}")

base = alt.Chart(player_stats).encode(
    alt.X("Index:T", axis=alt.Axis(title=None))
)

kills_area = alt.Chart(player_stats).mark_area(opacity=0.3,color="#052BF9").encode(
    alt.X("Index", title="Match number"),
    alt.Y("Kills"),
    tooltip = [alt.Tooltip("Kills"),
               alt.Tooltip("Deaths"),
               alt.Tooltip("Map name"),
               alt.Tooltip("Mode"),
               alt.Tooltip("KD Ratio", format="0.2")
              ]
)

kd_line = base.mark_line(stroke="#6610f2", interpolate="monotone").encode(
    alt.Y("KD Ratio",
          axis=alt.Axis(title="KD Ratio", titleColor='#000000'))
).interactive()

area_plot = alt.layer(kills_area, kd_line).resolve_scale(
    y="independent").interactive()

# Plots the data as a chart
st.altair_chart(area_plot, use_container_width=True)

# Assign the stats used to new df
player_stats_chart_data_df = player_stats[["Map name", "Mode", "Kills", "Deaths", "KD Ratio"]]

st.write(player_stats_chart_data_df)
st.markdown(get_table_download_link(player_stats_chart_data_df), unsafe_allow_html=True)


# Adds sidebar with option to show data
with st.sidebar:
    show_data = st.checkbox("Show raw data")

    # Forces the info to the bottom
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("")
    st.header("Important app notes")
    st.info(
        "Data provided in this app is on a 30 minute lag and hence may not be "
        "the most up-to-date. Only the Xbox platform is currently supported.\n\n"
        "[Jon Cording](https://www.linkedin.com/in/joncording12/) maintains this app."
    )
    # st.markdown("<h1 style='position: relative; top:150px; color: red;'>Some title</h1>", unsafe_allow_html=True)



if show_data:
    st.subheader("Player data")
    st.write(player_stats)
    st.markdown(get_table_download_link(player_stats), unsafe_allow_html=True)

