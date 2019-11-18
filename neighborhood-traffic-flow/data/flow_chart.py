# Create dataframe for chart

import pandas as pd

df = pd.read_pickle('flow_map.pkl')

year_list = []
nbhd_list = []
flow_list = []
for year in range(2007,2019):
    for neighborhood in range(103):

        nbhd_idx = df.nbhd.apply(lambda nbhd_list: neighborhood in nbhd_list)
        flow = df[nbhd_idx & (df['year']==year)]
        flows = flow['flow'].to_list()

        year_list.append(year)
        nbhd_list.append(neighborhood)
        flow_list.append(flows)

series = pd.DataFrame({'year': year_list, 'nbhd': nbhd_list, 'flow': flow_list})
series.to_pickle('flow_chart.pkl')

