
import GameResultsCall as grc
import pandas as pd

team = 'Alabama'
season = 2023

statsPath = f'Teams/{team}/{season}'

# Read in data
seasonStats = pd.read_csv(statsPath)
confStrength = pd.read_csv('ConferenceStrength.csv')

# Find statistics

averageMargin = round(seasonStats['Margin'].sum()/seasonStats['Margin'].count(), 2)

# Calculate the win rate of the season
win = 0
lose = 0
for value in seasonStats['Outcome']:
    if value == 'W':
        win += 1
    else:
        lose += 1
winRate = round(win/(win + lose), 3)

# Calculate strength of each game
calculatedGameValues = {}
for index, row in seasonStats.iterrows():
    oppCon = row['Conference']
    marVic = row['Margin']
    opponent = row['Opponent']
    test = confStrength["Conference"]
    if oppCon not in confStrength['Conference'].values:
        strength = 0.2
        calculatedGameValues[opponent] = marVic * strength
    else:
        for index, line in confStrength.iterrows():
            test = line["Conference"]
            if line['Conference'] == oppCon:
                strength = line['Strength'] * 0.2
                calculatedGameValues[opponent] = marVic * strength
print(calculatedGameValues)

# Print results to check validity
print("Average Margin of Victory: ", averageMargin)
print("Win Rate: ", winRate)
