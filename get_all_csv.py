import json
import requests
import csv


def load_data():
    cod_data_url = "https://api.tracker.gg/api/v1/cold-war/matches/xbl/Cording%20Xx?type=mp&next=null"
    headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/50.0.2661.102 Safari/537.36'}
    result = requests.get(cod_data_url, headers=headers)

    # Checks the API is working. If not, exits code
    if result.status_code == 200:
        api_success = 1
    else:
        api_fail = result.status_code
        print(f"API Failed. Status code: {api_fail}")
        exit()

    # Load data into JSON format
    data = json.loads(result.content.decode())

    # Finds the next page value to append to end of API URL
    next_page_val = data["data"]["metadata"]["next"]

    fname = "output.csv"

    with open(fname, "w", newline="") as file:
        csv_file = csv.writer(file)
        csv_file.writerow([
            "Match ID",
            "Map name",
            "Map Image URL",
            "Mode",
            "Match duration (milliseconds)",
            "Match duration",
            "Kills",
            "XP at end",
            "EKIA Ratio",
            "Rank at end",
            "Accuracy",
            "Shots Landed",
            "Highest Multikill",
            "EKIA",
            "Score",
            "Headshots",
            "Assists",
            "Score per minute",
            "Deaths",
            "Damage dealt",
            "KD Ratio",
            "Shots Missed",
            "Multi Kills",
            "Highest Streak",
            "Hits",
            "Time played",
            "Suicides",
            "Time played alive",
            "Objectives",
            "Shots",
            "Shots fired"
        ])

        for match in data["data"]["matches"]:
            # Gets match specific data
            matchid_results = match["attributes"]["id"]
            mapname_results = match["metadata"]["mapName"]
            mapimgurl_results = match["metadata"]["mapImageUrl"]
            modename_results = match["metadata"]["modeName"]
            duration_results = match["metadata"]["duration"]["value"]
            durationValues_results = match["metadata"]["duration"]["displayValue"]

            for data_results in match["segments"]:
                # Gets player specific data
                kills_result = data_results["stats"]["kills"]["value"]
                ekiadRatio_result = data_results["stats"]["ekiadRatio"]["value"]
                accuracy_result = data_results["stats"]["accuracy"]["value"]
                shotsLanded_result = data_results["stats"]["shotsLanded"]["value"]
                highestMultikill_result = data_results["stats"]["highestMultikill"]["value"]
                ekia_result = data_results["stats"]["ekia"]["value"]
                score_result = data_results["stats"]["score"]["value"]
                headshots_result = data_results["stats"]["headshots"]["value"]
                assists_result = data_results["stats"]["assists"]["value"]
                spm_result = data_results["stats"]["scorePerMinute"]["value"]
                deaths_result = data_results["stats"]["deaths"]["value"]
                damage_result = data_results["stats"]["damageDealt"]["value"]
                kd_result = data_results["stats"]["kdRatio"]["value"]
                shotsMissed_result = data_results["stats"]["shotsMissed"]["value"]
                multikills_result = data_results["stats"]["multikills"]["value"]
                higheststreak_result = data_results["stats"]["highestStreak"]["value"]
                hits_result = data_results["stats"]["hits"]["value"]
                timeplayed_result = data_results["stats"]["timePlayed"]["value"]
                suicides_result = data_results["stats"]["suicides"]["value"]
                timeplayedAlive_result = data_results["stats"]["timePlayedAlive"]["value"]
                objectives_result = data_results["stats"]["objectives"]["value"]
                shots_result = data_results["stats"]["shots"]["value"]
                shotsFired_result = data_results["stats"]["shotsFired"]["value"]

                # These values aren't always present so adding error exceptions
                try:
                    xpAtEnd_result = data_results["stats"]["xpAtEnd"]["value"]
                except:
                    xpAtEnd_result = 0

                try:
                    rankAtEnd_result = data_results["stats"]["rankAtEnd"]["value"]
                except:
                    rankAtEnd_result = 0

                # Adds all the data to a CSV
                csv_file.writerow([
                    matchid_results,
                    mapname_results,
                    mapimgurl_results,
                    modename_results,
                    duration_results,
                    durationValues_results,
                    kills_result,
                    xpAtEnd_result,
                    ekiadRatio_result,
                    rankAtEnd_result,
                    accuracy_result,
                    shotsLanded_result,
                    highestMultikill_result,
                    ekia_result,
                    score_result,
                    headshots_result,
                    assists_result,
                    spm_result,
                    deaths_result,
                    damage_result,
                    kd_result,
                    shotsMissed_result,
                    multikills_result,
                    higheststreak_result,
                    hits_result,
                    timeplayed_result,
                    suicides_result,
                    timeplayedAlive_result,
                    objectives_result,
                    shots_result,
                    shotsFired_result])

    while next_page_val > 0:
        next_cod_data_url = f"https://api.tracker.gg/api/v1/cold-war/matches/xbl/Cording%20Xx?type=mp&next={next_page_val}"
        # next_cod_data_url = f"https://api.tracker.gg/api/v1/cold-war/matches/xbl/Cording%20Xx?type=mp&next=9999"
        headers = {
            "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(next_cod_data_url, headers=headers)

        # Checks the API is working. If not, exits code
        if result.status_code == 200:
            api_success = 1
        else:
            api_fail = result.status_code
            # print(f"API Failed. Status code: {api_fail}")
            exit()

        # Load data into JSON format
        data = json.loads(result.content.decode())

        # for result in data["errors"]:
        #     print(result["code"])

        with open(fname, "a", newline="") as file:
            csv_file = csv.writer(file)

            # try:
            #     for result in data["errors"]:
            #         err_code = result["code"]
            #         ()
            # except:
            #     ()

            try:
                for match in data["data"]["matches"]:
                    # Gets match specific data
                    matchid_results = match["attributes"]["id"]
                    mapname_results = match["metadata"]["mapName"]
                    mapimgurl_results = match["metadata"]["mapImageUrl"]
                    modename_results = match["metadata"]["modeName"]
                    duration_results = match["metadata"]["duration"]["value"]
                    durationValues_results = match["metadata"]["duration"]["displayValue"]

                    for data_results in match["segments"]:
                        # Gets player specific data
                        try:
                            kills_result = data_results["stats"]["kills"]["value"]
                        except:
                            kills_result = 0

                        try:
                            ekiadRatio_result = data_results["stats"]["ekiadRatio"]["value"]
                        except:
                            ekiadRatio_result = 0

                        try:
                            accuracy_result = data_results["stats"]["accuracy"]["value"]
                        except:
                            accuracy_result = 0
                        try:
                            shotsLanded_result = data_results["stats"]["shotsLanded"]["value"]
                        except:
                            shotsLanded_result = 0

                        try:
                            highestMultikill_result = data_results["stats"]["highestMultikill"]["value"]
                        except:
                            highestMultikill_result = 0

                        try:
                            ekia_result = data_results["stats"]["ekia"]["value"]
                        except:
                            ekia_result = 0

                        try:
                            score_result = data_results["stats"]["score"]["value"]
                        except:
                            score_result = 0

                        try:
                            headshots_result = data_results["stats"]["headshots"]["value"]
                        except:
                            headshots_result = 0

                        try:
                            assists_result = data_results["stats"]["assists"]["value"]
                        except:
                            assists_result = 0

                        try:
                            spm_result = data_results["stats"]["scorePerMinute"]["value"]
                        except:
                            spm_result = 0

                        try:
                            deaths_result = data_results["stats"]["deaths"]["value"]
                        except:
                            deaths_result = 0

                        try:
                            damage_result = data_results["stats"]["damageDealt"]["value"]
                        except:
                            damage_result = 0

                        try:
                            kd_result = data_results["stats"]["kdRatio"]["value"]
                        except:
                            kd_result = 0

                        try:
                            shotsMissed_result = data_results["stats"]["shotsMissed"]["value"]
                        except:
                            shotsMissed_result = 0

                        try:
                            multikills_result = data_results["stats"]["multikills"]["value"]
                        except:
                            multikills_result = 0

                        try:
                            higheststreak_result = data_results["stats"]["highestStreak"]["value"]
                        except:
                            higheststreak_result = 0

                        try:
                            hits_result = data_results["stats"]["hits"]["value"]
                        except:
                            hits_result = 0

                        try:
                            timeplayed_result = data_results["stats"]["timePlayed"]["value"]
                        except:
                            timeplayed_result = 0

                        try:
                            suicides_result = data_results["stats"]["suicides"]["value"]
                        except:
                            suicides_result = 0

                        try:
                            timeplayedAlive_result = data_results["stats"]["timePlayedAlive"]["value"]
                        except:
                            timeplayedAlive_result = 0

                        try:
                            objectives_result = data_results["stats"]["objectives"]["value"]
                        except:
                            objectives_result = 0

                        try:
                            shots_result = data_results["stats"]["shots"]["value"]
                        except:
                            shots_result = 0

                        try:
                            shotsFired_result = data_results["stats"]["shotsFired"]["value"]
                        except:
                            shotsFired_result = 0

                        try:
                            xpAtEnd_result = data_results["stats"]["xpAtEnd"]["value"]
                        except:
                            xpAtEnd_result = 0

                        try:
                            rankAtEnd_result = data_results["stats"]["rankAtEnd"]["value"]
                        except:
                            rankAtEnd_result = 0

                        # Adds all the data to a CSV
                        csv_file.writerow([
                            matchid_results,
                            mapname_results,
                            mapimgurl_results,
                            modename_results,
                            duration_results,
                            durationValues_results,
                            kills_result,
                            xpAtEnd_result,
                            ekiadRatio_result,
                            rankAtEnd_result,
                            accuracy_result,
                            shotsLanded_result,
                            highestMultikill_result,
                            ekia_result,
                            score_result,
                            headshots_result,
                            assists_result,
                            spm_result,
                            deaths_result,
                            damage_result,
                            kd_result,
                            shotsMissed_result,
                            multikills_result,
                            higheststreak_result,
                            hits_result,
                            timeplayed_result,
                            suicides_result,
                            timeplayedAlive_result,
                            objectives_result,
                            shots_result,
                            shotsFired_result])
            except:
                ()

        # Finds the next page value to append to end of API URL
        try:
            next_page_val = data["data"]["metadata"]["next"]
        except:
            exit()

# load_data()