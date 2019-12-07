"""Test module for generating maps."""
from pathlib import Path
import pickle

import numpy as np
import pytest

from neighborhoodtrafficflow.figures.maps import \
    matplotlib_to_plotly, neighborhood_map

# Import neighborhood data
CWD = Path(__file__).parent
NBHD_PATH = CWD / '../data/cleaned/nbhd_data.pkl'
with open(NBHD_PATH, 'rb') as pickle_file:
    NBHD_DATA = pickle.load(pickle_file)


def test_na_matplotlib_to_plotly():
    """Ensure color map has no nas"""
    colormap = matplotlib_to_plotly('viridis', 255)
    assert np.NaN not in colormap, "There are nas in the colormap"


def test_neighborhoods_neighborhood_map():
    """Ensure function breaks if given wrong neighborhood"""
    with pytest.raises(KeyError):
        neighborhood_map(*NBHD_DATA, selected=200)


def test_parameter_types_neighborhood_map():
    """Ensure function breaks if given wrong type"""
    nbhd_data = NBHD_DATA.copy()
    nbhd_data[0] = "103"
    with pytest.raises(TypeError):
        neighborhood_map(*nbhd_data)