import requests
import pandas as pd


def load_data(username, platform, page):
    formatted_username = username.replace(" ", "%20")
    cod_data_url = f"https://api.tracker.gg/api/v1/cold-war/matches/{platform}/{formatted_username}?type=mp&next={page}"
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}

    result = requests.get(cod_data_url, headers=headers).json()

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
    highestmultikill_list = []
    ekia_list = []
    score_list = []
    headshots_list = []
    assists_list = []
    spm_list = []
    deaths_list = []
    damage_list = []
    kd_list = []
    shotsmissed_list = []
    multikills_list = []
    higheststreak_list = []
    hits_list = []
    timeplayed_list = []
    suicides_list = []
    timeplayedalive_list = []
    objectives_list = []
    shots_list = []
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
            highestmultikill_list.append(player_data["stats"]["highestMultikill"]["value"])
            ekia_list.append(player_data["stats"]["ekia"]["value"])
            score_list.append(player_data["stats"]["score"]["value"])
            headshots_list.append(player_data["stats"]["headshots"]["value"])
            assists_list.append(player_data["stats"]["assists"]["value"])
            spm_list.append(player_data["stats"]["scorePerMinute"]["value"])
            deaths_list.append(player_data["stats"]["deaths"]["value"])
            damage_list.append(player_data["stats"]["damageDealt"]["value"])
            kd_list.append(player_data["stats"]["kdRatio"]["value"])
            shotsmissed_list.append(player_data["stats"]["shotsMissed"]["value"])
            multikills_list.append(player_data["stats"]["multikills"]["value"])
            higheststreak_list.append(player_data["stats"]["highestStreak"]["value"])
            hits_list.append(player_data["stats"]["hits"]["value"])
            timeplayed_list.append(player_data["stats"]["timePlayed"]["value"])
            suicides_list.append(player_data["stats"]["suicides"]["value"])
            timeplayedalive_list.append(player_data["stats"]["timePlayedAlive"]["value"])
            objectives_list.append(player_data["stats"]["objectives"]["value"])
            shots_list.append(player_data["stats"]["shots"]["value"])
            shotsfired_list.append(player_data["stats"]["shotsFired"]["value"])

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
                "ekia": ekia_list,
                "score": score_list,
                "headshots": headshots_list,
                "assists": assists_list,
                "spm": spm_list,
                "deaths": deaths_list,
                "damage": damage_list,
                "kd": kd_list,
                "shots_missed": shotsmissed_list,
                "multikills": multikills_list,
                "highest_streak": higheststreak_list,
                "hits": hits_list,
                "time_played": timeplayed_list,
                "suicides": suicides_list,
                "time_played_alive": timeplayedalive_list,
                "objectives": objectives_list,
                "shots": shots_list,
                "shots_fired": shotsfired_list,
            }
        )
    return combo_df


# Test this module with the below
username_val = "Cording Xx"
platform_val = "xbl"
page_val = "null"

load_data(username_val, platform_val, page_val)
# load_data()


