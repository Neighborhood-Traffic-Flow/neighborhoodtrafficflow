"""Filter Seattle streets datasets

Load and filter Seattle street datasets into format used by dashboard.

Columns
-------
key : int
    Primary key (COMPKEY) of the street asset table, assigned by the
    Hansen asset management system.
name : str
    Street segment name.
lon : list
    List of street segment longitude coordinates (float).
lat : list
    List of street segment latitude coordinates (float).
speed : float
    Speed limit in MPH.
road : float
    Arterial classification code:
    5 - Interstate Freeway
    4 - State Highway
    3 - Collector Arterial
    2 - Minor Arterial
    1 - Principal Arterial
    0 - Not Designated (not an arterial)
nbhd : list
    List of indices (int) of all neighborhoods that the street segment
    passes through.
2007-2018 : float
    Annual Average Week Day Traffic: derived by averaging 24-hour daily
    traffic volumes for both directions across Monday thru Friday,
    excluding holidays and weekends, then adjusting for seasonal
    variations by applying an annual adjustment factor. This number is
    given in thousands of vehicles.
"""
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon

# Load streets dataset
STREET_DATA = gpd.read_file('Seattle_Streets/Seattle_Streets.shp')

# Load neighborhood dataset
NBHD_DATA = gpd.read_file('zillow-neighborhoods/zillow-neighborhoods.shp')

# Create polygons for each neighborhood
IDX2POLY = {}
for idx, row in NBHD_DATA.iterrows():
    try:
        IDX2POLY[idx] = Polygon(row['geometry'])
    except NotImplementedError:
        IDX2POLY[idx] = MultiPolygon(row['geometry'])


def get_neighborhood(lon, lat):
    """Get street neighborhoods

    Get list of neighborhods that a street segment passes through,
    based on inclusion of the street's (lon,lat) coordinates in
    neighborhood polygons.

    Parameters
    ----------
    lon : list
        List of street segment longitude coordinates (float).
    lat : list
        List of street segment latitude coordinates (float).

    Returns
    -------
    nbhd : list
        List of indices (int) of all neighborhoods that the street segment
        passes through.
    """
    point_list = [Point(lon[i], lat[i]) for i in range(len(lat))]
    nbhd_list = []
    for key in IDX2POLY:
        if np.any([IDX2POLY[key].contains(point) for point in point_list]):
            nbhd_list.append(key)
    return nbhd_list


# Populate lists for key, name, lon, lat, speed, and road
KEY_LIST = []
NAME_LIST = []
LON_LIST = []
LAT_LIST = []
SPEED_LIST = []
ROAD_LIST = []
NBHD_LIST = []
for idx, row in STREET_DATA.iterrows():

    print('Percent done: %.2f' % (100.0*idx/len(STREET_DATA)), end='\r')

    geo = row['geometry']
    lon = [x for x, y in geo.coords]
    lat = [y for x, y in geo.coords]

    KEY_LIST.append(row['COMPKEY'])
    NAME_LIST.append(row['STNAME_ORD'])
    LON_LIST.append(lon)
    LAT_LIST.append(lat)
    SPEED_LIST.append(row['SPEEDLIMIT'])
    ROAD_LIST.append(row['ARTCLASS'])
    NBHD_LIST.append(get_neighborhood(lon, lat))
print()

# Add missing streets from 2007-2014
for year in range(2007, 2015):
    df = gpd.read_file('%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year, year))
    count = 0
    for _, row in df.iterrows():
        if row['COMPKEY'] not in KEY_LIST:
            geo = row['geometry']
            lon = [x for x, y in geo.coords]
            lat = [y for x, y in geo.coords]
            KEY_LIST.append(row['COMPKEY'])
            NAME_LIST.append(row['STNAME'])
            LON_LIST.append(lon)
            LAT_LIST.append(lat)
            SPEED_LIST.append(None)
            ROAD_LIST.append(None)
            NBHD_LIST.append(get_neighborhood(lon, lat))
            count += 1
    print('Year: %d, Added: %d' % (year, count))

# Mapping from FLOWSEGID to COMPKEY
FLOW2KEY = {}
new_key = 800000
DF_LIST = []
YEAR_LIST = []
for year in range(2018, 2014, -1):
    df = gpd.read_file('%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year, year))
    for _, row in df.iterrows():

        # Assign flowseg ids
        if np.isnan(row['FLOWSEGID']):
            row['FLOWSEGID'] = 5000
        else:
            row['FLOWSEGID'] = int(row['FLOWSEGID'])

        # Assign compkeys
        if row['FLOWSEGID'] in FLOW2KEY.keys():
            row['COMPKEY'] = FLOW2KEY[row['FLOWSEGID']]
        else:
            if (year in [2015, 2016]) or (row['COMPKEY'] is None):
                row['COMPKEY'] = str(new_key)
                new_key += 1

            FLOW2KEY[row['FLOWSEGID']] = row['COMPKEY']

    DF_LIST.append(df)
    YEAR_LIST.append(year)

# Add missing streets from 2015-2018
for i, df in enumerate(DF_LIST):
    count = 0
    for _, row in df.iterrows():
        try:
            key_str = FLOW2KEY[row['FLOWSEGID']]
        except KeyError:
            key_str = FLOW2KEY[5000]
        keys = key_str.split(',')
        for key in keys:
            if int(key) not in KEY_LIST:
                geo = row['geometry']
                lon = [x for x, y in geo.coords]
                lat = [y for x, y in geo.coords]
                KEY_LIST.append(int(key))
                if i in [2, 3]:
                    NAME_LIST.append(row['FIRST_STNA'])
                else:
                    NAME_LIST.append(row['STNAME_ORD'])
                LON_LIST.append(lon)
                LAT_LIST.append(lat)
                SPEED_LIST.append(None)
                ROAD_LIST.append(None)
                NBHD_LIST.append(get_neighborhood(lon, lat))
                count += 1
    print('Year: %d, Added: %d' % (YEAR_LIST[i], count))

# Create DataFrame
DF_STREETS = pd.DataFrame(
    data={
        'key': KEY_LIST,
        'name': NAME_LIST,
        'lon': LON_LIST,
        'lat': LAT_LIST,
        'speed': SPEED_LIST,
        'road': ROAD_LIST,
        'nbhd': NBHD_LIST
    }
)

# Mapping from year to flow column name
COL_NAMES = {
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
for year in range(2007, 2015):
    DF_STREETS[str(year)] = None
    df_flow = gpd.read_file('%d_Traffic_Flow_Counts/%d_Traffic_Flow_Counts.shp' % (year, year))
    for _, row in df_flow.iterrows():
        flow = row[COL_NAMES[year]]
        key = row['COMPKEY']
        DF_STREETS.loc[DF_STREETS['key'] == key, str(year)] = flow

# Add flow for 2015-2018
for i, df_flow in enumerate(DF_LIST):
    year = YEAR_LIST[i]
    for _, row in df_flow.iterrows():
        flow = row[COL_NAMES[year]]
        try:
            key_str = FLOW2KEY[row['FLOWSEGID']]
        except KeyError:
            key_str = FLOW2KEY[5000]
        keys = key_str.split(',')
        for key in keys:
            rows = DF_STREETS[DF_STREETS['key'] == int(key)]
            DF_STREETS.loc[DF_STREETS['key'] == int(key), str(year)] = flow

# Save DataFrame
DF_STREETS.to_pickle('flow_new.pkl')
