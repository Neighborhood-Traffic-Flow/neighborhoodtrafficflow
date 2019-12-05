"""Test module for pre-processing Seattle street datasets."""
from pathlib import Path

import pytest
from shapely.geometry import Polygon

from neighborhoodtrafficflow.data.street_data import \
    get_polygons

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
    """Check output."""
    idx2poly = get_polygons(SHP_PATH)
    assert len(idx2poly) == 103
    assert isinstance(idx2poly, dict)
    assert isinstance(idx2poly[0], Polygon)
