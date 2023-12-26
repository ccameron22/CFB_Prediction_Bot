
import requests
import json


headers = {"Authorization": "Bearer xmp7pWvJT4r2fqy2jKYne3JZUojqOEC7l0Obn1Kq33Zkp/yxXIGS4nlxT9ZtIn/y"}

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

year = input("Enter year: ")
week = input("Enter week: ")
seasonType = input("Enter 'regular' or 'post': ")
team = input("Enter team name: ")

parameters = {
    "year": year,
    "week": week,
    "seasonType": seasonType,
    "team": team
}

response = requests.get("https://api.collegefootballdata.com/games", headers=headers, params=parameters)
print(response.status_code)
jprint(response.json())
