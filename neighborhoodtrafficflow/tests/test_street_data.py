"""Test module for pre-processing Seattle street datasets."""
import os
from pathlib import Path, PosixPath

import geopandas as gpd
import pandas as pd
import pytest
import numpy as np
from shapely.geometry import Polygon

from neighborhoodtrafficflow.data.street_data import \
    get_polygons, get_neighborhood, get_flow_path, get_flow_data, \
    get_street_data, add_flow_data

# Don't run tests if no updates have been made to street_data.py
pytestmark = pytest.mark.skip("Skipping test_street_data.py")

# File paths
CWD = Path(__file__).parent
SHP_PATH = CWD/'../data/raw/zillow-neighborhoods/' \
           'zillow-neighborhoods.shp'
STREET_PATH = CWD/'../data/raw/Seattle_Streets/Seattle_Streets.shp'

def test_get_polygons_1():
    """Check that function throws an error if no file at shp_path."""

    # Call function
    with pytest.raises(Exception):
        assert get_polygons('dummy.shp')


def test_get_polygons_2():
    """Check length and output types."""
    idx2poly = get_polygons(SHP_PATH)
    assert len(idx2poly) == 103
    assert isinstance(idx2poly, dict)
    assert isinstance(idx2poly[0], Polygon)


def test_get_neighborhood_1():
    """Check output type."""
    lon = [-122.36866107043400]
    lat = [47.66757206792280]
    idx2poly = get_polygons(SHP_PATH)
    nbhd_list = get_neighborhood(lon, lat, idx2poly)
    nbhd_type = set(type(n) for n in nbhd_list)
    assert isinstance(nbhd_list, list)
    assert len(nbhd_type) == 1
    assert isinstance(nbhd_list[0], int)


def test_get_neighborhood_2():
    """Check output of one neighborhood."""
    lon = [-122.36866107043400]
    lat = [47.66757206792280]
    idx2poly = get_polygons(SHP_PATH)
    nbhd_list = get_neighborhood(lon, lat, idx2poly)
    assert len(nbhd_list) == 1
    assert nbhd_list[0] == 0


def test_get_neighborhood_3():
    """Check output of two neighborhoods."""
    lon = [-122.36866107043400, -122.3821835817560]
    lat = [47.66757206792280, 47.69606176398850]
    idx2poly = get_polygons(SHP_PATH)
    nbhd_list = get_neighborhood(lon, lat, idx2poly)
    assert len(nbhd_list) == 2
    assert nbhd_list[0] == 0
    assert nbhd_list[1] == 1


def test_get_flow_path_1():
    """Test output type."""
    path = get_flow_path(2007)
    assert isinstance(path, PosixPath)


def test_get_flow_path_2():
    """Test output value."""
    path = get_flow_path(2007)
    path_str = str(path)
    assert path_str[-28:-4] == '2007_Traffic_Flow_Counts'
    assert os.path.exists(path)


def test_get_flow_data_1():
    """Check length of output."""
    _, _, df_list, year_list = get_flow_data()
    assert len(df_list) == 12
    assert len(year_list) == 12


def test_get_flow_data_2():
    """Check DataFrame columns names."""
    _, _, df_list, _ = get_flow_data()
    for i in range(12):
        assert df_list[i].columns[0] == 'COMPKEY'
        assert df_list[i].columns[1] == 'FLOWSEGID'
        assert df_list[i].columns[2] == 'geometry'
        assert df_list[i].columns[3] == 'flow'
        assert df_list[i].columns[4] == 'name'


def test_get_flow_data_3():
    """Check DataFrame types."""
    _, _, df_list, _ = get_flow_data()
    for i in range(12):
        assert df_list[i].dtypes[0] == object
        assert df_list[i].dtypes[1] == int
        assert df_list[i].dtypes[3] == float
        assert df_list[i].dtypes[4] == object


def test_get_flow_data_4():
    """Check first dictionary."""
    flow2key, _, _, _ = get_flow_data()
    assert isinstance(flow2key, dict)
    key_type = set(type(k) for k in flow2key)
    val_type = set(type(v) for v in flow2key.values())
    assert len(key_type) == 1
    assert len(val_type) == 1
    assert list(key_type)[0] == int
    assert list(val_type)[0] == str


def test_get_flow_data_5():
    """Check second dictionary."""
    _, key2flow, _, _ = get_flow_data()
    assert isinstance(key2flow, dict)
    key_type = set(type(k) for k in key2flow)
    val_type = set(type(v) for v in key2flow.values())
    assert len(key_type) == 1
    assert len(val_type) == 1
    assert list(key_type)[0] == str
    assert list(val_type)[0] == int


