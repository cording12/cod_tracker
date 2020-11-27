from datafetch.get_cw_dataframe import load_data
from datafetch.get_bo4_dataframe import load_data_bo4
from datafetch.get_bo4_dataframe_short import load_data_bo4_short
from datafetch.get_mw_dataframe import load_data_mw
from datafetch.get_mw_dataframe_short import load_data_mw_short
import streamlit as st
import numpy as np
import pandas as pd


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_cw_data(plyr, pltf):
    base_df = load_data(plyr, pltf)
    return base_df


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_mw_data(plyr, pltf):
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Modern Warfare data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        player_data_mw = load_data_mw(plyr, pltf)

        if player_data_mw.empty:
            player_data_mw = pd.DataFrame()
            return player_data_mw
        else:
            return player_data_mw


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_mw_data_short(plyr, pltf, nmbr):
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Modern Warfare data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        player_data_mw = load_data_mw_short(plyr, pltf, nmbr)

        if player_data_mw.empty:
            player_data_mw = pd.DataFrame()
            return player_data_mw
        else:
            return player_data_mw


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_bo4_data(plyr, pltf):
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Black Ops 4 data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        player_data_bo4 = load_data_bo4(plyr, pltf)

        if player_data_bo4.empty:
            player_data_bo4 = pd.DataFrame()
            return player_data_bo4
        else:
            return player_data_bo4


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_bo4_data_short(plyr, pltf, nmbr):
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Black Ops 4 data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        player_data_bo4 = load_data_bo4_short(plyr, pltf, nmbr)

        if player_data_bo4.empty:
            player_data_bo4 = pd.DataFrame()
            return player_data_bo4
        else:
            return player_data_bo4


def map_stats(player_data, kills_type, kd_ratio, n_val):
    # Group dataframe based on map name; values as averages
    map_mean_df = player_data.groupby(["map_name"]).mean()
    map_mean_df = map_mean_df.reset_index()

    # Create table for top 3 map results
    map_table_data = map_mean_df[["map_name", kills_type, kd_ratio]]
    map_table = map_table_data.sort_values(by=[kd_ratio], ascending=False)
    map_table = map_table.reset_index()

    # Get top N only
    map_table_top = map_table.head(n_val)
    return map_table_top


def best_map(player_data, kd_ratio):
    max_kd_index_pos = player_data[kd_ratio].idxmax()
    best_map_name = player_data.loc[max_kd_index_pos, "map_name"]
    return best_map_name


def map_img_url(player_data, map_name):
    # Use the map name to get the map URl
    map_img_index_pos = player_data[player_data["map_name"] == map_name].index.values

    # Just added the .min to get the first value from the list of values
    map_url = player_data.loc[map_img_index_pos.min(), "map_img"]
    return map_url


def mode_stats(player_data, kills_type, kd_ratio, n_val):
    # Group dataframe based on map name; values as averages
    mode_mean_df = player_data.groupby(["mode"]).mean()
    mode_mean_df = mode_mean_df.reset_index()

    # Create table for top 3 map results
    mode_table_data = mode_mean_df[["mode", kills_type, kd_ratio]]
    mode_table = mode_table_data.sort_values(by=[kd_ratio], ascending=False)
    mode_table = mode_table.reset_index()

    # Get top N only
    mode_table_top = mode_table.head(n_val)
    return mode_table_top


def mode_img_url():
    # Currently not API fed as standard images are used
    mode_url = "https://trackercdn.com/cdn/cod.tracker.gg/modern-warfare/images/top-weapons-bg.jpg"
    return mode_url
