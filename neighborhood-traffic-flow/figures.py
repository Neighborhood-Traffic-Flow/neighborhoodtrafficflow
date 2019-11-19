"""
Functions to figures shown in the dashboard
1. map of Seattle neighborhoods
2. traffic flow map
"""

# 92 = University District

import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from controls import ROAD_TYPE, CENTROIDS

mapbox_style = 'carto-positron'


def neighborhood_map(num, df, regionids, names, selected=92):
    """Create neighborhood map with current neighborhood highlighted

    Arguments:
    ----------
    num:
    df:
    regionids:
    names:
    selected:

    """
    figure = {
        'data': [{
            'type': 'choroplethmapbox',
            'z': np.zeros((num)),
            'geojson': df,
            'locations': regionids,
            'hovertext': names,
            'hoverinfo': 'text',
            'marker': {
                'line': {
                    'width': 3
                }
            },
            'colorscale': 'Greens',
            'showscale': False,
            'selectedpoints': [selected],
            'selected': {
                'marker': {
                    'opacity': 0.75
                }
            },
            'unselected': {
                'marker': {
                    'opacity': 0.25
                }
            }
        }],
        'layout': {
            'margin': {
                'l': 0,
                'r': 0,
                't': 0,
                'b': 0
            },
            'width': 1000,
            'height': 1500,
            'clickmode': 'event+select',
            'mapbox': {
                'style': mapbox_style,
                'center': {
                    'lon': -122.3266736043623,
                    'lat': 47.61506497849028
                },
                'zoom': 11.25
            }
        }
    }
    return figure


def traffic_flow_map(df, neighborhood='92', map_type='flow', year=2018):
    """Create traffic flow map of currently selected neighborhood

    Arguments:
    ----------
    df:
    neighborhood:
    year:
    map_type: 'flow', 'speed', or 'road'
    """
    lon = CENTROIDS[neighborhood][0]
    lat = CENTROIDS[neighborhood][1]
    nbhd_idx = df.nbhd.apply(lambda nbhd_list: int(neighborhood) in nbhd_list)
    if map_type == 'flow':
        df = df[nbhd_idx & (df['flow'].notna()) & (df['year'] == year)]
    elif map_type == 'speed':
        df = df[nbhd_idx & (df['speed'].notna())]
    else:
        df = df[nbhd_idx & (df['road'].notna())]
    data = []

    for idx, row in df.iterrows():
        trace = {
            'type': 'scattermapbox',
            'mode': 'lines',
            'lon': row['lon'],
            'lat': row['lat'],
            'line': {
                'width': 5,
                'color': road_color(row[map_type],map_type)
            },
            'showlegend': False,
            'hoverinfo': 'text',
            'hovertext': hover_text(row['name'],row[map_type],map_type)
        }
        data.append(trace)
    figure = {
        'data': data,
        'layout': {
            'margin': {
                'l': 0,
                'r': 0,
                't': 0,
                'b': 0
            },
            'width': 1000,
            'height': 750,
            'hovermode': 'closest',
            'clickmode': 'none',
            'mapbox': {
                'style': mapbox_style,
                'center': {
                    'lon': lon,
                    'lat': lat
                },
                'zoom': 13.5
            }
        }
    }
    return figure


def road_color(val,map_type):
    """Define the flow color"""

    if val is None:
        return 'rgb(255,255,255)'

    if map_type == 'flow':
        cmap = cm.get_cmap('viridis')
        norm = Normalize(vmin=0, vmax=108179)
    elif map_type == 'speed':
        cmap = cm.get_cmap('RdYlGn')
        norm = Normalize(vmin=0, vmax=60)
    else:
        cmap = cm.get_cmap('tab10')
        norm = Normalize(vmin=0, vmax=5)
    
    rgba = cmap(norm(float(val)))
    return 'rgb(%f,%f,%f)' % rgba[:-1]


def hover_text(name,val,map_type):

    if map_type == 'flow':
        return name + ', Flow Count:' + str(val)
    elif map_type == 'speed':
        return name + ', Speed Limit:' + str(int(val)) + 'mph'
    else:
        return name + ', Road Type:' + ROAD_TYPE[val]


def traffic_flow_chart():
    """Create traffic flow chart"""
    figure = {
        'data': [{
            'type': 'scatter',
            'x': [1, 2, 3],
            'y': [1, 2, 3]
        }],
        'layout': {
            'line_color': 'deepskyblue'
        }
    }
    return figure