def test_get_flow_data_6():
    """Check data consistincy across dictionaries."""
    flow2key, key2flow, _, _ = get_flow_data()
    for key in key2flow:
        flow = key2flow[key]
        assert key in flow2key[flow].split(',')
    for flow in flow2key:
        keys = flow2key[flow]
        for key in keys.split(','):
            assert key2flow[key] == flow


def test_get_flow_data_7():
    """Check year list."""
    _, _, _, year_list = get_flow_data()
    assert year_list == list(np.arange(2018, 2006, -1))


def test_get_street_data_1():
    """Check output types."""
    # Initialize lists for street data
    key_list = []
    name_list = []
    lon_list = []
    lat_list = []
    speed_list = []
    road_list = []
    nbhd_list = []

    # Get street data
    idx2poly = get_polygons(SHP_PATH)
    df = gpd.read_file(get_flow_path(2007))
    get_street_data(df, 2007, idx2poly, key_list, name_list, lon_list,
                    lat_list, speed_list, road_list, nbhd_list)

    # Get types
    key_type = set(type(k) for k in key_list)
    name_type = set(type(n) for n in name_list)
    lon_type = set(type(l) for l in lon_list)
    lat_type = set(type(l) for l in lat_list)
    speed_type = set(type(s) for s in speed_list)
    road_type = set(type(r) for r in road_list)
    nbhd_type = set(type(n) for n in nbhd_list)

    # Check number of types
    assert len(key_type) == 1
    assert len(name_type) == 1
    assert len(lon_type) == 1
    assert len(lat_type) == 1
    assert len(speed_type) == 1
    assert len(road_type) == 1
    assert len(nbhd_type) == 1

    # Check types
    assert list(key_type)[0] == int
    assert list(name_type)[0] == str
    assert list(lon_type)[0] == list
    assert list(lat_type)[0] == list
    assert list(speed_type)[0] == int
    assert list(road_type)[0] == int
    assert list(nbhd_type)[0] == list


def test_get_street_data_2():
    """Check modify in place."""
    # Initialize lists for street data
    key_list = []
    name_list = []
    lon_list = []
    lat_list = []
    speed_list = []
    road_list = []
    nbhd_list = []

    # Get street data
    idx2poly = get_polygons(SHP_PATH)
    df = gpd.read_file(get_flow_path(2007))
    get_street_data(df, 2007, idx2poly, key_list, name_list, lon_list,
                    lat_list, speed_list, road_list, nbhd_list)

    # Check length
    assert len(key_list) > 0
    assert len(name_list) > 0
    assert len(lon_list) > 0
    assert len(lat_list) > 0
    assert len(speed_list) > 0
    assert len(road_list) > 0
    assert len(nbhd_list) > 0


def test_get_street_data_3():
    """Check range of output."""
    # Initialize lists for street data
    key_list = []
    name_list = []
    lon_list = []
    lat_list = []
    speed_list = []
    road_list = []
    nbhd_list = []

    # Get street data
    idx2poly = get_polygons(SHP_PATH)
    df = gpd.read_file(STREET_PATH)
    get_street_data(df, 'street', idx2poly, key_list, name_list, lon_list,
                    lat_list, speed_list, road_list, nbhd_list)

    # Check range
    assert min(speed_list) >= -1
    assert max(speed_list) <= 60
    assert min(road_list) >= 0
    assert max(road_list) <= 5


def test_add_flow_data():
    """Check final DataFrame."""
     # Get neighborhood polygons
    idx2poly = get_polygons(SHP_PATH)

    # Get mapping from FLOWSEGID to COMPKEY
    flow2key, _, df_list, year_list = get_flow_data()

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
    get_street_data(df, 'street', idx2poly, key_list, name_list, lon_list,
                    lat_list, speed_list, road_list, nbhd_list)

    # Get street data from Traffic Flow Counts datasets
    for i in range(len(df_list)-1, -1, -1):
        get_street_data(df_list[i], year_list[i], idx2poly, key_list,
                        name_list, lon_list, lat_list, speed_list, road_list,
                        nbhd_list)

    # Create initial DataFrame
    df_streets = pd.DataFrame(
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

    # Add traffic flow data
    for i in range(len(df_list)-1, -1, -1):
        add_flow_data(df_streets, df_list[i], year_list[i], flow2key)

    # Check column names and types
    name_list = ['key', 'name', 'lon', 'lat', 'speed', 'road', 'nbhd']
    type_list = [int, object, list, list, int, int, list]
    for i in range(7):
        assert df_streets.columns[i] == name_list[i]
        assert df_streets.dtypes[i] == type_list[i]
    for year in range(2007, 2019):
        assert df_streets.columns[year-2000] == str(year)
        assert df_streets.dtypes[year-2000] == int

    # Check values
    for year in range(2007, 2019):
        assert max(df_streets[str(year)].to_list()) > -1
        assert max(df_streets[str(year)].to_list()) > -1
