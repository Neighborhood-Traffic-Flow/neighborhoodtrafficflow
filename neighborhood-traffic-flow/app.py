# Dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Data
import json
import pandas as pd

# Controls
from controls import NEIGHBORHOODS, MAP_TYPE

# Visualizations
from figures import neighborhood_map, traffic_flow_map, traffic_flow_chart


# TODO:
# - Data pre-processing:
#   * Do we want to do ahead of time, and add new datasets to repo, or put script in setup.py?
#   * Join traffic flow datasets for multiple years
#   * Join neighborhood and traffic flow datasets
# - Create function to filter data by neighborhood, year, time of day
# - Add roads traces to traffic flow map (so slow) with controls
# - Add time series chart with controls
# - Style and documention


# ISSUES:
# - Shift+Click and Lasso can select multiple neighborhoods, can we disable this?
# - Clicking the home button on traffic flow map takes us back to U-District, not current neighborhood


# Create control options
nbhd_options = [{'label': NEIGHBORHOODS[regionid], 'value': regionid} for regionid in NEIGHBORHOODS]
map_options = [{'label': MAP_TYPE[0][idx], 'value': idx} for idx in MAP_TYPE[0]]
year_options = {year: str(year) for year in range(2007, 2019)}


# Import neighborhood data
with open('data/neighborhoods.geojson') as json_file:
    neighborhoods = json.load(json_file)
for feature in neighborhoods['features']:
    feature['id'] = feature['properties']['regionid']
num = len(neighborhoods['features'])
regionids = [feature['properties']['regionid'] for feature in neighborhoods['features']]
names = [feature['properties']['name'] for feature in neighborhoods['features']]
NBHD_DATA = [num, neighborhoods, regionids, names]


# Import filtered dataframes
MAP_DATA = pd.read_pickle('data/map_data.pkl')
CHART_DATA = pd.read_pickle('data/flow_chart.pkl')


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
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=nbhd_options,
                                    value='92'
                                ),
                                dcc.Graph(
                                    id='neighborhoodMap',
                                    figure=neighborhood_map(*NBHD_DATA)
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
                                html.H4('Traffic Flow Map'),
                                dcc.RadioItems(
                                    id='radio',
                                    options=map_options,
                                    value='flow',
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
                                ),
                                html.Br(),
                                dcc.Graph(
                                    id='trafficFlowMap',
                                    figure=traffic_flow_map(MAP_DATA)
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
                                html.H4('Traffic Flow Stats'),
                                dcc.Checklist(
                                    id='checklist',
                                    options=map_options,
                                    value=['flow'],
                                    labelStyle={
                                        'display': 'inline-block'
                                    }
                                ),
                                dcc.Graph(
                                    id='trafficFlowChart',
                                    figure=traffic_flow_chart()
                                )
                            ]
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
def update_neighborhood_map(neighborhood):
    return neighborhood_map(*NBHD_DATA, neighborhood)


# Update traffic flow map after dropdown selection
@app.callback(
    Output('trafficFlowMap', 'figure'),
    [Input('dropdown', 'value'),
     Input('radio', 'value'),
     Input('slider', 'value')]
)
def update_traffic_flow_map(neighborhood, map_type, year):
    return traffic_flow_map(MAP_DATA, neighborhood, map_type, year)


# Update dropdown after neighborhood map selection
@app.callback(
    Output('dropdown', 'value'),
    [Input('neighborhoodMap', 'selectedData')]
)
def update_dropdown(neighborhood):
    try:
        return str(neighborhood['points'][0]['pointIndex'])
    except:
        return '92'


# Run dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
