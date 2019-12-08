"""Test module for pre-processing Seattle neighborhood datasets."""
import os
from pathlib import Path
import pickle

import pandas as pd
import pytest

from neighborhoodtrafficflow.data.neighborhood_data import \
    prep_map_data, prep_map_info

# Don't run tests if no updates have been made to neighborhood_data.py
#pytestmark = pytest.mark.skip("Skipping test_neighborhood_data.py")

# File paths
CWD = Path(__file__).parent
JSON_PATH = CWD / '../data/raw/zillow-neighborhoods/' \
    'zillow-neighborhoods.geojson'
SHP_PATH = CWD / '../data/raw/zillow-neighborhoods/' \
    'zillow-neighborhoods.shp'
DATA_PATH = 'nbhd_data.pkl'
INFO_PATH = 'nbhd_info.csv'


#############
# prep_data #
#############

def test_no_file_prep_map_data_():
    """Check that function throws an error if no file at json_path."""

    # Call function
    with pytest.raises(Exception):
        assert prep_map_data('dummy.geojson', DATA_PATH)

def test_create_file_prep_map_data():
    """Check that function creates new data file if none exists."""

    # Delete old data file if exists
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Check that new data file created
    assert os.path.exists(DATA_PATH)

    # Delete new data file
    os.remove(DATA_PATH)

def test_output_length_prep_map_data():
    """Check length of new data file."""

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Load new data file
    with open(DATA_PATH, 'rb') as pickle_file:
        nbhd_data = pickle.load(pickle_file)

    # Check data length
    assert len(nbhd_data) == 4

    # Delete new data file
    os.remove(DATA_PATH)

def test_column_types_prep_map_data():
    """Check column types of new file."""

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Load new data file
    with open(DATA_PATH, 'rb') as pickle_file:
        nbhd_data = pickle.load(pickle_file)

    # Check entry types
    correct_types = [int, dict, list, list]
    for i in range(4):
        assert isinstance(nbhd_data[i], correct_types[i])

    # Check list types
    assert all(isinstance(entry, str) for entry in nbhd_data[2])
    assert all(isinstance(entry, str) for entry in nbhd_data[3])

    # Delete new data file
    os.remove(DATA_PATH)

def test_entries_prep_map_data():
    """Check some entries of new data file."""

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Load new data file
    with open(DATA_PATH, 'rb') as pickle_file:
        nbhd_data = pickle.load(pickle_file)

    # Check some data
    assert nbhd_data[0] == 103
    assert set(nbhd_data[1].keys()) == {'type', 'features'}
    assert nbhd_data[2][0] == '344008'
    assert nbhd_data[3][0] == 'West Woodland'

    # Delete new data file
    os.remove(DATA_PATH)


#############
# prep_info #
#############

def test_no_file_prep_info():
    """Check that function throws an error if no file at shp_path."""

    # Call function
    with pytest.raises(Exception):
        assert prep_map_data('dummy.shp', INFO_PATH)

def test_create_file_prep_map_info():
    """Check that function creates new data file if none exists."""

    # Delete old data file if exists
    if os.path.exists(INFO_PATH):
        os.remove(INFO_PATH)

    # Create new data file
    prep_map_info(SHP_PATH, INFO_PATH)

    # Check that new data file created
    assert os.path.exists(INFO_PATH)

    # Delete new data file
    os.remove(INFO_PATH)

def test_output_length_prep_map():
    """Check length of new data file."""

    # Create new data file
    prep_map_info(SHP_PATH, INFO_PATH)

    # Load new data file
    nbhd_info = pd.read_csv(INFO_PATH)

    # Check data length
    assert len(nbhd_info) == 103

    # Delete new data file
    os.remove(INFO_PATH)

def test_column_types_prep_map_info():
    """Check column types of new data file."""

    # Create new data file
    prep_map_info(SHP_PATH, INFO_PATH)

    # Load new data file
    nbhd_info = pd.read_csv(INFO_PATH)

    # Check column types
    types = nbhd_info.dtypes.to_list()
    for i in range(7):
        if i == 0:
            assert types[i] == object
        else:
            assert types[i] == float

    # Delete new data file
    os.remove(INFO_PATH)

def test_column_names_prep_map_info():
    """Check column names of new data file."""

    # Create new data file
    prep_map_info(SHP_PATH, INFO_PATH)

    # Load new data file
    nbhd_info = pd.read_csv(INFO_PATH)

    # Check column names
    columns = nbhd_info.columns.to_list()
    assert columns == ['name', 'minLon', 'midLon', 'maxLon', 'minLat',
                       'midLat', 'maxLat']

    # Delete new data file
    os.remove(INFO_PATH)

def test_entries_prep_map_info():
    """Check some entries of new data file."""

    # Create new data file
    prep_map_info(SHP_PATH, INFO_PATH)

    # Load new data file
    nbhd_info = pd.read_csv(INFO_PATH)

    # Check some data
    row_one = ['West Woodland', -122.37648625599986,
               -122.36866107043352, -122.36075799399993,
               47.65533747300008, 47.66757206792284, 47.67599213900007]
    assert nbhd_info.loc[0].to_list() == row_one

    # Delete new data file
    os.remove(INFO_PATH)
