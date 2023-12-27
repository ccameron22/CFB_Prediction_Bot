
import requests
import json


# Authentication credentials for API request
headers = {"Authorization": "Your Key"}

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

def GameResults():
    # Make request to API for data in json format and print status code
    response = requests.get("https://api.collegefootballdata.com/games", headers=headers, params=parameters)
    print(response.status_code)
    # Convert json to human readable format
    jprint(response.json())

    # Get list
    data = response.json()
    # Extract data for database
    for d in data:
        home_team = d['home_team']
        home_points = d['home_points']
        away_team = d['away_team']
        away_score = d['away_points']


if __name__ == '__main__':
  GameResults()