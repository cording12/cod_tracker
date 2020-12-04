"""Handles all of the data processing required"""

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
    """Loads the Cold War data via the load_data function"""
    print("LOADING CW DATA")
    base_df = load_data(plyr, pltf)
    base_df.loc[:, "ekiadratio"] = pd.to_numeric(base_df["ekiadratio"])
    base_df.loc[:, "ekia"] = pd.to_numeric(base_df["ekia"])
    base_df.loc[:, "accuracy"] = pd.to_numeric(base_df["accuracy"])
    base_df.loc[:, "shotslanded"] = pd.to_numeric(base_df["shotslanded"])
    base_df.loc[:, "shots_missed"] = pd.to_numeric(base_df["shots_missed"])
    base_df.loc[:, "shots_fired"] = pd.to_numeric(base_df["shots_fired"])
    return base_df


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_mw_data(plyr, pltf):
    """Loads all Modern Warfare data"""
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
    """Loads Modern Warfare data upto the same amount of matches that have been loaded by Cold War"""
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Modern Warfare data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        print("LOADING MW DATA")
        player_data_mw = load_data_mw_short(plyr, pltf, nmbr)

        if player_data_mw.empty:
            player_data_mw = pd.DataFrame()
            return player_data_mw
        else:
            player_data_mw.loc[:, "ekiadratio"] = pd.to_numeric(player_data_mw["ekiadratio"])
            player_data_mw.loc[:, "ekia"] = pd.to_numeric(player_data_mw["ekia"])
            player_data_mw.loc[:, "accuracy"] = pd.to_numeric(player_data_mw["accuracy"])
            player_data_mw.loc[:, "shotslanded"] = pd.to_numeric(player_data_mw["shotslanded"])
            player_data_mw.loc[:, "shots_missed"] = pd.to_numeric(player_data_mw["shots_missed"])
            player_data_mw.loc[:, "shots_fired"] = pd.to_numeric(player_data_mw["shots_fired"])
            return player_data_mw


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_bo4_data(plyr, pltf):
    """Loads all Black Ops 4 data"""
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Black Ops 4 data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        print("LOADING BO4 DATA")
        player_data_bo4 = load_data_bo4(plyr, pltf)

        if player_data_bo4.empty:
            player_data_bo4 = pd.DataFrame()
            return player_data_bo4
        else:
            return player_data_bo4


@st.cache(allow_output_mutation=True, show_spinner=False)
def load_bo4_data_short(plyr, pltf, nmbr):
    """Loads Black Ops 4 data upto the same amount of matches that have been loaded by Cold War"""
    if pltf == "xbl":
        pltf_str = "Xbox"
    else:
        pltf_str = "Playstation"

    with st.spinner(f"Loading Black Ops 4 data for {plyr} on {pltf_str}."
                    f"\n\n **Please note**: this may take a while the first time you load the data."):

        print("LOADING BO4 DATA")
        player_data_bo4 = load_data_bo4_short(plyr, pltf, nmbr)

        if player_data_bo4.empty:
            player_data_bo4 = pd.DataFrame()
            return player_data_bo4
        else:
            player_data_bo4.loc[:, "ekiadratio"] = pd.to_numeric(player_data_bo4["ekiadratio"])
            player_data_bo4.loc[:, "ekia"] = pd.to_numeric(player_data_bo4["ekia"])
            player_data_bo4.loc[:, "accuracy"] = pd.to_numeric(player_data_bo4["accuracy"])
            player_data_bo4.loc[:, "shotslanded"] = pd.to_numeric(player_data_bo4["shotslanded"])
            player_data_bo4.loc[:, "shots_missed"] = pd.to_numeric(player_data_bo4["shots_missed"])
            player_data_bo4.loc[:, "shots_fired"] = pd.to_numeric(player_data_bo4["shots_fired"])
            return player_data_bo4


def map_stats(player_data, kills_type, kd_ratio, n_val):
    """Calculates the top N maps by KD/EKIAD ratio"""
    # Group dataframe based on map name; values as averages
    map_mean_df = player_data.groupby(["map_name"]).mean()
    map_mean_df = map_mean_df.reset_index()

    # Create table for results
    map_table_data = map_mean_df[["map_name", kills_type, kd_ratio]]
    map_table = map_table_data.sort_values(by=[kd_ratio], ascending=False)
    map_table = map_table.reset_index()

    # Get top N only
    map_table_top = map_table.head(n_val)
    return map_table_top


def best_map(player_data, kd_ratio):
    """Gets the name of the best map by highest KD value.
    This should be run on the mean dataframe
    """
    max_kd_index_pos = player_data[kd_ratio].idxmax()
    best_map_name = player_data.loc[max_kd_index_pos, "map_name"]
    return best_map_name


def map_img_url(player_data, map_name):
    """Provides the image url that mathes the best map"""
    # Use the map name to get the map URl
    map_img_index_pos = player_data[player_data["map_name"] == map_name].index.values

    # Just added the .min to get the first value from the list of values
    map_url = player_data.loc[map_img_index_pos.min(), "map_img"]
    return map_url


def mode_stats(player_data, kills_type, kd_ratio, n_val):
    """Gets the top mode results by KD/EKIAD ratio"""
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
    """Returns the mode image url"""
    # Currently not API fed as generic images are used by tracker.gg
    mode_url = "https://trackercdn.com/cdn/cod.tracker.gg/modern-warfare/images/top-weapons-bg.jpg"
    return mode_url
