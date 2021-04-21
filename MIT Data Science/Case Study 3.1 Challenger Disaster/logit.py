# MIT Data Science - Case Study 3.1 Logistic Regression of Challenger Disaster data

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

data = pd.read_csv(r"MIT Data Science/Case Study 3.1 Challenger Disaster/Data/challenger-data.csv")

# Split data into failures and no failures
failures = data[data.Y == 1]
no_failures = data[data.Y == 0]

failures_freq = failures.X.value_counts()
no_failures_freq = no_failures.X.value_counts()

draw = False

if draw:
    plt.scatter(failures_freq.index, failures_freq, c='red', s=40)
    plt.scatter(no_failures_freq.index, np.zeros(len(no_failures_freq)), c='blue', s=40)
    plt.xlabel('X: Temperature')
    plt.ylabel('Number of Failures')
    plt.show()

import patsy

from patsy import dmatrices
import statsmodels.discrete.discrete_model as sm

y, X = dmatrices('Y ~ X', data, return_type='dataframe')

logit = sm.Logit(y, X)
result = logit.fit()

print(result.summary())

data["f"] = result.predict()
data["F"] = data.f ** 5

res_data = pd.DataFrame()
res_data["T"] = np.arange(0, 80, 1)
res_data["f"] = [result.predict([1, t], None)[0] for t in res_data.T]
res_data["F"] = res_data.f ** 5

plt.plot(res_data["T"], res_data.f)
plt.plot(res_data["T"], res_data.F)
plt.scatter(failures.X, failures.Y, c='red', s=4)
plt.scatter(no_failures.X, no_failures.Y, c='blue', s=4)
plt.show()

if draw:
    plt.scatter(failures_freq.index, failures_freq, c='red', s=40)
    plt.scatter(no_failures_freq.index, np.zeros(len(no_failures_freq)), c='blue', s=40)
    plt.plot(data.X, data.f)
    plt.plot(data.X, data.F)
    plt.xlabel('X: Temperature')
    plt.ylabel('Number of Failures')
    plt.show()

