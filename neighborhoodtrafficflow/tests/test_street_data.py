"""Test module for pre-processing Seattle street datasets."""
import os
from pathlib import Path, PosixPath

import pytest
import numpy as np
from shapely.geometry import Polygon

from neighborhoodtrafficflow.data.street_data import \
    get_polygons, get_neighborhood, get_flow_path, get_flow_data

# File paths
CWD = Path(__file__).parent
SHP_PATH = CWD/'../data/raw/zillow-neighborhoods/' \
           'zillow-neighborhoods.shp'
DATA_PATH = 'street_data.pkl'

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
    assert isinstance(nbhd_list, list)
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
        assert df_list[i].columns[2] == 'flow'
        assert df_list[i].columns[3] == 'name'


def test_get_flow_data_3():
    """Check DataFrame types."""
    _, _, df_list, _ = get_flow_data()
    for i in range(12):
        assert df_list[i].dtypes[0] == object
        assert df_list[i].dtypes[1] == int
        assert df_list[i].dtypes[2] == float
        assert df_list[i].dtypes[3] == object


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
