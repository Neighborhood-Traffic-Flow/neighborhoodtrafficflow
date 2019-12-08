"""Test module for generating maps."""
from pathlib import Path
import pickle

import numpy as np
import pytest

from neighborhoodtrafficflow.figures.maps import \
    matplotlib_to_plotly, neighborhood_map, road_map, road_color, \
    hover_text

# Import neighborhood data
CWD = Path(__file__).parent
NBHD_PATH = CWD / '../data/cleaned/nbhd_data.pkl'
with open(NBHD_PATH, 'rb') as pickle_file:
    NBHD_DATA = pickle.load(pickle_file)


########################
# matplotlib_to_plotly #
########################

def test_viridis_matplotlib_to_plotly():
    "Test output of viridis colormap for traffic flow."
    colormap = matplotlib_to_plotly('viridis', 255)
    assert np.nan not in colormap
    assert colormap[0][0] == 0.0
    assert colormap[-1][0] == 1.0
    assert colormap[0][1] == 'rgb(0.267004,0.004874,0.329415)'
    assert colormap[-1][1] == 'rgb(0.983868,0.904867,0.136897)'

def test_RdYlGn_matplotlib_to_plotly():
    "Test output of RdYlGn_r colormap for speed limit."
    colormap = matplotlib_to_plotly('RdYlGn_r', 255)
    assert np.nan not in colormap
    assert colormap[0][0] == 0.0
    assert colormap[-1][0] == 1.0
    assert colormap[0][1] == 'rgb(0.000000,0.407843,0.215686)'
    assert colormap[-1][1] == 'rgb(0.654748,0.007382,0.149173)'

def test_tab10_matplotlib_to_plotly():
    """Test output of tab10 colormap for road type."""
    colormap = matplotlib_to_plotly('tab10', 6)
    assert np.nan not in colormap
    assert colormap[0][0] == 0.0
    assert colormap[-1][0] == 1.0
    assert colormap[0][1] == 'rgb(0.121569,0.466667,0.705882)'
    assert colormap[-1][1] == 'rgb(0.549020,0.337255,0.294118)'


####################
# neighborhood_map #
####################

def test_range_neighborhood_map():
    """Ensure function breaks if given wrong neighborhood."""
    with pytest.raises(KeyError):
        neighborhood_map(*NBHD_DATA, selected=200)

def test_parameter_types_neighborhood_map():
    """Ensure function breaks if given wrong type."""
    nbhd_data = NBHD_DATA.copy()
    nbhd_data[0] = "103"
    with pytest.raises(TypeError):
        neighborhood_map(*nbhd_data)

# Parameters: num, data, region_ids, names, selected
# Check errors if input bad
# Check output type
# Check a specific example (centroid, selected)


############
# road_map #
############

# Parameters: data_frame, neighborhood, map_type, year
# Check errors input bad
# Check output type
# Check a specific example (centroid, colormap, legend items for road, title)


##############
# road_color #
##############

def test_flow_road_color():
    """Check values of flow count colors."""
    assert road_color(None, 'flow') == 'rgb(192,192,192)'
    assert road_color(-1, 'flow') == 'rgb(192,192,192)'
    assert road_color(0, 'flow') == 'rgb(0.267004,0.004874,0.329415)'
    assert road_color(108179, 'flow') == 'rgb(0.993248,0.906157,0.143936)'

def test_speed_road_color():
    """Check values of speed limit colors."""
    assert road_color(None, 'speed') == 'rgb(192,192,192)'
    assert road_color(-1, 'speed') == 'rgb(192,192,192)'
    assert road_color(0, 'speed') == 'rgb(0.000000,0.407843,0.215686)'
    assert road_color(60, 'speed') == 'rgb(0.647059,0.000000,0.149020)'

def test_road_road_color():
    """Check max an min values of road type colors."""
    assert road_color(None, 'road') == 'rgb(192,192,192)'
    assert road_color(-1, 'road') == 'rgb(192,192,192)'
    assert road_color(0, 'road') == 'rgb(0.121569,0.466667,0.705882)'
    assert road_color(5, 'road') == 'rgb(0.549020,0.337255,0.294118)'


##############
# hover_text #
##############

def test_flow_hover_text():
    """Check output for flow hover text."""
    assert hover_text('Dummy', -1, 'flow') == 'Dummy, Flow Count: Unknown'
    assert hover_text('Dummy', 10, 'flow') == 'Dummy, Flow Count: 10'

def test_speed_hover_text():
    """Check output for speed hover text."""
    assert hover_text('Dummy', -1, 'speed') == 'Dummy, Speed Limit: Unknown'
    assert hover_text('Dummy', 10, 'speed') == 'Dummy, Speed Limit: 10mph'

def test_road_hover_text():
    """Check output for road hover text."""
    road_type = {
        0: 'Not Designated',
        1: 'Principal Arterial',
        2: 'Minor Arterial',
        3: 'Collector Arterial',
        4: 'State Highway',
        5: 'Interstate Freeway'
    }
    for i in road_type:
        text = 'Dummy, Road Type: ' + road_type[i]
        test_text = hover_text('Dummy', i, 'road')
        assert test_text == text
