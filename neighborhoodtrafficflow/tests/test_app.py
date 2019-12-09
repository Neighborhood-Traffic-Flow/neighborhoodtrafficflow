"""Test module for dashboard manager."""
from neighborhoodtrafficflow.app import \
    update_road_map_title, update_flow_count_title, \
    update_speed_limit_title, update_road_type_title, \
    update_dropdown, update_slider, update_neighborhood_map, \
    update_road_map, update_traffic_flow_counts, update_speed_limits, \
    update_road_types


#########################
# update section titles #
#########################

def test_update_road_map_title():
    """Check output string."""
    output = update_road_map_title(0)
    assert output[-23:-4] == 'West Woodland Roads'


def test_update_flow_count_title():
    """Check output string."""
    output = update_flow_count_title(0)
    assert output[-29:-4] == 'West Woodland Flow Counts'


def test_update_speed_limit_title():
    """Test output string."""
    output = update_speed_limit_title(0)
    assert output[-30:-4] == 'West Woodland Speed Limits'


def test_update_road_type_title():
    """Test output string."""
    output = update_road_type_title(0)
    assert output[-28:-4] == 'West Woodland Road Types'


#########################
# update control status #
#########################

def test_default_update_dropdown():
    """Test default output."""
    value = update_dropdown('dummy')
    assert value[-5:-3] == '92'


def test_example_update_dropdown():
    """Test specific example."""
    selected_data = {'points': [{'pointIndex': 0}]}
    value = update_dropdown(selected_data)
    assert value[-4:-3] == '0'


def test_flow_update_slider():
    """Test flow output."""
    output = update_slider('flow')
    assert output[-11:-5] == 'inline'


def test_other_update_slider():
    """Test non-flow output."""
    output = update_slider('dummy')
    assert output[-9:-5] == 'none'


###############
# update maps #
###############

def test_type_update_neighborhood_map():
    """Test output type."""
    figure = update_neighborhood_map(92)
    assert figure[54:70] == 'choroplethmapbox'


def test_type_update_road_map():
    """Test output type."""
    figure = update_road_map(92, 'flow', 2018)
    assert figure[54:63] == 'scattergl'


#################
# update charts #
#################

def test_type_update_traffic_flow_counts():
    """Test output type."""
    figure = update_traffic_flow_counts(92)
    assert figure[54:57] == 'box'


def test_type_update_speed_limits():
    """Test output type."""
    figure = update_speed_limits(92)
    assert figure[54:63] == 'histogram'


def test_type_update_road_types():
    """Test output type."""
    figure = update_road_types(92)
    assert figure[54:63] == 'histogram'
