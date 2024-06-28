import numpy as np
import random
import DTLearner as dt

class BagLearner:
    def __init__(self, learner, kwargs={"argument1": 1, "argument2": 2}, bags=20, boost=False, verbose=False):
        # Initialize attributes
        self.learner = learner
        self.kwargs = kwargs
        self.bags = bags
        self.verbose = verbose
        self.learners = []

    def add_evidence(self, data_x, data_y):
        # Find the length of a row (number of features)
        num = len(data_x[0])
        # Created subsets of x and y with the same datatype as x and y to avoid issues
        # when passing in as parameters to called learners
        data_x_subset = np.empty((self.bags, num), dtype=data_x.dtype)
        data_y_subset = np.empty(self.bags, dtype=data_y.dtype)

        # Loop through the process to create the desired number of learners
        for i in range(0, self.bags):
            # Generate subsets of data with 'bags' number of samples
            for j in range(0, self.bags):
                # ensure subset of data have the correct dimensions and matching rows (samples) for x and y
                data_x_subset[j] = random.choice(data_x)
                data_y_subset[j] = random.choice(data_y)
            # create 'bag' number of learners and store in a list for later reference during query
            learnerInstance = self.learner(**self.kwargs)
            learnerInstance.add_evidence(data_x_subset, data_y_subset)
            self.learners.append(learnerInstance)

    def query(self, points):
        # Call each learner with the list of points
        results = []
        for learner in self.learners:
            result = learner.query(points)
            results.append(result)
        return np.mean(results, axis=0)