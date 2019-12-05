"""Tests"""
import numpy as np
from neighborhoodtrafficflow.figures import matplotlib_to_plotly

def test_na_matplotlib_to_plotly():
    """Ensure color map has no nas"""
    colormap = matplotlib_to_plotly('viridis', 255)
    assert np.NaN not in colormap, "There are nas in the colormap"