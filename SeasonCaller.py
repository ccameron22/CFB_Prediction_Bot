import subprocess

for i in range(1, 14):
    subprocess.run(["python", "GameResultsCall.py", str(i)])
