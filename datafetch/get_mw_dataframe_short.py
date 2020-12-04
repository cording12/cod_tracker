import requests
import pandas as pd
import numpy as np


def load_data_mw_short(username, platform, num_matches):
    combo_df = pd.DataFrame()
    formatted_username = username.replace(" ", "%20")
    cod_data_url = f"https://api.tracker.gg/api/v1/modern-warfare/matches/{platform}/{formatted_username}?type=mp" \
                   f"&next=null"

    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/50.0.2661.102 Safari/537.36"}

    result = requests.get(cod_data_url, headers=headers).json()

    try:
        next_page_val = result["data"]["metadata"]["next"]
    except:
        combo_df = pd.DataFrame()
        return combo_df

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
            if player_data["type"] == "overview":
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

    while next_page_val > 0:
        next_cod_data_url = f"https://api.tracker.gg/api/v1/modern-warfare/matches/{platform}/{formatted_username}?type=mp" \
                            f"&next={next_page_val}"

        result_2 = requests.get(next_cod_data_url, headers=headers).json()

        try:
            for match_data in result_2["data"]["matches"]:
                matchid_list.append(match_data["attributes"]["id"])
                mapname_list.append(match_data["metadata"]["mapName"])
                mapimgurl_list.append(match_data["metadata"]["mapImageUrl"])
                modename_list.append(match_data["metadata"]["modeName"])
                duration_list.append(match_data["metadata"]["duration"]["value"])
                durationValues_list.append(match_data["metadata"]["duration"]["displayValue"])
                for player_data in match_data["segments"]:
                    if player_data["type"] == "overview":
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

        # Passing the Kills and KDR list into EKIA/EKIADRatio because
        # these values are not present from this API. When comparing
        # this data with other games, values appear as empty when
        # comparing EKIA/EKIADRatio
        combo_df = pd.DataFrame(
            {
                "match_id": matchid_list,
                "map_name": mapname_list,
                "map_img": mapimgurl_list,
                "mode": modename_list,
                "duration": duration_list,
                "duration_mins": durationValues_list,
                "kills": kills_list,
                # "ekiadratio": ekiadratio_list,
                "ekiadratio": kd_list,
                "accuracy": accuracy_list,
                "shotslanded": shotslanded_list,
                # "ekia": ekia_list,
                "ekia": kills_list,
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

        if len(matchid_list) > num_matches:
            next_page_val = 0
        else:
            try:
                next_page_val = result_2["data"]["metadata"]["next"]
            except:
                next_page_val = 0

    rows_to_drop = len(matchid_list) - num_matches
    if rows_to_drop < 0:
        rows_to_drop = 0

    combo_df.drop(combo_df.tail(rows_to_drop).index, inplace=True)
    combo_df["match_number"] = np.arange(1, len(combo_df) + 1)
    combo_df["Game"] = "Modern Warfare"

    return combo_df


# Test this module with the below
# username_val = "Cording Xx"
# platform_val = "xbl"
# number_matches = 101
# df = load_data_mw_short(username_val, platform_val, number_matches)
#
# print(df.head)
# print(len(df.index))
# print(df.dtypes)
# print(df.columns)
#
# match_id_count = df["match_id"].unique()
# print(f"Total different matches loaded: {len(match_id_count)}")
