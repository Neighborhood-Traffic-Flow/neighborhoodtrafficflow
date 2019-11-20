"""
Functions to figures shown in the dashboard
1. map of Seattle neighborhoods
2. traffic flow map
"""
import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import plotly.graph_objs as go

from controls import ROAD_TYPE, CENTROIDS

# Mapbox style for neighborhood and flow maps
MAP_STYLE = 'carto-positron'


def neighborhood_map(num, data, region_ids, names, selected=92):
    """Create neighborhood map with selected neighborhood highlighted

    Create Plotly choroplethmapbox figure of Seattle neighborhoods from
    Zillow data with selected neighborhood highlighted in a darker
    color. Default neighborhood is University District (index=92).

    Parameters
    ----------
    num : int
        Number of Seattle neighborhoods.
    data : dict
        Neighborhood polygon geometry.
    region_ids : list
        Neighborhood indices (str) from Zillow data.
    names : list
        Neighborhood names (str).
    selected : int
        Index of selected neighborhood on map.

    Returns
    -------
    figure : dict
        Plotly choroplethmapbox figure.
    """
    figure = {
        'data': [{
            'type': 'choroplethmapbox',
            'z': np.zeros((num)),
            'geojson': data,
            'locations': region_ids,
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
                'style': MAP_STYLE,
                'center': {
                    'lon': -122.3266736043623,
                    'lat': 47.61506497849028
                },
                'zoom': 11.25
            }
        }
    }
    return figure


def traffic_flow_map(data_frame, neighborhood='92', map_type='flow', year=2018):
    """Create traffic flow map of currently selected neighborhood

    Create Plotly scattermapbox figure of roads in selected Seattle
    neighborhood, where roads are colored by either traffic flow,
    speed limit, or road type. Default is University District (idx=92)
    with roads colored by traffic flow in 2018.

    Parameters
    ----------
    data : Pandas Dataframe
        DataFrame with traffic flow, speed limit, and road type data.
    neighborhood : str
        Index of selected neighborhood from dropdown.
    map_type : str
        Selected type from radio: 'flow' (default), 'speed', or 'road'.
    year : int
        Selected year from slider.

    Returns
    -------
    figure : dict
        Plotly scattermapbox figure.
    """
    lon = CENTROIDS[neighborhood][0]
    lat = CENTROIDS[neighborhood][1]
    nbhd_idx = data_frame.nbhd.apply(lambda nbhd_list: int(neighborhood) in nbhd_list)
    if map_type == 'flow':
        flow_idx = data_frame['flow'].notna()
        year_idx = data_frame['year'] == year
        data_frame = data_frame[nbhd_idx & flow_idx & year_idx]
    elif map_type == 'speed':
        data_frame = data_frame[nbhd_idx & (data_frame['speed'].notna())]
    else:
        data_frame = data_frame[nbhd_idx & (data_frame['road'].notna())]
    data = []

    for _, row in data_frame.iterrows():
        trace = {
            'type': 'scattermapbox',
            'mode': 'lines',
            'lon': row['lon'],
            'lat': row['lat'],
            'line': {
                'width': 5,
                'color': road_color(row[map_type], map_type)
            },
            'showlegend': False,
            'hoverinfo': 'text',
            'hovertext': hover_text(row['name'], row[map_type], map_type)
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
                'style': MAP_STYLE,
                'center': {
                    'lon': lon,
                    'lat': lat
                },
                'zoom': 13.5
            }
        }
    }
    return figure


<<<<<<< HEAD
def traffic_flow_chart(df, neighborhood=92, map_type='flow'):
    """Create traffic flow chart"""
    if map_type == 'flow':
        y_df = df.loc[df["flow"].notnull(), "flow"]
    elif map_type == 'speed':
        y_df = df.loc[df["speed"].notnull(), "speed"]
    else:
        y_df = df.loc[df["road"].notnull(), "road"]
    figure = {
        'data': [go.Scatter(
            x = df["year"],
            y = y_df,
        marker={
            'line': {'color': 'deepskyblue'}
            }
        )
    ]
}
    return figure


def road_color(val, map_type):
    """Assign road color

    Determine the color of a given road based on road type and value.
    Color is determined by viridis (flow), RdYlGn (speed), and tab10
    (road) colormaps and min/max values in dataset.

    Parameters
    ----------
    val : double
        Traffic flow, speed limit, or road type of given road.
    map_type : str
        Either 'flow', 'speed', or 'road'.

    Returns
    -------
    rgb : str
        String containting rgb value of given road.
    """
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


def hover_text(name, val, map_type):
    """Create hover text for traffic flow map

    Create description that appears when when mouse hovers over a road
    in the traffic flow map, e.g., '65th St N, Speed Limit: 30mph'.

    Parameters
    ----------
    name : str
        Name of the given street.
    val : float
        Traffic flow, speed limit, or road type of given road.
    map_type : str
        Either 'flow', 'speed', or 'road'.

    Returns
    -------
    hovertext : str
        Description of road including name and value.
    """
    if map_type == 'flow':
        return name + ', Flow Count:' + str(val)
    if map_type == 'speed':
        return name + ', Speed Limit:' + str(int(val)) + 'mph'
    return name + ', Road Type:' + ROAD_TYPE[val]


