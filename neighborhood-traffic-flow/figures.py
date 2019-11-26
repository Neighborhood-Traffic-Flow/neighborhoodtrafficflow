"""
Functions to figures shown in the dashboard
1. map of Seattle neighborhoods
2. traffic flow map
"""
import numpy as np
import matplotlib.cm as cm
import math
import matplotlib
from matplotlib.colors import Normalize
import plotly.graph_objs as go

from controls import BOUNDS, CENTROIDS, NEIGHBORHOODS, ROAD_TYPE 

# Mapbox style for neighborhood and flow maps
MAPBOX_STYLE = 'carto-positron'


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
                'style': MAPBOX_STYLE,
                'center': {
                    'lon': -122.3266736043623,
                    'lat': 47.61506497849028
                },
                'zoom': 11.25
            }
        }
    }
    return figure


def lat2y(lat):
    """Pseudo-Mercator projection"""
    y = 180.0/math.pi*math.log(math.tan(math.pi/4.0+lat*(math.pi/180.0)/2.0))
    return y


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
    bounds = BOUNDS[neighborhood]
    lon_range = bounds[2] - bounds[0]
    lat_range = bounds[3] - bounds[1]
    height = 750
    width = lon_range/lat_range*height
    lon = CENTROIDS[neighborhood][0]
    lat = CENTROIDS[neighborhood][1]
    nbhd_idx = data_frame.nbhd.apply(
        lambda nbhd_list: int(neighborhood) in nbhd_list)
    data_frame = data_frame[nbhd_idx]
    if map_type == 'flow':
        data_frame = data_frame.rename(columns={str(year): 'flow'})
        colorscale = flow_cmap
        cmax = 108179
        title = 'Average Weekday Traffic (1000 vehicles)'
    elif map_type == 'speed':
        colorscale = speed_cmap
        cmax = 60
        title = 'Speed Limit (mph)'
    else:
        colorscale = road_cmap
        cmax = 5.9
        title = 'Arterial Classification'
    data = [{
        'type': 'scattergl',
        'name': 'Centroid',
        'x': [lon],
        'y': [lat2y(lat)],
        'mode': 'markers',
        'showlegend': False,
        'marker': {
            'size': 0,
            'color': [0],
            'cmin': 0,
            'cmax': cmax,
            'colorscale': colorscale,
            'showscale': True,
            'colorbar': {
                'tickfont': {
                    'size': 16
                },
                'title': {
                    'text': title,
                    'font': {
                        'size': 20
                    },
                    'side': 'right'
                }
            }
        }
    }]
    if map_type == 'road':
        data[0]['marker']['colorbar']['tickvals'] = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
        data[0]['marker']['colorbar']['ticktext'] = [
            'Not Designated',
            'Principal Arterial',
            'Minor Arterial',
            'Collector Arterial',
            'State Highway',
            'Interstate Freeway'
        ]

    for _, row in data_frame.iterrows():
        trace = {
            'type': 'scattergl',
            'x': row['lon'],
            'y': [lat2y(lat) for lat in row['lat']],
            'mode': 'lines',
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
            'width': width,
            'height': height,
            'hovermode': 'closest',
            'clickmode': 'none'
        }
    }
    return figure


def traffic_flow_chart(data_frame, neighborhood=92, map_type='flow'):
    """Create traffic flow chart"""
    data = []
    for nbhd in CENTROIDS.keys():
        data.append(get_series(data_frame, int(nbhd)))
    data.append(get_series(data_frame, int(neighborhood), 5, 'steelblue'))
    figure = {
        'data': data
    }
    return figure


def get_series(data_frame, nbhd, width=2, color='rgb(192,192,192)'):
    """Get time series of flow for given neighborhood"""
    nbhd_idx = data_frame.nbhd.apply(
        lambda nbhd_list: nbhd in nbhd_list)
    nbhd_flow = data_frame[nbhd_idx]
    years = np.arange(2007,2019)
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

# https://plot.ly/python/v3/matplotlib-colorscales/
def matplotlib_to_plotly(cmap, pl_entries):
    h = 1.0/(pl_entries - 1)
    pl_colorscale = []

    for k in range(pl_entries):
        C = map(np.uint8, np.array(cmap(k*h)[:3])*255)
        C_list = [c for c in C]
        pl_colorscale.append([k*h, 'rgb' + str((C_list[0], C_list[1], C_list[2]))])

    return pl_colorscale

flow_cmap = cm.get_cmap('viridis')
flow_norm = Normalize(vmin=0, vmax=108179)
flow_rgb = []
for i in range(0,255):
    k = matplotlib.colors.colorConverter.to_rgb(flow_cmap(flow_norm(i)))
    flow_rgb.append(k)
flow_cmap = matplotlib_to_plotly(flow_cmap, 255)


speed_cmap = cm.get_cmap('RdYlGn_r')
speed_norm = Normalize(vmin=0, vmax=60)
speed_rgb = []
for i in range(0,255):
    k = matplotlib.colors.colorConverter.to_rgb(speed_cmap(speed_norm(i)))
    speed_rgb.append(k)
speed_cmap = matplotlib_to_plotly(speed_cmap, 255)


road_cmap = cm.get_cmap('tab10')
road_rgb = []
for i in range(6):
    if i == 1:
        road_rgb.append([i/5.9, 'rgb(1,1,1)'])
        road_rgb.append([(i+0.9)/5.9, 'rgb(1,1,1)'])
    else:
        C = map(np.uint8, np.array(road_cmap(i)[:3])*255)
        C_list = [c for c in C]
        road_rgb.append([i/5.9, 'rgb' + str((C_list[0], C_list[1], C_list[2]))])
        road_rgb.append([(i+0.9)/5.9, 'rgb' + str((C_list[0], C_list[1], C_list[2]))])
road_cmap = road_rgb



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
    if val is None or np.isnan(val):
        return 'rgb(192,192,192)'
    if map_type == 'flow':
        cmap = cm.get_cmap('viridis')
        norm = Normalize(vmin=0, vmax=108179)
    elif map_type == 'speed':
        cmap = cm.get_cmap('RdYlGn_r')
        norm = Normalize(vmin=0, vmax=60)
    else:
        cmap = cm.get_cmap('tab10')
        norm = Normalize(vmin=0, vmax=9)
    if map_type == 'road' and val == 1:
        rgba = (0.0,0.0,0.0,1.0)
    else:
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
