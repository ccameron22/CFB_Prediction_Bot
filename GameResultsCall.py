
import requests
import json
import pandas as pd
import os


# Authentication credentials for API request
headers = {"Authorization": "Your token here"}

# Convert to readable format
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# Get user input for parameters
#year = input("Enter year: ")
#week = input("Enter week: ")
#seasonType = input("Enter 'regular' or 'postseason': ")
#team = input("Enter team name: ")

# Parameters to be inserted into request
parameters = {
    "year": 2023,
    "week": 1,
    "seasonType": "regular",
    "team": "alabama"
}

# Function to call game results from API
def GameResults():
    # Make request to API for data in json format and print status code
    response = requests.get("https://api.collegefootballdata.com/games", headers=headers, params=parameters)
    print(response.status_code)
    # Convert json to human readable format
    jprint(response.json())

    df = pd.DataFrame(columns=['GameID', 'Home_Team', 'Away_Team'])


    # Get list
    data = response.json()
    # Extract data for database
    for d in data:
        home_team = d['home_team']
        home_score = d['home_points']
        away_team = d['away_team']
        away_score = d['away_points']
        away_conference = d['away_conference']
        if home_score > away_score:
            outcome = 'W'
        else:
            outcome = 'F'
        margin = home_score - away_score
        date = d['start_date'][:10]
        game_id = d['id']

        #rw = {'GameID': game_id, 'Home_Team': home_score, 'Away_Team': away_score}
        #df.loc[len(df)] = rw
        df = df.append({'GameID': game_id, 'Home_Team': home_score, "Away_Team": away_score}, ignore_index=True)

    df.columns = ['GameID', home_team, away_team]

    # Check if the team folder exists, create if not
    folder_name = os.path.join("Teams", home_team)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = os.path.join(folder_name, f"{date}.csv")
    # If the file already exists, load, add the row, save
    if os.path.exists(filename):
        # Create a new row from the current game data
        newFrame = {"Opponent": away_team, "Conference": away_conference, "Outcome": outcome, "Margin": margin}
        existing = pd.read_csv(filename)
        update = existing.append(newFrame, ignore_index=True)
        update.to_csv(filename, index=False)
    # If not, create, add the row, save
    else:
        # Create a new row from the current game data
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
    #GameStatisctics(test)