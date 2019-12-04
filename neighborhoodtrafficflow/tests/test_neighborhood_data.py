"""Test module for pre-processing Seattle neighborhood datasets"""
import os
import pickle

import pytest

from ..data.neighborhood_data import prep_map_data

# File paths
JSON_PATH = 'neighborhoodtrafficflow/data/raw/' \
        'zillow-neighborhoods/zillow-neighborhoods.geojson'
DATA_PATH = 'nbhd_data.pkl'


def test_prep_data_1():
    """Check that function throws an error if no file at json_path"""

    # Bad file path
    json_path_bad = JSON_PATH + 'bad'

    # Call function
    with pytest.raises(Exception):
        assert prep_map_data(json_path_bad, DATA_PATH)


def test_prep_map_data_2():
    """Check that function creates new data file if none exists"""

    # Delete old data file if exists
    if os.path.exists(DATA_PATH):
        os.remove(DATA_PATH)

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Check that new data file created
    assert os.path.exists(DATA_PATH)

    # Delete new data file
    os.remove(DATA_PATH)


def test_prep_map_data_3():
    """Check format of new data file"""

    # Create new data file
    prep_map_data(JSON_PATH, DATA_PATH)

    # Load new data file
    with open(DATA_PATH, 'rb') as pickle_file:
        nbhd_data = pickle.load(pickle_file)

    # Check data length
    assert len(nbhd_data) == 4

    # Check entry types
    assert isinstance(nbhd_data[0], int)
    assert isinstance(nbhd_data[1], dict)
    assert isinstance(nbhd_data[2], list)
    assert isinstance(nbhd_data[3], list)

    # Check list types
    assert all(isinstance(entry, str) for entry in nbhd_data[2])
    assert all(isinstance(entry, str) for entry in nbhd_data[3])

    # Check some data
    assert nbhd_data[0] == 103
    assert set(nbhd_data[1].keys()) == {'type', 'features'}
    assert nbhd_data[2][0] == '344008'
    assert nbhd_data[3][0] == 'West Woodland'

    # Delete new data file
    os.remove(DATA_PATH)
