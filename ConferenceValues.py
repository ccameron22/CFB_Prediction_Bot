import requests
import json
import pandas as pd


# Authentication credentials for API request
headers = {"Authorization": "Bearer xmp7pWvJT4r2fqy2jKYne3JZUojqOEC7l0Obn1Kq33Zkp/yxXIGS4nlxT9ZtIn/y"}

# Convert to readable format
def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def createConferences():
    # Create a dataframe to hold the strength score of the conferences. This must be manually updated
    # This will be the most subjective part of the bot
    conference_data = [
        {'Conference': "AAC", 'Strength': "2"},
        {'Conference': "ACC", 'Strength': "4"},
        {'Conference': "Big 10", 'Strength': "7"},
        {'Conference': "Big 12", 'Strength': "4"},
        {'Conference': "Conference USA", 'Strength': "1"},
        {'Conference': "MID", 'Strength': "1"},
        {'Conference': "MWC", 'Strength': "2"},
        {'Conference': "P12", 'Strength': "3"},
        {'Conference': "SEC", 'Strength': "7"},
        {'Conference': "OTH", 'Strength': "1"}
    ]
    conferenceDF = pd.DataFrame(conference_data)

    # Print out values to confirm, then save to csv in project folder
    print(conferenceDF.to_string(index=False))
    conferenceDF.to_csv(r'C:\Users\chase\OneDrive\Documents\Projects\CFB_Bot/ConferenceStrength.csv', index=False)

if __name__ == '__main__':
    createConferences()