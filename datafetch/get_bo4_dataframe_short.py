import requests
import pandas as pd
import numpy as np


def load_data_bo4_short(username, platform, num_matches):
    combo_df = pd.DataFrame()
    formatted_username = username.replace(" ", "%20")
    cod_data_url = f"https://api.tracker.gg/api/v1/black-ops-4/matches/{platform}/{formatted_username}?type=mp" \
                   f"&next=null"

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/50.0.2661.102 Safari/537.36"}

    result = requests.get(cod_data_url, headers=headers).json()

    try:
        next_page_val = result["data"]["metadata"]["next"]
    except:
        combo_df = pd.DataFrame()
        return combo_df

    # print(cod_data_url)
    # print(next_page_val)

    # Initialise a bunch of blank lists for each column to be used in the final dataframe
    matchid_list = []
    mapname_list = []
    mapimgurl_list = []
    modename_list = []
    duration_list = []
    durationValues_list = []
    kills_list = []
    ekiadratio_list = []
    accuracy_list = []
    shotslanded_list = []
    ekia_list = []
    score_list = []
    headshots_list = []
    assists_list = []
    spm_list = []
    deaths_list = []
    kd_list = []
    shotsmissed_list = []
    timeplayed_list = []
    timeplayedalive_list = []
    shotsfired_list = []

    for match_data in result["data"]["matches"]:
        matchid_list.append(match_data["attributes"]["id"])
        mapname_list.append(match_data["metadata"]["mapName"])
        mapimgurl_list.append(match_data["metadata"]["mapImageUrl"])
        modename_list.append(match_data["metadata"]["modeName"])
        duration_list.append(match_data["metadata"]["duration"]["value"])
        durationValues_list.append(match_data["metadata"]["duration"]["displayValue"])

        for player_data in match_data["segments"]:
            kills_list.append(player_data["stats"]["kills"]["value"])
            ekiadratio_list.append(player_data["stats"]["ekiadRatio"]["value"])
            accuracy_list.append(player_data["stats"]["accuracy"]["value"])
            shotslanded_list.append(player_data["stats"]["shotsLanded"]["value"])
            ekia_list.append(player_data["stats"]["ekia"]["value"])
            score_list.append(player_data["stats"]["score"]["value"])
            headshots_list.append(player_data["stats"]["headshots"]["value"])
            assists_list.append(player_data["stats"]["assists"]["value"])
            spm_list.append(player_data["stats"]["scorePerMinute"]["value"])
            deaths_list.append(player_data["stats"]["deaths"]["value"])
            kd_list.append(player_data["stats"]["kdRatio"]["value"])
            shotsmissed_list.append(player_data["stats"]["shotsMissed"]["value"])
            timeplayed_list.append(player_data["stats"]["timePlayed"]["value"])
            timeplayedalive_list.append(player_data["stats"]["timePlayedAlive"]["value"])
            shotsfired_list.append(player_data["stats"]["shotsFired"]["value"])

    while next_page_val > 0:
        next_cod_data_url = f"https://api.tracker.gg/api/v1/black-ops-4/matches/{platform}/{formatted_username}?type=mp" \
                            f"&next={next_page_val} "

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/50.0.2661.102 Safari/537.36"}

        result_2 = requests.get(next_cod_data_url, headers=headers).json()

        # This while makes us only load enough values such that it equals
        # the same or slightly more match than played in Cold War.
        # This is done so that we don't load thousands of matches from
        # previous Call of Duties; thus keeping better app performance.

        while len(kills_list) < num_matches:
            try:
                for match_data in result_2["data"]["matches"]:
                    matchid_list.append(match_data["attributes"]["id"])
                    mapname_list.append(match_data["metadata"]["mapName"])
                    mapimgurl_list.append(match_data["metadata"]["mapImageUrl"])
                    modename_list.append(match_data["metadata"]["modeName"])
                    duration_list.append(match_data["metadata"]["duration"]["value"])
                    durationValues_list.append(match_data["metadata"]["duration"]["displayValue"])

                    for player_data in match_data["segments"]:
                        try:
                            kills_list.append(player_data["stats"]["kills"]["value"])
                        except:
                            kills_list.append("0")

                        try:
                            ekiadratio_list.append(player_data["stats"]["ekiadRatio"]["value"])
                        except:
                            ekiadratio_list.append("0")

                        try:
                            accuracy_list.append(player_data["stats"]["accuracy"]["value"])
                        except:
                            accuracy_list.append("0")

                        try:
                            shotslanded_list.append(player_data["stats"]["shotsLanded"]["value"])
                        except:
                            shotslanded_list.append("0")

                        try:
                            ekia_list.append(player_data["stats"]["ekia"]["value"])
                        except:
                            ekia_list.append("0")

                        try:
                            score_list.append(player_data["stats"]["score"]["value"])
                        except:
                            score_list.append("0")

                        try:
                            headshots_list.append(player_data["stats"]["headshots"]["value"])
                        except:
                            headshots_list.append("0")

                        try:
                            assists_list.append(player_data["stats"]["assists"]["value"])
                        except:
                            assists_list.append("0")

                        try:
                            spm_list.append(player_data["stats"]["scorePerMinute"]["value"])
                        except:
                            spm_list.append("0")

                        try:
                            deaths_list.append(player_data["stats"]["deaths"]["value"])
                        except:
                            deaths_list.append("0")

                        try:
                            kd_list.append(player_data["stats"]["kdRatio"]["value"])
                        except:
                            kd_list.append("0")

                        try:
                            shotsmissed_list.append(player_data["stats"]["shotsMissed"]["value"])
                        except:
                            shotsmissed_list.append("0")

                        try:
                            timeplayed_list.append(player_data["stats"]["timePlayed"]["value"])
                        except:
                            timeplayed_list.append("0")

                        try:
                            timeplayedalive_list.append(player_data["stats"]["timePlayedAlive"]["value"])
                        except:
                            timeplayedalive_list.append("0")

                        try:
                            shotsfired_list.append(player_data["stats"]["shotsFired"]["value"])
                        except:
                            shotsfired_list.append("0")
            except:
                for data_error in result_2["errors"]:
                    error_code = data_error["code"]
        else:
            next_page_val = 0
            limit = "met"
            combo_df = pd.DataFrame(
                {
                    "match_id": matchid_list,
                    "map_name": mapname_list,
                    "map_img": mapimgurl_list,
                    "mode": modename_list,
                    "duration": duration_list,
                    "duration_mins": durationValues_list,
                    "kills": kills_list,
                    "ekiadratio": ekiadratio_list,
                    "accuracy": accuracy_list,
                    "shotslanded": shotslanded_list,
                    "ekia": ekia_list,
                    "score": score_list,
                    "headshots": headshots_list,
                    "assists": assists_list,
                    "spm": spm_list,
                    "deaths": deaths_list,
                    "kd": kd_list,
                    "shots_missed": shotsmissed_list,
                    "time_played": timeplayed_list,
                    "time_played_alive": timeplayedalive_list,
                    "shots_fired": shotsfired_list,
                })

        # Finds the next page value to append to end of API URL
        if limit != "met":
            try:
                next_page_val = result_2["data"]["metadata"]["next"]
            except:
                next_page_val = 0
        else:
            next_page_val = 0

    # Remove any left over items so that final dataframe is the same
    # length as the value given in the function's argument
    rows_to_drop = len(matchid_list) - num_matches

    if rows_to_drop < 0:
        rows_to_drop = 0

    combo_df.drop(combo_df.tail(rows_to_drop).index, inplace=True)

    combo_df["match_number"] = np.arange(1, len(combo_df) + 1)
    combo_df["Game"] = "Black Ops 4"

    return combo_df


# Test this module with the below
# username_val = "Cording Xx"
# platform_val = "xbl"
# num_matches = 17

# df = load_data_bo4_short(username_val, platform_val, num_matches)

# print(df.head(5))
# print(len(df.index))
# print(df.dtypes)
# print(df.columns)
