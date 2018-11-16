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

count_ratings = len(raw_data.index)
count_users = len(raw_data.user_id.unique())

plot = ratings.value_counts().sort_index().plot.bar()
for tick in plot.get_xticklabels():
    tick.set_rotation(0)
plot.figure.suptitle("Histogram of Movie Ratings", fontsize=16)
plot.set_ylabel("Number of Users", fontsize=12)



plot.yaxis.grid(True)  # Add gridlines to make it easier gauge the height of the bars
plot.set_ylabel("Number of Users", fontsize=12)
ylims = plot.get_ylim()
miny = ylims[0] / count_ratings
maxy = ylims[1] / count_ratings
yax2 = plot.twinx()
yax2.set_ylim((miny, maxy))  # Set min and max for % scale on secondary Y-axis
yax2.set_ylabel("Percent of Users", fontsize=12)


yax2_labels = ["{:.0f}%".format(label.get_position()[1]*100) for label in list(yax2.get_yticklabels())]
yax2.set_yticklabels(yax2_labels)

#yax2.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(x*100, '{0:.0f}%')))

# X-axis customizations
plot.set_xlabel("Movie Rating\n\n{} Total Ratings from {} Users".format(count_ratings, count_users), fontsize=12)
# plot.figure.tight_layout()

