"""Neighborhood traffic flow dashboard

Interactive dashboard to explore traffic flow, speed limits, and road
types in Seattle neighborhoods. To use, run `python app.py` in the
terminal and copy/paste the URL into your browers.
"""
print("test")
import json

import pandas as pd
import importlib
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from neighborhoodtrafficflow.controls import NEIGHBORHOOD, MAP_TYPE
from neighborhoodtrafficflow.figures import neighborhood_map, traffic_flow_map, traffic_flow_chart

# Import neighborhood data
with open('data/neighborhoods.geojson') as json_file:
    NBHD_JSON = json.load(json_file)
for feature in NBHD_JSON['features']:
    feature['id'] = feature['properties']['regionid']
NUM = len(NBHD_JSON['features'])
REGION_IDS = [feature['properties']['regionid']
              for feature in NBHD_JSON['features']]
NAMES = [feature['properties']['name']
         for feature in NBHD_JSON['features']]
NBHD_DATA = [NUM, NBHD_JSON, REGION_IDS, NAMES]

# Import street data
STREET_DATA = pd.read_pickle('data/street_data.pkl')

# Create control options
NBHD_OPTIONS = [{'label': NEIGHBORHOOD[regionid], 'value': regionid}
                for regionid in NEIGHBORHOOD]
MAP_OPTIONS = [{'label': MAP_TYPE[0][idx], 'value': idx}
               for idx in MAP_TYPE[0]]
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
                html.H1(
                    'Neighborhood Traffic Flow',
                    style={
                        'color': 'black',
                        'fontSize': 50
                    }
                ),
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
                    className='five columns',
                    children=[
                        # Seattle Neighborhood Map
                        html.Div(
                            id='neighborhoodMapContainer',
                            children=[
                                html.H4('Choose a Seattle neighborhood:'),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=NBHD_OPTIONS,
                                    value='92',
                                    style={
                                        'width': '80%'
                                    }
                                ),
                                html.Br(),
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
                    className='seven columns',
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
                                html.Br(),
                                dcc.Graph(
                                    id='trafficFlowMap',
                                    # className='four columns',
                                    className='seven columns',
                                    figure=traffic_flow_map(
                                        STREET_DATA)
                                )
                            ],
                            style={
                                'margin': 50
                            }
                        ),
                        # Traffic Flow Chart
                        html.Div(
                            id='trafficFlowChartContainer',
                            className='seven columns',
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
                                    figure=traffic_flow_chart(
                                        STREET_DATA)
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

    Update neighborhood map after a drowpdown selection is made.

    Parameters
    ----------
    neighborhood : int
        Currently selected neighborhood (0-102).

    Returns
    -------
    figure : dict
        Plotly choroplethmapbox figure.
    """
    return neighborhood_map(*NBHD_DATA, selected=neighborhood)


# Update traffic flow map after dropdown, radio, or slider selection
@APP.callback(
    Output('trafficFlowMap', 'figure'),
    [Input('dropdown', 'value'),
     Input('radio', 'value'),
     Input('slider', 'value')]
)
def update_traffic_flow_map(neighborhood, map_type, year):
    """Update traffic flow map

    Update traffic flow map after a dropdown, radio, or slider
    selection is made. Also triggered by neighborhood map selection
    via dropdown callback.

    Parameters
    ----------
    neighborhood : str
        Currently selected neighborhood (0-102)
    map_type : str
        Currently selected map type (flow, speed, road).
    year : int
        Currently selected year (2007-2018)

    Returns
    -------
    figure : dict
        Plotly scattermapbox figure.
    """
    return traffic_flow_map(STREET_DATA, neighborhood, map_type, year)


# Update chart after dropdown selection
@APP.callback(
    Output('trafficFlowChart', 'figure'),
    [Input('dropdown', 'value')]
)
def update_traffic_flow_chart(neighborhood):
    """Update traffic flow chart"""
    return traffic_flow_chart(STREET_DATA, neighborhood)


# Update dropdown after neighborhood map selection
@APP.callback(
    Output('dropdown', 'value'),
    [Input('neighborhoodMap', 'selectedData')]
)
def update_dropdown(selected_data):
    """Update dropdown

    Update dropdown menu after neighborhood map selection is made.
    If TypeError, returns '92' (University District).

    Parameters
    ----------
    selected_data : dict
        Selected data in neighborhood map.

    Returns
    -------
    neighborhood : str
        Index of selected neighborhood (0-102).
    """
    try:
        return str(selected_data['points'][0]['pointIndex'])
    except TypeError:
        return '92'


# Run dashboard
if __name__ == '__main__':
    APP.run_server(debug=True)
