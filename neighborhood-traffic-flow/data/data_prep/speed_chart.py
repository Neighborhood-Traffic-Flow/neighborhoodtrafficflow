# Create dataframe for chart

import pandas as pd

df = pd.read_pickle('speed_map.pkl')

nbhd_list = []
art_list = []
speed_list = []
for neighborhood in range(103):

    nbhd_idx = df.nbhd.apply(lambda nbhd_list: neighborhood in nbhd_list)
    art = df[nbhd_idx]
    arts = art['art'].to_list()
    speed = df[nbhd_idx]
    speeds = speed['speed'].to_list()

    nbhd_list.append(neighborhood)
    art_list.append(arts)
    speed_list.append(speeds)

series = pd.DataFrame({'nbhd': nbhd_list, 'art': art_list, 'speed': speed_list})
series.to_pickle('speed_chart.pkl')

