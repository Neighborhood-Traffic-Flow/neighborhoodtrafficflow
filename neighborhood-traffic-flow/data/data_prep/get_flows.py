
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString
from shapely.ops import linemerge

df_streets = pd.read_pickle('streets_new.pkl')

# flow names by year
col_names = {
    2007: 'AAWDT',
    2008: 'AAWDT',
    2009: 'AAWDT',
    2010: 'AAWDT',
    2011: 'AAWDT',
    2012: 'AAWDT',
    2013: 'AAWDT',
    2014: 'AAWDT',
    2015: 'COUNTAAWDT',
    2016: 'COUNTAAWDT',
    2017: 'AWDT',
    2018: 'AWDT'
}

# Add flow for 2007-2014
for year in range(2007,2015):
    df_flow = gpd.read_file('../%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year,year))
    df_streets[str(year)] = None
    for idx,row in df_flow.iterrows():
        flow = row[col_names[year]]
        key = row['COMPKEY']
        df_streets.loc[df_streets['key']==key,str(year)] = flow

# Mapping from FLOWSEGID to COMPKEY
flow2comp = {}
compkey = 800000
df_list = []
year_list = []
for year in range(2018,2014,-1):
    df = gpd.read_file('../%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year,year))
    for idx,row in df.iterrows():

        # Assign flowseg ids
        if np.isnan(row['FLOWSEGID']):
            row['FLOWSEGID'] = 5000 
        else:
            row['FLOWSEGID'] = int(row['FLOWSEGID'])

        # Assign compkeys
        if row['FLOWSEGID'] in flow2comp.keys():
            row['COMPKEY'] = flow2comp[row['FLOWSEGID']]
        else:
            if (year in [2015,2016]) or (row['COMPKEY'] == None):
                row['COMPKEY'] = str(compkey)
                compkey += 1
            
            flow2comp[row['FLOWSEGID']] = row['COMPKEY']

    df_list.append(df)
    year_list.append(year)

# Add flow for 2015-2018
for i in range(len(df_list)):
    df_flow = df_list[i]
    year = year_list[i]
    for idx,row in df_flow.iterrows():
        flow = row[col_names[year]]
        try:
            key_str = flow2comp[row['FLOWSEGID']]
        except:
            key_str = flow2comp[5000]
        keys = key_str.split(',')
        for key in keys:
            rows = df_streets[df_streets['key']==int(key)]
            if len(rows) < 1:
                print('no for key',key)
            elif len(rows) > 1:
                print(len(rows),'for key',key)
            df_streets.loc[df_streets['key']==int(key),str(year)] = flow

# Save
df_streets.to_pickle('flow_new.pkl')
