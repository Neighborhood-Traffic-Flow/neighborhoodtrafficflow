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

# Get neighborhoods
def get_neighborhood(lon,lat):
    
    point_list = [Point(lon[i],lat[i]) for i in range(len(lat))]
    nbhd_list = []
    for key in idx2poly.keys():
        if np.any([idx2poly[key].contains(point) for point in point_list]):
            nbhd_list.append(key)
    return nbhd_list

# Load speed limit dataset
df = gpd.read_file('Seattle_Streets/Seattle_Streets.shp')

# Filter dataframe
name_list = []
lon_list = []
lat_list = []
nbhd_list = []
art_list = []
speed_list = []
bad_list = []

for idx, row in df.iterrows():

    name = row['STNAME_ORD']
    geo = row['geometry']
    art = row['ARTCLASS']
    speed = row['SPEEDLIMIT']

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
        art_list.append(art)
        speed_list.append(speed)
        nbhd_list.append(nbhd)

    # some will still be MultiLinestrings (streets not contiguous)
    else:
        bad_list.append(idx)
    
# Create new dataframe
df_filtered = pd.DataFrame(data={'name': name_list,
                            'lon': lon_list,
                            'lat': lat_list,
                            'art': art_list,
                            'speed': speed_list,
                            'nbhd': nbhd_list})


# Save dataframe
df_filtered.to_pickle('speed_map.pkl')

