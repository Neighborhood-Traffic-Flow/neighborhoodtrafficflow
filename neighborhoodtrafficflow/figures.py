"""
Functions to figures shown in the dashboard
1. map of Seattle neighborhoods
2. traffic flow map
"""
import math

import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from neighborhoodtrafficflow.controls import CENTROIDS, ROAD_TYPE, BOUNDS


def matplotlib_to_plotly(cmap, entries):
    """Convert matplotlib colormap to plotly format

    Define plotly colorscales for traffic flow map colorbar based on
    matplotlib colormaps.

    Parameters
    ----------
    cmap : matplotlib.colors.ListedColormap
           matplotlib.colors.LinearSegmentedColormap
        Current colormap used in traffic flow map.
    entries : int
        Number of colors in colorscale.

    Returns
    -------
    colorscale : list
        List of float and rgb values for colorscale.
    """
    cmap = cm.get_cmap(cmap)
    colorscale = []
    for k in range(entries):
        rgba = cmap(k)
        if entries == 6:
            if k == 1:
                colorscale.append([k / 5.9, 'rgb(1, 1, 1)'])
                colorscale.append([(k + 0.9) / 5.9, 'rgb(1, 1, 1)'])
            else:
                colorscale.append([k / 5.9, 'rgb(%f,%f,%f)' % rgba[:-1]])
                colorscale.append(
                    [(k + 0.9) / 5.9, 'rgb(%f,%f,%f)' % rgba[:-1]])
        else:
            colorscale.append([k / (entries - 1), 'rgb(%f,%f,%f)' % rgba[:-1]])
    return colorscale


# Colormaps for traffic flow map
FLOW_CMAP = matplotlib_to_plotly('viridis', 255)
SPEED_CMAP = matplotlib_to_plotly('RdYlGn_r', 255)
ROAD_CMAP = matplotlib_to_plotly('tab10', 6)
CMAP_INFO = {
    'flow': [FLOW_CMAP, 108179, 'Average Weekday Traffic (1000 vehicles)'],
    'speed': [SPEED_CMAP, 60, 'Speed Limit (mph)'],
    'road': [ROAD_CMAP, 5.9, 'Arterial Classification']
}


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
                    'width': 2
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
            'paper_bgcolor': '#F9F9F9',
            'clickmode': 'event+select',
            'mapbox': {
                'style': 'carto-positron',
                'center': {
                    # 'lon': -122.3266736043623,
                    # 'lat': 47.61506497849028
                    'lon': CENTROIDS[str(selected)][0],
                    'lat': CENTROIDS[str(selected)][1],
                },
                'zoom': 12
            }
        }
    }
    return figure


def traffic_flow_map(data_frame, neighborhood='92',
                     map_type='flow', year=2018):
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
    # Filter DataFrame by neighborhood
    nbhd_idx = data_frame.nbhd.apply(
        lambda nbhd_list: int(neighborhood) in nbhd_list)
    data_frame = data_frame[nbhd_idx]
    if map_type == 'flow':
        data_frame = data_frame.rename(columns={str(year): 'flow'})

    # Initialize data list with neighborhood centroid and colorscale
    info = CMAP_INFO[map_type]
    data = [{
        'type': 'scattergl',
        'name': 'Centroid',
        'x': [CENTROIDS[neighborhood][0]],
        'y': [lat2y(CENTROIDS[neighborhood][1])],
        'mode': 'markers',
        'showlegend': False,
        'marker': {
            'size': 0,
            'color': [0],
            'cmin': 0,
            'cmax': info[1],
            'colorscale': info[0],
            'showscale': True,
            'colorbar': {
                'tickfont': {
                    'size': 12
                }
            }
        }
    }]
    # Add categorical legend items for road types
    if map_type == 'road':
        data[0]['marker']['colorbar']['tickvals'] = np.arange(0.5, 6.5, 1)
        data[0]['marker']['colorbar']['ticktext'] = [
            'Not Designated',
            'Principal Arterial',
            'Minor Arterial',
            'Collector Arterial',
            'State Highway',
            'Interstate Freeway'
        ]

    # Add roads to data list
    for _, row in data_frame.iterrows():
        trace = {
            'type': 'scattergl',
            'x': row['lon'],
            'y': [lat2y(lat) for lat in row['lat']],
            'mode': 'lines',
            'line': {
                'width': 3,
                'color': road_color(row[map_type], map_type)
            },
            'showlegend': False,
            'hoverinfo': 'text',
            'hovertext': hover_text(row['name'], row[map_type], map_type)
        }
        data.append(trace)

    # Define plotly figure
    dimensions = get_dimensions(neighborhood)
    figure = {
        'data': data,
        'layout': {
            # 'width': dimensions[0],
            # 'height': dimensions[1],
            'title': info[2],
            #'plot_bgcolor': '#F9F9F9',
            'paper_bgcolor': '#F9F9F9',
            'hovermode': 'closest',
            'clickmode': 'none',
            'xaxis': {
                'linecolor': 'black',
                'mirror': True,
                'tickvals': [],
                'ticktext': []
            },
            'yaxis': {
                'linecolor': 'black',
                'mirror': True,
                'tickvals': [],
                'ticktext': []
            },
        }
    }
    return figure


