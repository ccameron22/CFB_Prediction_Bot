import os
import pandas as pd

# Get the current directory
current_directory = os.getcwd()

# Get the name of the CSV file
csv_file_name = "2023"

# Construct the path to the CSV file
csv_file_path = os.path.join(current_directory, csv_file_name)

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    print(f"CSV file '{csv_file_name}' does not exist in the current directory.")
else:
    # Read and print the CSV file
    df = pd.read_csv(csv_file_path, index_col=False)
    print(df)