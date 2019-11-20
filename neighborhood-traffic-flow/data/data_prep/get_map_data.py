# Create dataframe for road maps
#
# name: name of road segment
# lon: list of longitude coordinates
# lat: list of latitude coordinates
# nbhd: list of neighborhoods
# type: flow, speed, or art
# year: year of data
# flow: traffic flow counts
# speed: speed limit
# road: road type

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString
from shapely.ops import linemerge

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
def filter_dataframe(df,df_type,name_attr,flow_attr,year):
    
    name_list = []
    lon_list = []
    lat_list = []
    nbhd_list = []
    year_list = []
    flow_list = []
    speed_list = []
    road_list = []
    num_bad = 0

    for idx, row in df.iterrows():

        name = row[name_attr]
        geo = row['geometry']

        if df_type == 'flow': 
            year = year
            flow = row[flow_attr]
            speed = None
            road = None
        else:
            year = None
            flow = None
            road = row['ARTCLASS']
            speed = row['SPEEDLIMIT']

        # merge any MultiLineStrings
        if type(geo) == MultiLineString:
            geo = linemerge(geo)

        # add all LineStrings
        if type(geo) == LineString:

            lon = [x for x,y in geo.coords]
            lat = [y for x,y in geo.coords]
            nbhd = get_neighborhood(lon,lat)

            if len(nbhd) > 0:

                name_list.append(name)
                lon_list.append(lon)
                lat_list.append(lat)
                nbhd_list.append(nbhd)
                year_list.append(year)
                flow_list.append(flow)
                speed_list.append(speed)
                road_list.append(road)
            
        # some will still be MultiLinestrings (streets not contiguous)
        else:
            num_bad += 1
        
    df_filtered = pd.DataFrame(
        data={
            'name': name_list,
            'lon': lon_list,
            'lat': lat_list,
            'nbhd': nbhd_list,
            'year': year_list,
            'flow': flow_list,
            'speed': speed_list,
            'road': road_list
        }
    )
    
    return df_filtered, num_bad

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

# Filter flow dataframes
df_list = []
for year in range(2007,2019):

    df_flow = gpd.read_file('%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year,year))
    df_filtered, num_bad = filter_dataframe(df_flow,'flow',*col_names[year],year)
    df_list.append(df_filtered)
    print('Year:',year,', Bad:',num_bad)

# Filter speed dataframes
df_speed = gpd.read_file('Seattle_Streets/Seattle_Streets.shp')
df_filtered, num_bad = filter_dataframe(df_speed,'speed','STNAME_ORD',None,None)
df_list.append(df_filtered)
print('Speeds, Bad:',num_bad)

# Concatenate dataframes
df_concat = pd.concat(df_list)
df_concat.to_pickle('map_data.pkl')

