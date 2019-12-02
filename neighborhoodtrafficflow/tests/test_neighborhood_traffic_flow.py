"""Tests"""
import numpy as np
import importlib

FIGURES = importlib.import_module("neighborhoodtrafficflow.figures")

def test_na_matplotlib_to_plotly():
    """Ensure color map has no nas"""
    colormap = FIGURES.matplotlib_to_plotly('viridis', 255)
    assert np.NaN not in colormap, "There are nas in the colormap"