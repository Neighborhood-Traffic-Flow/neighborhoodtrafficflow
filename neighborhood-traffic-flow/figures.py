# TODO: better documentation!

# 92 = University District

import numpy as np
import matplotlib.cm as cm
from matplotlib.colors import Normalize

from controls import CENTROIDS

# define colormap
# right now vmin, vmax based on 2018
# update vmin, vmax dynamically, or just based on all years
cmap = cm.get_cmap('viridis')
norm = Normalize(vmin=387, vmax=108179)
def flow_color(flow):
    if flow is None:
        return 'rgb(255,255,255)'
    rgba = cmap(norm(float(flow)))
    return 'rgb(%f,%f,%f)' % rgba[:-1]
    


# Create neighborhood map with current neighborhood highlighted
def neighborhood_map(num,df,regionids,names,selected=92):
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
            'width': 1000,
            'height': 1500,
            'clickmode': 'event+select',
            'mapbox': {
                'style': 'stamen-terrain',
                'center': {
                    'lon': -122.3266736043623,
                    'lat': 47.61506497849028
                },
                'zoom': 11.25
            }
        }
    }
    return figure




# Create traffic flow map of currently selected neighborhood
def traffic_flow_map(df,neighborhood='92',year=2018,flow_type='flow'):
    lon = CENTROIDS[neighborhood][0]
    lat = CENTROIDS[neighborhood][1]
    nbhd_idx = df.nbhd.apply(lambda nbhd_list: int(neighborhood) in nbhd_list)
    df = df[nbhd_idx & (df['year']==year)]
    data = []
    for idx,row in df.iterrows():
        trace = {
            'type': 'scattermapbox',
            'mode': 'lines',
            'lon': row['lon'],
            'lat': row['lat'],
            'line': {
                'width': 5,
                'color': flow_color(row[flow_type])
            },
            'showlegend': False,
            'hoverinfo': 'text',
            'hovertext': row['name'] + ', Flow: ' + str(row[flow_type])
        }
        data.append(trace)
    figure = {
        'data': data,
        'layout': {
            'width': 1000,
            'height': 750,
            'hovermode': 'closest',
            'clickmode': 'none',
            'mapbox': {
                'style': 'stamen-terrain',
                'center': {
                    'lon': lon,
                    'lat': lat
                },
                'zoom': 13.5
            }
        }
    }
    return figure

    

# Create traffic flow chart
def traffic_flow_chart():
    figure = {
        'data': [{
            'type': 'scatter',
            'x': [1,2,3],
            'y': [1,2,3]
        }],
        'layout': {
            'line_color': 'deepskyblue'
        }
    }
    return figure