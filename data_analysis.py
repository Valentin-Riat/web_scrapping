import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

# load data set
data_matrix = np.load("data_matrix.npy")
data = pd.DataFrame(data_matrix,
                     columns=["uni_name","points", "nb compet","first year"],
                     index=np.arange(1,280,1))

data = data.astype({'uni_name':'str', 'points':'float32', 'nb compet':'int32', 'first year':'int32'})

# get values for our team
epflrt = data[data["uni_name"] == "École Polytechnique Fédérale de Lausanne"]
our_index = epflrt.index[0]
our_nb_compet = epflrt["nb compet"].values[0]
our_first_year = epflrt["first year"].values[0]
our_points = epflrt["points"].values[0]

print(2023-our_first_year)

better_teams = data[data.index < our_index]
print(better_teams)

newest_better_team = better_teams[better_teams["first year"] == better_teams.max()["first year"]]
print("newest team : {}".format(better_teams.max()["first year"]))

mean = data.mean()
print(data.mean())
print(data.sort_values(by="first year", ascending=False))

print("---- Done ----")