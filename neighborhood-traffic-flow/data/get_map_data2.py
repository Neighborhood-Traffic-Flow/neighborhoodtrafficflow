
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon
from shapely.geometry.multilinestring import MultiLineString
from shapely.geometry.linestring import LineString
from shapely.ops import linemerge

# Load neighborhood dataset
df_nbhd = gpd.read_file('../zillow-neighborhoods/zillow-neighborhoods.shp')

# Create polygons for each neighborhood
idx2poly = {}
for idx, row in df_nbhd.iterrows():
    try:
        idx2poly[idx] = Polygon(row['geometry'])
    except:
        idx2poly[idx] = MultiPolygon(row['geometry'])
        
# Get neighborhoods
def get_neighborhood(lon,lat):
    point_list = [Point(lon[i],lat[i]) for i in range(len(lat))]
    nbhd_list = []
    for key in idx2poly.keys():
        if np.any([idx2poly[key].contains(point) for point in point_list]):
            nbhd_list.append(key)
    return nbhd_list

# Load streets dataset
streets = gpd.read_file('../Seattle_Streets/Seattle_Streets.shp')

# Create list of key, name, lon, lat, speed, type
key_list = []
name_list = []
lon_list = []
lat_list = []
speed_list = []
road_list = []
nbhd_list = []
for idx, row in streets.iterrows():
    
    print('Percent done: %.2f' % (100.0*idx/len(streets)),end='\r')
    
    geo = row['geometry']
    lon = [x for x,y in geo.coords]
    lat = [y for x,y in geo.coords]
    
    key_list.append(row['COMPKEY'])
    name_list.append(row['STNAME_ORD'])
    lon_list.append(lon)
    lat_list.append(lat)
    speed_list.append(row['SPEEDLIMIT'])
    road_list.append(row['ARTCLASS'])
    nbhd_list.append(get_neighborhood(lon,lat))

# Add missing streets from 2007-2014
print()
for year in range(2007,2015):
    df = gpd.read_file('../%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year,year))
    count = 0
    for idx,row in df.iterrows():
        if row['COMPKEY'] not in key_list:
            geo = row['geometry']
            lon = [x for x,y in geo.coords]
            lat = [y for x,y in geo.coords]
            key_list.append(row['COMPKEY'])
            name_list.append(row['STNAME'])
            lon_list.append(lon)
            lat_list.append(lat)
            speed_list.append(None)
            road_list.append(None)
            nbhd_list.append(get_neighborhood(lon,lat))
            count += 1
    print('Year: %d, Added: %d' % (year,count))

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

# Add missing streets from 2015-2018
for i in range(len(df_list)):
    count = 0
    df = df_list[i]
    for idx,row in df.iterrows():
        try:
            key_str = flow2comp[row['FLOWSEGID']]
        except:
            key_str = flow2comp[5000]
        keys = key_str.split(',')
        for key in keys:
            if int(key) not in key_list:
                geo = row['geometry']
                lon = [x for x,y in geo.coords]
                lat = [y for x,y in geo.coords]
                key_list.append(int(key))
                if i in [2,3]:
                    name_list.append(row['FIRST_STNA'])
                else:
                    name_list.append(row['STNAME_ORD'])
                lon_list.append(lon)
                lat_list.append(lat)
                speed_list.append(None)
                road_list.append(None)
                nbhd_list.append(get_neighborhood(lon,lat))
                count += 1
    print('Year: %d, Added: %d' % (year_list[i],count))

# Save dataframe
df = pd.DataFrame(
    data={
        'key': key_list,
        'name': name_list,
        'lon': lon_list,
        'lat': lat_list,
        'speed': speed_list,
        'road': road_list,
        'nbhd': nbhd_list
    }
)
df.to_pickle('streets_new.pkl')
print(len(df))
