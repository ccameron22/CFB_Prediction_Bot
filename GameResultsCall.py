import sys

import requests
import json
import pandas as pd
import os


# Authentication credentials for API request
headers = {"Authorization": "Bearer xmp7pWvJT4r2fqy2jKYne3JZUojqOEC7l0Obn1Kq33Zkp/yxXIGS4nlxT9ZtIn/y"}

# Convert to readable format
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    #print(text)
    if text == '[]':
        return 0
    else:
        return 1

# Get user input for parameters
#year = input("Enter year: ")
#week = input("Enter week: ")
#seasonType = input("Enter 'regular' or 'postseason': ")
#team = input("Enter team name: ")

# Hardcoded parameters for testing
year = 2023
week = 1
seasonType = 'regular'
team = 'alabama'

parameters = {
    "year": year,
    "week": week,
    "seasonType": seasonType,
    "team": team
}


# Function to call game results from API
def GameResults():
    # Make request to API for data in json format and print status code
    response = requests.get("https://api.collegefootballdata.com/games", headers=headers, params=parameters)
    print(response.status_code)
    print(response)

    # Convert json to human readable format
    # jprint(response.json())
    # Check if the json is empty; Empty = bye week, return 0 and skip the rest of the function
    if jprint(response.json()) == 0:
        print('No Game')
        return 0

    # Deprecated; Used for testing
    # df = pd.DataFrame(columns=['GameID', 'Home_Team', 'Away_Team'])


    # Get list
    data = response.json()
    for d in data:
        home_team = d['home_team']
    home_team = home_team.lower()
    # Extract data for database
    # If the team that was pulled for is the away team, flip the values to
    # keep consistent with the script
    if home_team == team:
        for d in data:
            home_team = d['home_team']
            home_score = d['home_points']
            away_team = d['away_team']
            away_score = d['away_points']
            away_conference = d['away_conference']
    else:
        for d in data:
            home_team = d['away_team']
            home_score = d['away_points']
            away_team = d['home_team']
            away_score = d['home_points']
            away_conference = d['home_conference']

    if home_score > away_score:
        outcome = 'W'
    else:
        outcome = 'F'
    margin = home_score - away_score
    season = str(d['season'])
    #date = d['start_date'][:10]
    game_id = d['id']

        # Deprecated; Used to check output is correct
        #rw = {'GameID': game_id, 'Home_Team': home_score, 'Away_Team': away_score}
        #df.loc[len(df)] = rw
        #df = df.append({'GameID': game_id, 'Home_Team': home_score, "Away_Team": away_score}, ignore_index=True)

    #df.columns = ['GameID', home_team, away_team]

    # Check if the team folder exists, create if not
    folderName = os.path.join("Teams", team)
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    filename = os.path.join(folderName, season)
    # If the file already exists:
    if os.path.exists(filename):
        # Read the file and create the new row
        existing = pd.read_csv(filename)
        newFrame = pd.DataFrame(
            {"Opponent": away_team, "Conference": away_conference, "Outcome": outcome, "Margin": margin}, index=[0])
        update = existing.append(newFrame, ignore_index=True)
        update.to_csv(filename, index=False)
    # If the file doesn't exist:
    else:
        # Create a new row from the current game data and save as a csv
        newFrame = pd.DataFrame(
            {"Opponent": [away_team], "Conference": [away_conference], "Outcome": [outcome], "Margin": [margin]})
        newFrame.to_csv(filename, index=False)

    #df.to_csv('C:/Temp/PandasExport.csv', index=False)

    return game_id


# Function to call game statistics from API
def GameStatisctics(game_id):
    print(game_id)
    response = requests.get("https://api.collegefootballdata.com/game/box/advanced", headers=headers, params={"gameId": game_id})
    print(response.status_code)
    # Convert json to human readable format
    jprint(response.json())


if __name__ == '__main__':
    # Call GameResults function and capture Game ID
    # to pass to GameStatistics function
    test = GameResults()
    print()
    print()
    #if test != 0:
        #GameStatisctics(test)