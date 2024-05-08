
import GameResultsCall as grc
import pandas as pd

team = 'Alabama'
season = 2023

path = f'Teams/{team}/{season}'

# Read in data
seasonStats = pd.read_csv(path)

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


# Print results to check validity
print("Average Margin of Victory: ", averageMargin)
print("Win Rate: ", winRate)
