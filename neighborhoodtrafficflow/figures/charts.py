"""Functions corresponding charts shown in the dashboard"""
from pathlib import Path

import numpy as np
import pandas as pd

# Arterial classification for traffic flow map hover text
ROAD_TYPE = {
    0: 'Not Designated',
    1: 'Principal Arterial',
    2: 'Minor Arterial',
    3: 'Collector Arterial',
    4: 'State Highway',
    5: 'Interstate Freeway'
}

# Neighborhood names, centroids, and bounds
CWD = Path(__file__).parent
INFO_PATH = CWD / '../data/cleaned/nbhd_info.csv'
NBHD_INFO = pd.read_csv(INFO_PATH)


def traffic_flow_counts(data_frame, neighborhood=92):
    """Create traffic flow stats."""
    x_city = []
    y_city = []
    x_nbhd = []
    y_nbhd = []
    for year in range(2007, 2019):
        # City statistics
        city_data = data_frame[data_frame[str(year)] >= 0]
        x_city.extend([year] * len(city_data))
        y_city.extend(city_data[str(year)].to_list())

        # Neighborhood statistics
        nbhd_idx = city_data.nbhd.apply(
            lambda nbhd_list: int(neighborhood) in nbhd_list)
        nbhd_data = city_data[nbhd_idx]
        x_nbhd.extend([year] * len(nbhd_data))
        y_nbhd.extend(nbhd_data[str(year)].to_list())
    trace_city = {
        'type': 'box',
        'name': 'City',
        'x': x_city,
        'y': y_city,
        'showledgend': False,
        'marker': {
            'color': 'gray'
        }
    }
    trace_nbhd = {
        'type': 'box',
        'name': 'Neighborhood',
        'x': x_nbhd,
        'y': y_nbhd,
        'showledgend': False,
        'marker': {
            'color': 'steelblue'
        }
    }
    figure = {
        'data': [trace_city, trace_nbhd],
        'layout': {
            'margin': {
                't': 20,
                'l': 70,
                'b': 70
            },
            'paper_bgcolor': '#F9F9F9',
            'hovermode': 'closest',
            'boxmode': 'group',
            'xaxis': {
                'title': 'Year',
                'linecolor': 'black',
                'mirror': True,
                'tickmode': 'array',
                'tickvals': np.arange(2007, 2019),
                'tickangle': -90
            },
            'yaxis': {
                'title': 'Average Weekday Traffic (1000 vehicles)',
                'linecolor': 'black',
                'mirror': True
            }
        }
    }
    return figure


def speed_limits(data_frame, neighborhood=92):
    """docstring"""
    city_data = data_frame[data_frame['speed'] >= 0]
    x_city = city_data['speed'].to_list()
    trace_city = {
        'type': 'histogram',
        'name': 'City',
        'opacity': 0.75,
        'x': x_city,
        'histnorm': 'percent',
        'marker': {
            'color': 'gray'
        }
    }
    nbhd_idx = city_data.nbhd.apply(
        lambda nbhd_list: int(neighborhood) in nbhd_list)
    nbhd_data = city_data[nbhd_idx]
    nbhd_roads = nbhd_data['speed'].to_list()
    trace_nbhd = {
        'type': 'histogram',
        'name': 'Neighborhood',
        'opacity': 0.75,
        'x': nbhd_roads,
        'histnorm': 'percent',
        'marker': {
            'color': 'steelblue'
        }
    }
    figure = {
        'data': [trace_city, trace_nbhd],
        'layout': {
            'margin': {
                't': 20,
                'b': 40,
                'l': 70
            },
            'paper_bgcolor': '#F9F9F9',
            'barmode': 'overlay',
            'xaxis': {
                'title': 'Speed Limit (mph)',
                'linecolor': 'black',
                'mirror': True
            },
            'yaxis': {
                'title': 'Percent of Roads',
                'linecolor': 'black',
                'mirror': True
            }
        }
    }
    return figure


def road_types(data_frame, neighborhood=92):
    """docstring"""
    city_data = data_frame
    x_city = city_data['road'].to_list()
    trace_city = {
        'type': 'histogram',
        'name': 'City',
        'opacity': 0.75,
        'x': x_city,
        'histnorm': 'percent',
        'marker': {
            'color': 'gray'
        }
    }
    nbhd_idx = city_data.nbhd.apply(
        lambda nbhd_list: int(neighborhood) in nbhd_list)
    nbhd_data = city_data[nbhd_idx]
    nbhd_roads = nbhd_data['road'].to_list()
    trace_nbhd = {
        'type': 'histogram',
        'name': 'Neighborhood',
        'opacity': 0.75,
        'x': nbhd_roads,
        'histnorm': 'percent',
        'marker': {
            'color': 'steelblue'
        }
    }
    figure = {
        'data': [trace_city, trace_nbhd],
        'layout': {
            'margin': {
                't': 20,
                'l': 70
            },
            'paper_bgcolor': '#F9F9F9',
            'barmode': 'overlay',
            'xaxis': {
                'title': 'Arterial Classification',
                'tickmode': 'array',
                'tickvals': list(ROAD_TYPE.keys()),
                'ticktext': list(ROAD_TYPE.values()),
                'linecolor': 'black',
                'mirror': True
            },
            'yaxis': {
                'title': 'Percent of Roads',
                'linecolor': 'black',
                'mirror': True
            }
        }
    }
    return figure
