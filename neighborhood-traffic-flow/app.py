"""Neighborhood traffic flow dashboard

Interactive dashboard to explore traffic flow, speed limits, and road
types in Seattle neighborhoods. To use, run `python app.py` in the
terminal and copy/paste the URL into your browers.
"""
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

from controls import NEIGHBORHOODS, MAP_TYPE
from figures import neighborhood_map, traffic_flow_map, traffic_flow_chart

# Import neighborhood data
with open('data/neighborhoods.geojson') as json_file:
    NBHD_JSON = json.load(json_file)
for feature in NBHD_JSON['features']:
    feature['id'] = feature['properties']['regionid']
NUM = len(NBHD_JSON['features'])
REGION_IDS = [feature['properties']['regionid'] for feature in NBHD_JSON['features']]
NAMES = [feature['properties']['name'] for feature in NBHD_JSON['features']]
NBHD_DATA = [NUM, NBHD_JSON, REGION_IDS, NAMES]

# Import filtered dataframes
MAP_DATA = pd.read_pickle('data/map_data.pkl')
CHART_DATA = pd.read_pickle('data/flow_chart.pkl')

# Create control options
NBHD_OPTIONS = [{'label': NEIGHBORHOODS[regionid], 'value': regionid} for regionid in NEIGHBORHOODS]
MAP_OPTIONS = [{'label': MAP_TYPE[0][idx], 'value': idx} for idx in MAP_TYPE[0]]
YEAR_OPTIONS = {year: str(year) for year in range(2007, 2019)}

# Initialize dashboard
APP = dash.Dash(__name__)

# Define dashboard layout
APP.layout = html.Div(
    id='mainContainer',
    className='twelve columns',
    children=[
        # Header
        html.Div(
            id='header',
            className='twelve columns',
            children=[
                html.H1('Neighborhood Traffic Flow', style={'color': 'black', 'fontSize': 50}),
                html.H4(
                    html.A(
                        'CSE 583: Software Engineering for Data Scientists',
                        href='https://uwseds.github.io/'
                    )
                )
            ]
        ),
        # Neighborhood selector
        html.Div(
            id='dropdownContainer',
            className='twelve columns',
            children=[
                html.H4('Choose a Seattle neighborhood:'),
                dcc.Dropdown(
                    id='dropdown',
                    options=NBHD_OPTIONS,
                    value='92',
                    style={
                        'width': '80%'
                    }
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
                                    options=MAP_OPTIONS,
                                    value='flow',
                                    labelStyle={
                                        'display': 'inline-block'
                                    }
                                ),
                                dcc.Slider(
                                    id='slider',
                                    min=2007,
                                    max=2018,
                                    marks=YEAR_OPTIONS,
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
                                    options=MAP_OPTIONS,
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
@APP.callback(
    Output('neighborhoodMap', 'figure'),
    [Input('dropdown', 'value')]
)
def update_neighborhood_map(neighborhood):
    """Update neighborhood map

    Updates neighborhood map after a drowpdown selection is made.

    Input:  (int)  Currently selected neighborhood
    Output: (dict) Plotly choroplethmapbox figure
    """
    return neighborhood_map(*NBHD_DATA, neighborhood)


# Update traffic flow map after dropdown selection
@APP.callback(
    Output('trafficFlowMap', 'figure'),
    [Input('dropdown', 'value'),
     Input('radio', 'value'),
     Input('slider', 'value')]
)
def update_traffic_flow_map(neighborhood, map_type, year):
    """Update traffic flow map

    Updates traffic flow map after a dropdown, radio, or slider
    selection is made.

    Input:  (int)  Currently selected neighborhood
            (str)  Currently selected map type
            (int)  Currently selected year
    Output: (dict) Plotly scattermapbox figure
    """
    return traffic_flow_map(MAP_DATA, neighborhood, map_type, year)


# Update dropdown after neighborhood map selection
@APP.callback(
    Output('dropdown', 'value'),
    [Input('neighborhoodMap', 'selectedData')]
)
def update_dropdown(neighborhood):
    """DOCSTRING WILL FIX LATER"""
    try:
        return str(neighborhood['points'][0]['pointIndex'])
    except TypeError:
        return '92'

# Run dashboard
if __name__ == '__main__':
    APP.run_server(debug=True)
