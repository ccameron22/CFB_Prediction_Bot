
import numpy as np
class DTLearner:
    def __init__(self, leaf_size, verbose=False):
        self.verbose = verbose
        self.leafSize = leaf_size

    def add_evidence(self, data_x, data_y):
        # This line caused a data type error. Wasted several hours trying to force the returned type to work
        # Reverted to the separate data x and y, was able to solve in 20 minutes
        # data = np.column_stack((data_x, data_y))

        self.DLTree = self.build_tree(data_x, data_y)


    def build_tree(self, data_x, data_y):
        # Check if the data has more than 1 point
        # Check if the data is all the same
        if data_x.shape[0] <= self.leafSize:
            return [['leaf', data_y[-1], None, None]]
        if np.all(data_y == data_y[0]):
            return [['leaf', data_y[-1], None, None]]
        else:
            # Find best correlation among features
            bestCorrelation = self.best_correlation(data_x, data_y)
            # Pull the value of all samples (rows) for the chosen feature (column) and find the median value
            splitVal = np.median(data_x[:, bestCorrelation])

            # Split the data on the median
            leftX = data_x[data_x[:, bestCorrelation] <= splitVal]
            leftY = data_y[data_x[:, bestCorrelation] <= splitVal]
            rightX = data_x[data_x[:, bestCorrelation] > splitVal]
            rightY = data_y[data_x[:, bestCorrelation] > splitVal]

            # Check which points are less than the split value
            leftCheck = data_x[:, bestCorrelation] <= splitVal
            # make a leaf to prevent infinite recursion
            if np.all(leftCheck == leftCheck[0]):
                return [['leaf', np.mean(data_y), None, None]]

            # Recursively build the left and right subtrees
            left_tree = self.build_tree(leftX, leftY)
            right_tree = self.build_tree(rightX, rightY)

            # Construct the root node
            root = [bestCorrelation, splitVal, 1, len(left_tree) + 1]

            # Combine the root node with left and right subtrees
            return [root] + left_tree + right_tree

    def best_correlation(self, data_x, data_y):
        i = np.corrcoef(data_x.T, data_y)
        # Pull the correlation of each feature and find the strongest correlation
        correlations = i[:-1, -1]
        bestCorrelation = np.argmax(np.abs(correlations))
        return bestCorrelation

    def query(self, points):
        # Load decision tree
        tree = self.DLTree
        # Create an empty numpy array with enough space for the points
        predictions = np.empty(len(points))
        count = 0
        # Cycle through the points
        for point in points:
            x = 0
            # Check if the node is a leaf
            # When a leaf is found, store the prediction and move on to the next point
            while tree[x][0] != 'leaf':
                # Check the value against the split value and move left or right
                splitFeature = tree[x][0]
                splitValue = tree[x][1]
                if point[splitFeature] <= splitValue:
                    x += tree[x][2]
                else:
                    x += tree[x][3]
            # Get predicted value from leaf
            prediction = tree[x][1]
            predictions[count] = prediction
            count += 1
        return predictions