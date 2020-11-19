import json
import requests
import csv

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
