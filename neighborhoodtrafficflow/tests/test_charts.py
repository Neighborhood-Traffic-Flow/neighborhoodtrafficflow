"""Test module for generating charts."""
import pytest

from neighborhoodtrafficflow.figures.charts import \
    traffic_flow_counts, speed_limits, road_types


def test_dataframe_type_traffic_flow_counts():
    """Ensure function breaks if not given a dataframe."""
    with pytest.raises(TypeError):
        traffic_flow_counts("STREET_DATA")


def test_dataframe_type_speed_limits():
    """Ensure function breaks if not given a dataframe."""
    with pytest.raises(TypeError):
        speed_limits("STREET_DATA")


def test_dataframe_type_road_types():
    """Ensure function breaks if not given a dataframe."""
    with pytest.raises(TypeError):
        road_types("STREET_DATA")
