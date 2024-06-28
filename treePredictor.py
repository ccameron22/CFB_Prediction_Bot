
import math
import numpy as np
import sys
import os
import DTLearner as dt

# Define a function to process each line of the CSV file
def process_line(line):
    parts = line.strip().split(',')
    # Drop the first and sixth items
    processed_parts = parts[1:5] + parts[6:]
    return ','.join(processed_parts) + '\n'

strength = {}
with open('ConferenceStrength.csv', 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        strength[parts[0]] = parts[1]

# inf = open(sys.argv[1])
inf = open('Teams/lsu/2022')

# Create a new file to store the modified data temporarily
temp_filename = 'temp_modified_file.csv'
with open(temp_filename, 'w') as temp_file:
    for line in inf.readlines()[1:]:
        processed_line = process_line(line)
        temp_file.write(processed_line)

inf.close()

inf = open('temp_modified_file.csv')

data = np.array(
    [list(map(float, s.strip().split(",")[1:])) for s in inf.readlines()[1:]]
)

inf.close()

os.remove('temp_modified_file.csv')


# compute how much of the data is training and testing
train_rows = data.shape[0] - 1
test_rows = 1  # Since we're leaving only the last row for testing

# separate out training and testing data
train_x = data[:train_rows, 0:-1]
train_y = data[:train_rows, -1]
test_x = data[train_rows:, 0:-1]
test_y = data[train_rows:, -1]

learner = dt.DTLearner(leaf_size=1, verbose=True)
learner.add_evidence(train_x, train_y)


# evaluate in sample
pred_y_in = learner.query(train_x)  # get the predictions
rmseIn = math.sqrt(((train_y - pred_y_in) ** 2).sum() / train_y.shape[0])
c = np.corrcoef(pred_y_in, y=train_y)


# evaluate out of sample
pred_y_out = learner.query(test_x)  # get the predictions
rmseOut = math.sqrt(((test_y - pred_y_out) ** 2).sum() / test_y.shape[0])
cOut = np.corrcoef(pred_y_out, y=test_y)

print("RMSE In: ", rmseIn)
print("RMSE Out: ", rmseOut)