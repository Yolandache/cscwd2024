from __future__ import division
from __future__ import print_function

import time
import numpy as np
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import torch
import torch.nn.functional as F
from time import perf_counter
from model.utils import load_data
np.random.seed(222)

def our_precompute(features, adj, degree):
    t = perf_counter()
    for i in range(degree):
        if i != degree-1:
            features = F.relu(torch.spmm(adj, features))
            # features = F.dropout(features, 0.5)
        elif i == degree-1:
            features = torch.spmm(adj, features)
    precompute_time = perf_counter()-t
    return features, precompute_time


# Load data
adj, features, labels, idx_train, idx_val, idx_test = load_data()

exfeatures, precompute_time = our_precompute(features, adj, 2)

print("{:.4f}s".format(precompute_time))
print(exfeatures.size())


X = exfeatures
Y = labels

print('Model')
scorings = ['accuracy', 'precision', 'recall', 'f1']
dttime = []
for scoring in scorings:
    start = time.process_time()
    clf = DecisionTreeClassifier(criterion='gini')
    scores = cross_val_score(clf, X, Y, cv=5, scoring=scoring)  # cv为迭代次数。
    end = time.process_time()
    dttime.append(end - start)
    # print(scores) 
    print(scoring+": %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
print("Model检测速度：{:.0f}flows/s" .format(X.shape[0]/(5*(np.mean(dttime)+precompute_time))))
