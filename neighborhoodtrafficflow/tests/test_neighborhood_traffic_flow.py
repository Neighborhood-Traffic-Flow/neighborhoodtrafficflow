"""Test module for functions in figures.py"""
import numpy as np

from neighborhoodtrafficflow.figures import (matplotlib_to_plotly,
                                             neighborhood_map)
import pytest
import pickle
import os

NBHD_PATH = os.path.abspath(os.path.join(
    os.path.dirname("__file__"),
    'neighborhoodtrafficflow/data/cleaned/nbhd_data.pkl'))


# Import neighborhood data
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