def traffic_flow_chart(data_frame, neighborhood=92):
    """Create traffic flow chart"""
    data = []
    for nbhd in CENTROIDS:
        data.append(get_series(data_frame, int(nbhd)))
    data.append(get_series(data_frame, int(neighborhood), 5, 'steelblue'))
    figure = {
        'data': data,
        'layout': {
            'plot_bgcolor': '#F9F9F9',
            'paper_bgcolor': '#F9F9F9',
        }
    }
    return figure


def get_series(data_frame, nbhd, width=2, color='rgb(192,192,192)'):
    """Get time series of flow for given neighborhood"""
    nbhd_idx = data_frame.nbhd.apply(
        lambda nbhd_list: nbhd in nbhd_list)
    nbhd_flow = data_frame[nbhd_idx]
    years = np.arange(2007, 2019)
    flows = np.zeros(12)
    for i in range(12):
        flow_current = nbhd_flow[nbhd_flow[str(years[i])].notna()]
        flow_current = flow_current[str(years[i])].to_list()
        flow = [flow_current[j] for j in range(len(flow_current))]
        flows[i] = np.mean(flow)
    trace = {
        'type': 'scatter',
        'showlegend': False,
        'mode': 'lines',
        'x': years,
        'y': flows,
        'hoverinfo': 'none',
        'line': {
            'width': width,
            'color': color
        }
    }
    return trace


def lat2y(lat):
    """Pseudo-Mercator projection"""
    return 180.0 / math.pi * math.log(
        math.tan(math.pi / 4.0 + lat * (math.pi / 180.0) / 2.0))


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
    # Bad values
    if val is None or np.isnan(val):
        return 'rgb(192,192,192)'

    # Create colormap
    if map_type == 'flow':
        cmap = cm.get_cmap('viridis')
        norm = Normalize(vmin=0, vmax=108179)
    elif map_type == 'speed':
        cmap = cm.get_cmap('RdYlGn_r')
        norm = Normalize(vmin=0, vmax=60)
    else:
        cmap = cm.get_cmap('tab10')
        norm = Normalize(vmin=0, vmax=9)

    # Assign color
    if map_type == 'road' and val == 1:
        rgba = (0, 0, 0, 1)  # use black because orange looks like red
    else:
        rgba = cmap(norm(float(val)))

    # Parse color
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
        if val is None or np.isnan(val):
            return name + ', Flow Count: Unknown'
        return name + ', Flow Count:' + str(val)
    if map_type == 'speed':
        if val is None or np.isnan(val):
            return name + ', Speed Limit: Unknown'
        return name + ', Speed Limit:' + str(int(val)) + 'mph'
    if val is None or np.isnan(val):
        return name + ', Road Type: Unknown'
    return name + ', Road Type:' + ROAD_TYPE[val]


def get_dimensions(neighborhood):
    """Get traffic flow map dimensions

    Determine width and height of traffic flow map based on aspect
    ratio of currently selected neighborhood.

    Parameters
    ----------
    neighborhood : str
        Index of selected neighborhood from dropdown.

    Returns
    -------
    dimensions : list
        [width, height] in pixels (float).
    """
    bounds = BOUNDS[neighborhood]
    lon_range = bounds[2] - bounds[0]
    lat_range = bounds[3] - bounds[1]
    height = lat_range / lon_range * 1000
    if height <= 1000:
        return [1000, height]
    return [lon_range / lat_range * 1000, 1000]
