"""Neighborhood traffic flow dashboard

Interactive dashboard to explore traffic flow, speed limits, and road
types in Seattle neighborhoods. To use, run `python app.py` in the
terminal and copy/paste the URL into your browers.
"""
from pathlib import Path
import pickle

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from neighborhoodtrafficflow.figures import neighborhood_map, \
    traffic_flow_map, traffic_flow_series, traffic_flow_stats

# Data file paths
CWD = Path(__file__).parent
NBHD_PATH = CWD / 'data/cleaned/nbhd_data.pkl'
STREET_PATH = CWD / 'data/street_data.pkl'

# Import neighborhood data
with open(NBHD_PATH, 'rb') as pickle_file:
    NBHD_DATA = pickle.load(pickle_file)
NAMES = NBHD_DATA[3]

# Import street data
STREET_DATA = pd.read_pickle(STREET_PATH)

# Create control options for dropdown, radio, and slider
NBHD_OPTIONS = [{'label': NAMES[idx], 'value': idx}
                for idx in range(len(NAMES))]
MAP_OPTIONS = [{'label': 'Traffic Flow', 'value': 'flow'},
               {'label': 'Speed Limit', 'value': 'speed'},
               {'label': 'Road Type', 'value': 'road'}]
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
            className='twelve columns centerTitle',
            children=[
                html.H4('Neighborhood Traffic Flow'),
                html.H6(
                    children=[
                        'Final Project for ',
                        html.A(
                            'CSE 583: Software Engineering for\
                             Data Scientists',
                            href='https://uwseds.github.io/'
                        )
                    ]
                )
            ]
        ),
        # Row one
        html.Div(
            id='rowOne',
            className='twelve columns',
            children=[
                # Description
                html.Div(
                    className='six columns blankContainer',
                    children=[
                        html.H5('About This App',
                            className='centerTitle'),
                        html.P('This is an interactive dashboard for current and future Seattle residents\
                                to understand the traffic flow of neighboorhoods in the city. By clicking\
                                an area on the map below, you can view the average traffic flow, the \
                                speed limit, and types of roads. You may also view the historical data\
                                to see how traffic flow in the selected neighborhood has changed over time.')
                    ]
                ),
                # Controls
                html.Div(
                    id='controls',
                    className='six columns prettyContainer',
                    children=[
                        html.H6('Select a neighborhood:'),
                        dcc.Dropdown(
                            id='dropdown',
                            options=NBHD_OPTIONS,
                            value=92
                        ),
                        html.Br(),
                        html.H6('Select a map type:'),
                        dcc.RadioItems(
                            id='radio',
                            options=MAP_OPTIONS,
                            value='flow',
                            labelStyle={
                                'display': 'inline-block',
                                'width': '33%'
                            }
                        ),
                        # Slider
                        html.Div(
                            id='sliderContainer',
                            children=[
                                html.H6('Select a year:'),
                                dcc.Slider(
                                    id='slider',
                                    min=2007,
                                    max=2018,
                                    marks=YEAR_OPTIONS,
                                    value=2018
                                ),
                                html.Br()
                            ]
                        )
                    ]
                )
            ]
        ),
        # Row two
        html.Div(
            id='rowTwo',
            className='twelve columns',
            children=[
                # Seattle Neighborhood Map
                html.Div(
                    id='neighborhoodMapContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            className='centerTitle',
                            children='Seattle Neighborhoods'),
                        html.P('Select a neighborhood by clicking an area on the map.\
                                Use your cursor to zoom in and out.',
                                className='centerTitle'),
                        dcc.Graph(
                            id='neighborhoodMap',
                            figure=neighborhood_map(*NBHD_DATA)
                        )
                    ]
                ),
                # Traffic Flow Map
                html.Div(
                    id='trafficFlowMapContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='mapTitle',
                            className='centerTitle',
                            children='Neighborhood Roads'
                        ),
                        dcc.Graph(
                            id='trafficFlowMap',
                            figure=traffic_flow_map(
                                STREET_DATA)
                        )
                    ]
                )
            ]
        ),
        # Row three
        html.Div(
            id='rowThree',
            className='twelve columns',
            children=[
                # Traffic Flow Series
                html.Div(
                    id='trafficFlowSeriesContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='seriesTitle',
                            className='centerTitle',
                            children='Neighborhood Series'
                        ),
                        dcc.Graph(
                            id='trafficFlowSeries',
                            figure=traffic_flow_series(
                                STREET_DATA)
                        )
                    ]
                ),
                # Traffic Flow Stats
                html.Div(
                    id='trafficFlowStatsContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='statsTitle',
                            className='centerTitle',
                            children='Neighborhood Stats'
                        ),
                        html.P('This graph displays historical data about your selected neighborhood.\
                                The bolded line in the middle of each box represents the average statistic\
                                for the corresponding year.',
                                className='centerTitle'),
                        dcc.Graph(
                            id='trafficFlowStats',
                            figure=traffic_flow_stats(
                                STREET_DATA)
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


# Update traffic map title after dropdown selection
@APP.callback(
    Output('mapTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_traffic_map_title(value):
    """Update traffic map title"""
    return NAMES[value] + ' Roads'


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


# Update controls after radio selection
@APP.callback(
    Output('sliderContainer', 'style'),
    [Input('radio', 'value')]
)
def update_controls(value):
    """docstring"""
    if value == 'flow':
        return {'display': 'inline'}
    return {'display': 'none'}


# Update traffic flow series title after dropdown selection
@APP.callback(
    Output('seriesTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_traffic_series_title(value):
    """Update traffic flow series title"""
    return NAMES[value] + ' Series'


# Update traffic flow series after dropdown selection
@APP.callback(
    Output('trafficFlowSeries', 'figure'),
    [Input('dropdown', 'value')]
)
def update_traffic_flow_series(neighborhood):
    """Update traffic flow series"""
    return traffic_flow_series(STREET_DATA, neighborhood)


# Update stats title after dropdown selection
@APP.callback(
    Output('statsTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_stats_title(value):
    """Update stats title"""
    return NAMES[value] + ' Stats'


# Update traffic flow stats after dropdown selection
@APP.callback(
    Output('trafficFlowStats', 'figure'),
    [Input('dropdown', 'value')]
)
def update_traffic_flow_stats(neighborhood):
    """Update traffic flow stats"""
    return traffic_flow_stats(STREET_DATA, neighborhood)


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
        return selected_data['points'][0]['pointIndex']
    except TypeError:
        return 92


# Run dashboard
if __name__ == '__main__':
    APP.run_server(debug=True)
