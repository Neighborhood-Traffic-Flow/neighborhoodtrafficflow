"""Load Seattle street datasets and reformat for dashboard."""
import os
from pathlib import Path

import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon, MultiPolygon

# File paths
CWD = Path(__file__).parent
STREET_PATH = CWD/'raw/Seattle_Streets/Seattle_Streets.shp'

# Mapping from dataset to street column name
STREET_NAMES = {
    'street': 'STNAME_ORD',
    2007: 'STNAME',
    2008: 'STNAME',
    2009: 'STNAME',
    2010: 'STNAME',
    2011: 'STNAME',
    2012: 'STNAME',
    2013: 'STNAME',
    2014: 'STNAME',
    2015: 'FIRST_STNA',
    2016: 'FIRST_STNA',
    2017: 'STNAME_ORD',
    2018: 'STNAME_ORD',
}

# Mapping from year to flow column name
FLOW_NAMES = {
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

def get_polygons(shp_path):
    """Get dictionary of neighborhood polygons.

    Parameters
    ----------
    shp_path : str
        Path to neighborhood shp file.

    Returns
    -------
    IDX2POLY : dict
        Mapping from neighborhood index to polygon.

    Raises
    ------
    FileNotFoundError : No such file or directory
        If file at shp_path does not exist.
    """
    # Import neighborhood shape file
    nbhd_data = gpd.read_file(shp_path)

    # Create mapping from neighborhood index to polygon
    idx2poly = {}
    for idx, row in nbhd_data.iterrows():
        try:
            idx2poly[idx] = Polygon(row['geometry'])
        except NotImplementedError:
            idx2poly[idx] = MultiPolygon(row['geometry'])
    return idx2poly


def get_neighborhood(lon, lat, idx2poly):
    """Get neighborhoods that street passes through.

    Get list of neighborhods that a street segment passes through,
    based on inclusion of the street's (lon, lat) coordinates in
    neighborhood polygons.

    Parameters
    ----------
    lon : list
        List of street segment longitude coordinates (float).
    lat : list
        List of street segment latitude coordinates (float).
    idx2poly : dict
        Mapping from neighborhood index to polygon.

    Returns
    -------
    nbhd : list
        List of indices (int) of all neighborhoods that the street
        segment passes through.
    """
    point_list = [Point(lon[i], lat[i]) for i in range(len(lat))]
    nbhd_list = []
    for key in idx2poly:
        if np.any([idx2poly[key].contains(point) for point in point_list]):
            nbhd_list.append(key)
    return nbhd_list


def get_flow_path(year):
    """Format path to current traffic flow dataset."""
    name = '%d_Traffic_Flow_Counts' % year
    path = 'raw/' + name + '/' + name + '.shp'
    return CWD/path


def get_flow_data():
    """Load and format traffic flow datasets.

    Load Traffic Flow Count datasets for 2007-2018 and populate
    mappings between FLOWSEGIDs and COMPKEYS used to merge datasets:
    - Seattle Streets has unique COMPKEY (int)
    - 2007-2014 has unique COMPKEY (int)
    - 2015-2016 has unique FLOWSEGID (float)
    - 2017-2018 has unique FLOWSEGID (int) and list of COMPKEYS (str)

    Returns
    -------
    flow2key : dict
        Mapping from FLOWSEGID (int) to COMPKEY (str).
        COMPKEY string may contain a list of COMPKEYS.
    key2flow : dict
        Mapping from COMPKEY (str) to FLOWSEGID (int).
    df_list :
        List of reformatted traffic flow DataFrames.
    year_list :
        Years corresponding to the DataFrames in df_list.
    """
    # Initialize structures
    flow2key = {}
    key2flow = {}
    new_compkey = 1e6
    df_list = []
    year_list = []

    # Iterate backwards through traffic flow datasets
    for year in range(2018, 2006, -1):
        df = gpd.read_file(get_flow_path(year))
        for idx, row in df.iterrows():

            # pylint has a lot of complaints about this function, since
            # it is a bit overkill in terms of conditionals and type
            # casting, etc., but I'm prioritizing other things for now.

            if year in [2017, 2018]:

                # All rows have a FLOWSEGID
                # 14 rows missing a COMPKEY, same roads for both years
                if row['COMPKEY'] is None:
                    if row['FLOWSEGID'] not in flow2key:
                        df.at[idx, 'COMPKEY'] = str(new_compkey)
                        flow2key[row['FLOWSEGID']] = str(new_compkey)
                        key2flow[str(new_compkey)] = row['FLOWSEGID']
                        new_compkey += 1
                    else:
                        df.at[idx, 'COMPKEY'] = flow2key[row['FLOWSEGID']]
                # COMPKEYs can be lists
                else:
                    keys = row['COMPKEY'].split(',')
                    for key in keys:
                        if key not in key2flow:
                            key2flow[key] = row['FLOWSEGID']
                    if row['FLOWSEGID'] not in flow2key:
                        flow2key[row['FLOWSEGID']] = row['COMPKEY']
                    # 2017 has an additional COMPKEY for this FLOWSEGID
                    if row['FLOWSEGID'] == 604:
                        flow2key[row['FLOWSEGID']] = row['COMPKEY']

            if year in [2015, 2016]:

                # One row missing a FLOWSEGID, same for both years
                if np.isnan(row['FLOWSEGID']):
                    df.at[idx, 'FLOWSEGID'] = 1e6
                    row['FLOWSEGID'] = 1e6

                # No rows have a COMPKEY
                if int(row['FLOWSEGID']) not in flow2key:
                    df.at[idx, 'COMPKEY'] = str(new_compkey)
                    flow2key[int(row['FLOWSEGID'])] = str(new_compkey)
                    key2flow[str(new_compkey)] = int(row['FLOWSEGID'])
                    new_compkey += 1
                else:
                    df.at[idx, 'COMPKEY'] = flow2key[int(row['FLOWSEGID'])]

            if year < 2015:

                # All rows have a unique COMPKEY
                if str(row['COMPKEY']) not in key2flow:
                    df.at[idx, 'FLOWSEGID'] = -1
                # No rows have a FLOWSEGID
                else:
                    df.at[idx, 'FLOWSEGID'] = key2flow[str(row['COMPKEY'])]

        # Reformate DataFrame and store in list
        df = df[['COMPKEY', 'FLOWSEGID',
                FLOW_NAMES[year], STREET_NAMES[year]]]
        df = df.rename(columns={FLOW_NAMES[year]: 'flow',
                       STREET_NAMES[year]: 'name'})
        df = df.astype({'COMPKEY': 'str', 'FLOWSEGID': 'int64',
                        'flow': 'float'})
        df_list.append(df)
        year_list.append(year)

    return flow2key, key2flow, df_list, year_list


def get_street_data(df, df_name, idx2poly, key_list, name_list,
                    lon_list, lat_list, speed_list, road_list, nbhd_list):
    """get street data

    Returns
    -------
    out : None
        Modifies the input lists in place. (hopefully)
    """
    print('\nDataset: %s' % df_name)

    # Populate lists for street data
    count = 0
    for idx, row in df.iterrows():

        print('Percent done: %.2f' % (100.0*idx/len(df)), end='\r')

        row['COMPKEY'] = str(row['COMPKEY'])
        for key in row['COMPKEY'].split(','):
            if key not in key_list:

                # Get geometry
                geo = row['geometry']
                lon = [x for x, y in geo.coords]
                lat = [y for x, y in geo.coords]

                # Add info in all datasets
                key_list.append(row['COMPKEY'])
                name_list.append(row[STREET_NAMES[df_name]])
                lon_list.append(lon)
                lat_list.append(lat)
                nbhd_list.append(get_neighborhood(lon, lat, idx2poly))

                count += 1

                # Add info only in street dataset
                if df_name == 'street':
                    speed_list.append(row['SPEEDLIMIT'])
                    road_list.append(row['ARTCLASS'])
                else:
                    speed_list.append(None)
                    road_list.append(None)

    print('Added %d road segments' % count)


if __name__ == '__main__':
    # Create directory for cleaned data if none exists
    if not os.path.exists('cleaned'):
        os.mkdir('cleaned')

    # Get neighborhood polygons
    shp_path = 'raw/zillow-neighborhoods/zillow-neighborhoods.shp'
    IDX2POLY = get_polygons(shp_path)

    # Get mapping from FLOWSEGID to COMPKEY
    FLOW2KEY, KEY2FLOW, DF_LIST, YEAR_LIST = get_flow_data()

    # Initialize lists for street data
    key_list = []
    name_list = []
    lon_list = []
    lat_list = []
    speed_list = []
    road_list = []
    nbhd_list = []

    # Get street data from Seattle Streets dataset
    df = gpd.read_file(STREET_PATH)
    get_street_data(df, 'street', IDX2POLY, key_list, name_list,
                    lon_list, lat_list, speed_list, road_list, nbhd_list)
    print(len(key_list))

    # Get street data from Traffic Flow Counts datasets
    for i in range(len(DF_LIST)-1, -1, -1):
        get_street_data(DF_LIST[i], YEAR_LIST[i], IDX2POLY, key_list,
                        name_list, lon_list, lat_list, speed_list, road_list,
                        nbhd_list)
        print(len(key_list))

    # Create initial DataFrame
    DF_STREETS = pd.DataFrame(
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

    DF_STREETS.to_pickle('temp_street.pkl')

    # Write add_flow_data()
    # Save dataframe
