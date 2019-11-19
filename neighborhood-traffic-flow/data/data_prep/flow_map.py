# Clean traffic flow count datasets

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.ops import linemerge
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString

# Load neighborhood dataset
df_nbhd = gpd.read_file('zillow-neighborhoods/zillow-neighborhoods.shp')

# Create polygons for each neighborhood
idx2poly = {}
for idx, row in df_nbhd.iterrows():
    try:
        idx2poly[idx] = Polygon(row['geometry'])
    except:
        idx2poly[idx] = MultiPolygon(row['geometry'])

# Filter dataframe
def filter_dataframe(df,name_attr,flow_attr,year):
    
    name_list = []
    lon_list = []
    lat_list = []
    nbhd_list = []
    year_list = []
    flow_list = []
    bad_list = []

    for idx, row in df.iterrows():

        name = row[name_attr]
        geo = row['geometry']
        year = year
        flow = row[flow_attr]

        # merge any MultiLineStrings
        if type(geo) == MultiLineString:
            geo = linemerge(geo)

        # add all LineStrings
        if type(geo) == LineString:

            lon = [x for x,y in geo.coords]
            lat = [y for x,y in geo.coords]
            nbhd = get_neighborhood(lon,lat)

            name_list.append(name)
            lon_list.append(lon)
            lat_list.append(lat)
            year_list.append(year)
            flow_list.append(flow)
            nbhd_list.append(nbhd)

        # some will still be MultiLinestrings (streets not contiguous)
        else:
            bad_list.append(idx)
        
    df_filtered = pd.DataFrame(data={'name': name_list,
                                'lon': lon_list,
                                'lat': lat_list,
                                'year': year_list,
                                'flow': flow_list,
                                'nbhd': nbhd_list})
    
    return df_filtered, bad_list

# Get neighborhoods
def get_neighborhood(lon,lat):
    
    point_list = [Point(lon[i],lat[i]) for i in range(len(lat))]
    nbhd_list = []
    for key in idx2poly.keys():
        if np.any([idx2poly[key].contains(point) for point in point_list]):
            nbhd_list.append(key)
    return nbhd_list

# Column names by year
col_names = {
    2007: ['STNAME','AAWDT'],
    2006: ['STNAME','AAWDT'],
    2008: ['STNAME','AAWDT'],
    2009: ['STNAME','AAWDT'],
    2010: ['STNAME','AAWDT'],
    2011: ['STNAME','AAWDT'],
    2012: ['STNAME','AAWDT'],
    2013: ['STNAME','AAWDT'],
    2014: ['STNAME','AAWDT'],
    2015: ['FIRST_STNA', 'COUNTAAWDT'],
    2016: ['FIRST_STNA', 'COUNTAAWDT'],
    2017: ['STNAME_ORD','AWDT'],
    2018: ['STNAME_ORD','AWDT']
}

# Filter dataframes
df_list = []
for year in range(2007,2019):

    df_flow = gpd.read_file('%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year,year))
    df_filtered, bad_list = filter_dataframe(df_flow,*col_names[year],year)
    df_list.append(df_filtered)
    print('Year:',year,', Bad:',len(bad_list))

# Concatenate dataframes
df_concat = pd.concat(df_list)
df_concat.to_pickle('flow_map.pkl')

