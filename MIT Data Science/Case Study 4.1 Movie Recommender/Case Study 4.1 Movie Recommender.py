# MIT Data Science - Case Study 4.1 Movie Recommender

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from surprise import Dataset, SVD, NormalPredictor, BaselineOnly, KNNBasic, NMF
from surprise.model_selection import cross_validate, KFold

data = Dataset.load_builtin()

data_file = data.ratings_file

raw_data = pd.read_table(data_file, names=['user_id', 'item_id', 'rating', 'timestamp'])

ratings = raw_data.rating

ratings.value_counts().sort_index().plot.bar()

hist = ratings.value_counts()



plot = ratings.value_counts().sort_index().plot.bar()
for tick in plot.get_xticklabels():
    tick.set_rotation(0)
plot.figure.suptitle("Histogram of Movie Ratings", fontsize=16)
plot.set_xlabel("Movie Rating", fontsize=12)
plot.set_ylabel("Number of Users", fontsize=12)



