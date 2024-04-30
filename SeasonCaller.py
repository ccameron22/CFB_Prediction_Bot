import subprocess


year = 2023
season = 'regular'
team = 'alabama'

for i in range(1, 14):
    subprocess.run(["python", "GameResultsCall.py", str(i),str(year),season, team])
