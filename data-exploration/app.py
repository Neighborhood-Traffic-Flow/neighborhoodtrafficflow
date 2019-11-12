# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data
import geopandas as gpd
import json

# Controls
from controls import NEIGHBORHOODS, TIME_OF_DAY, CENTROIDS


# TODO:
# - Data pre-processing:
#   * Do we want to do ahead of time, and add new datasets to repo, or put script in setup.py?
#   * Join traffic flow datasets for multiple years
#   * Join neighborhood and traffic flow datasets
# - Create function to filter data by neighborhood, year, time of day
# - Add roads traces to traffic flow map (so slow) with controls
# - Add time series chart with controls
# - Styling


# ISSUES:
# - Shift+Click and Lasso can select multiple neighborhoods, can we disable this?
# - Clicking the home button on traffic flow map takes us back to U-District, not current neighborhood


# Create control options
nbhd_options = [{'label': NEIGHBORHOODS[regionid], 'value': regionid} for regionid in NEIGHBORHOODS]
time_options = [{'label': TIME_OF_DAY[0][idx], 'value': idx} for idx in TIME_OF_DAY[0]]
year_options = {year: str(year) for year in range(2007,2019)}


# Import neighborhood data
with open('zillow-neighborhoods/zillow-neighborhoods.geojson') as json_file:
    nbhd_json = json.load(json_file)
nbhd_gpd = gpd.read_file('zillow-neighborhoods/zillow-neighborhoods.shp')


# Add id feature to dataset
for feature in nbhd_json['features']:
    feature['id'] = feature['properties']['regionid']    

# Create neighborhood map
def neighborhood_map(current=92):
    figure = {
        'data': [{
            'type': 'choroplethmapbox',
            'z': 0*nbhd_gpd.index,
            'geojson': nbhd_json,
            'locations': nbhd_gpd.regionid,
            'hovertext': nbhd_gpd.name,
            'hoverinfo': 'text',
            'marker': {
                'line': {
                    'width': 3
                }
            },
            'colorscale': 'Greens',
            'showscale': False,
            'selectedpoints': [current], 
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


# Create traffic flow map
def traffic_flow_map(current='92'):
    centroid = CENTROIDS[current]
    lon = centroid[0]
    lat = centroid[1]
    figure = {
        'data': [{
            'type': 'scattermapbox',
            'mode': 'markers',
            'lon': [lon],
            'lat': [lat],
            'marker': {
                'size': 10
            },
            'showlegend': False
        }],
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


# Initialize dashboard
app = dash.Dash(__name__)


# Define dashboard layout
app.layout = html.Div(
    id='mainContainer',
    className='twelve columns',
    children=[
        # Header
        html.Div(
            id='header',
            className='twelve columns',
            children=[
                html.H1('Neighborhood Traffic Flow'),
                html.H4( 
                    html.A(
                        'CSE 583: Software Engineering for Data Scientists',
                        href='https://uwseds.github.io/'
                    )
                )
            ]
        ),
        # Dashboard
        html.Div(
            id='dashboard',
            className='twelve columns',
            children=[
                # Column 1
                html.Div(
                    id='columnOne',
                    className='six columns',
                    children=[
                        # Seattle Neighborhood Map
                        html.Div(
                            id='neighborhoodMapContainer',
                            children=[
                                html.H4('Seattle Neighborhoods'),
                                dcc.Graph(
                                    id='neighborhoodMap',
                                    figure=neighborhood_map()
                                ),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=nbhd_options,  
                                    value='92'
                                )
                            ],
                            style={
                                'margin': 50
                            }
                        )
                    ]
                ),
                # Column 2
                html.Div(
                    id='columnTwo',
                    className='six columns',
                    children=[
                        # Traffic Flow Map
                        html.Div(
                            id='trafficFlowMapContainer',
                            children=[
                                html.H4('Traffic Flow'),
                                dcc.Graph(
                                    id='trafficFlowMap',
                                    figure=traffic_flow_map()
                                ),
                                dcc.RadioItems(
                                    options=time_options,
                                    value='ADT',
                                    labelStyle={
                                        'display': 'inline-block'
                                    }
                                ),
                                dcc.Slider(
                                    id='slider',
                                    min=2007,
                                    max=2018,
                                    marks=year_options,
                                    value=2018
                                )
                            ],
                            style={
                                'margin': 50
                            }
                        ),
                        # Traffic Flow Chart
                        html.Div(
                            id='trafficFlowChartContainer',
                            children=[
                                dcc.Graph(
                                    id='trafficFlowChart',
                                    figure=traffic_flow_chart()
                                ),
                                dcc.Checklist(
                                    options=time_options,
                                    value=['ADT'],
                                    labelStyle={
                                        'display': 'inline-block'
                                    }
                                )
                            ],
                            style={
                                'margin': 50
                            }
                        )
                    ]
                )
            ]
        )
    ]
)


# Update neighborhood map after dropdown selection
@app.callback(
    Output('neighborhoodMap', 'figure'),
    [Input('dropdown', 'value')]
)

def update_neighborhood_map(value):
    return neighborhood_map(value)


# Update traffic flow map after dropdown selection
@app.callback(
    Output('trafficFlowMap', 'figure'),
    [Input('dropdown', 'value')]
)

def update_traffic_flow_map(value):
    return traffic_flow_map(value)


# Update dropdown after neighborhood map selection
@app.callback(
    Output('dropdown', 'value'),
    [Input('neighborhoodMap', 'selectedData')]
)
def update_dropdown(selectedData):
    try:
        return str(selectedData['points'][0]['pointIndex'])
    except:
        return '92'


# Run dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
