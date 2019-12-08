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

from neighborhoodtrafficflow.figures.maps import \
    neighborhood_map, road_map
from neighborhoodtrafficflow.figures.charts import \
    traffic_flow_counts, speed_limits, road_types

# Data file paths
CWD = Path(__file__).parent
NBHD_PATH = CWD / 'data/cleaned/nbhd_data.pkl'
STREET_PATH = CWD / 'data/cleaned/street_data.pkl'

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

# Descriptions
APP_DESCRIPTION = 'This is an interactive dashboard for current and future \
                  Seattle residents to understand the traffic flow of \
                  neighborhoods in the city. By clicking an area on the map \
                  below, you can view the average traffic flow, the speed \
                  limit, and types of roads. You may also view the \
                  historical data to see how traffic flow in the selected \
                  neighborhood has changed over time.'
NBHD_DESCRIPTION = 'Select a neighborhood by clicking an area on the map. \
                    Use your cursor to zoom in and out.'
FLOW_DESCRIPTION = 'This graph displays historical data about your selected \
                    neighborhood. The bolded line in the middle of each box \
                    represents the average statistic for the corresponding \
                    year.'
FLOWMAP_DESCRIPTION = 'This map represents data from your selected neighborhood.'
SPEED_LIMITS_DESCRIPTION = 'This chart displays the percentage of roads with all speed limits \
                            in your selected neighborhood. The neighborhood information is \
                            displayed in blue. This is compared to the city of Seattle \
                            which is displayed in gray.'
NBHD_RDTYPES_DESCRIPTION = 'This chart displays the percentage of road types in your \
                            selected neighborhood. The neighborhood information is \
                            displayed in blue. This is compared to the city of Seattle \
                            which is displayed in gray.'

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
                            'CSE 583: Software Engineering for \
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
                        html.H5(
                            className='centerTitle',
                            children='About This App'
                        ),
                        html.P(APP_DESCRIPTION)
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
                        html.P(
                            children=NBHD_DESCRIPTION
                        ),
                        dcc.Graph(
                            id='neighborhoodMapFigure',
                            figure=neighborhood_map(*NBHD_DATA)
                        )
                    ]
                ),
                # Neighborhood Road Map
                html.Div(
                    id='roadMapContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='roadMapTitle',
                            className='centerTitle',
                            children='Neighborhood Roads'
                        ),
                        dcc.Graph(
                            id='roadMapFigure',
                            figure=road_map(STREET_DATA)
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
                # Flow Count Bar Chart
                html.Div(
                    id='flowCountContainer',
                    className='twelve columns prettyContainer',
                    children=[
                        html.H4(
                            id='flowCountTitle',
                            className='centerTitle',
                            children='Neighborhood Flow Counts'
                        ),
                        html.P(FLOW_DESCRIPTION),
                        dcc.Graph(
                            id='flowCountFigure',
                            figure=traffic_flow_counts(STREET_DATA)
                        )
                    ]
                )
            ]
        ),
        # Row four
        html.Div(
            id='rowFour',
            className='twelve columns',
            children=[
                # Speed Limit Histogram
                html.Div(
                    id='speedLimitContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='speedLimitTitle',
                            className='centerTitle',
                            children='Neighborhood Speed Limits'
                        ),
                        html.P(SPEED_LIMITS_DESCRIPTION),
                        dcc.Graph(
                            id='speedLimitFigure',
                            figure=speed_limits(STREET_DATA)
                        )
                    ]
                ),
                # Road Type Histogram
                html.Div(
                    id='roadTypeContainer',
                    className='six columns prettyContainer',
                    children=[
                        html.H4(
                            id='roadTypeTitle',
                            className='centerTitle',
                            children='Neighborhood Road Types'
                        ),
                        html.P(NBHD_RDTYPES_DESCRIPTION),
                        dcc.Graph(
                            id='roadTypeFigure',
                            figure=road_types(STREET_DATA)
                        )
                    ]
                )
            ]
        )
    ]
)


#########################
# Update section titles #
#########################

# Update neighborhood road map title after dropdown selection
@APP.callback(
    Output('roadMapTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_road_map_title(neighborhood):
    """Update neighborhood road map title."""
    return NAMES[neighborhood] + ' Roads'

# Update traffic flow count title after dropdown selection
@APP.callback(
    Output('flowCountTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_flow_count_title(neighborhood):
    """Update flow count title."""
    return NAMES[neighborhood] + ' Flow Counts'

# Update speed limit title after dropdown selection
@APP.callback(
    Output('speedLimitTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_speed_limit_title(neighborhood):
    """Update speed limit title."""
    return NAMES[neighborhood] + ' Speed Limits'

# Update road type title after dropdown selection
@APP.callback(
    Output('roadTypeTitle', 'children'),
    [Input('dropdown', 'value')]
)
def update_road_type_title(neighborhood):
    """Update road type title."""
    return NAMES[neighborhood] + ' Road Types'


##########################
# Update controls status #
##########################

# Update dropdown after Seattle neighborhood map selection
@APP.callback(
    Output('dropdown', 'value'),
    [Input('neighborhoodMapFigure', 'selectedData')]
)
def update_dropdown(selected_data):
    """Update dropdown after neighborhood map selection.

    Update dropdown menu status after neighborhood map selection is
    made. If TypeError, returns '92' (University District).

    Parameters
    ----------
    selected_data : dict
        Selected data in neighborhood map.

    Returns
    -------
    neighborhood : int
        Index of selected neighborhood (0-102).
    """
    try:
        return selected_data['points'][0]['pointIndex']
    except TypeError:
        return 92

# Update slider after radio selection
@APP.callback(
    Output('sliderContainer', 'style'),
    [Input('radio', 'value')]
)
def update_controls(map_type):
    """Update slider after radio selection.

    Update slider after radio selection. If 'flow' selected, show
    slider. If 'speed' or 'road' selected, hide slider.

    Parameters
    ----------
    map_type : str
        Currently selected map type from radio.

    Returns
    -------
    out : dict
        CSS for slider status.
    """
    if map_type == 'flow':
        return {'display': 'inline'}
    return {'display': 'none'}


##################
# Update figures #
##################

# Update Seattle neighborhood map after dropdown selection
@APP.callback(
    Output('neighborhoodMapFigure', 'figure'),
    [Input('dropdown', 'value')]
)
def update_neighborhood_map(neighborhood):
    """Update Seattle neighborhood map.

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

# Update neighborhood road map after dropdown, radio, or slider selection
@APP.callback(
    Output('roadMapFigure', 'figure'),
    [Input('dropdown', 'value'),
     Input('radio', 'value'),
     Input('slider', 'value')]
)
def update_road_map(neighborhood, map_type, year):
    """Update neighborhood road map.

    Update road map after a dropdown, radio, or slider selection is
    made. Also triggered by neighborhood map selection via dropdown
    callback.

    Parameters
    ----------
    neighborhood : int
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
    return road_map(STREET_DATA, neighborhood, map_type, year)

# Update traffic flow count figure after dropdown selection
@APP.callback(
    Output('flowCountFigure', 'figure'),
    [Input('dropdown', 'value')]
)
def update_traffic_flow_counts(neighborhood):
    """Update traffic flow count figure.

    Update traffic flow count bar chart after a dropdown selection is
    made. Also triggered by neighborhood map selection via dropdown
    callback.

    Parameters
    ----------
    neighborhood: int
        Currently selected neighborhood (0-102)

    Returns
    -------
    figure : dict
        Plotly bars figure.
    """
    return traffic_flow_counts(STREET_DATA, neighborhood)

# Update speed limit figure after dropdown selection
@APP.callback(
    Output('speedLimitFigure', 'figure'),
    [Input('dropdown', 'value')]
)
def update_speed_limits(neighborhood):
    """Update speed limits figure.

    Update speed limits histogram after a dropdown selection is made.
    Also triggered by neighborhood map selection via dropdown callback.

    Parameters
    ----------
    neighborhood : int
        Currently selected neighborhood (0-102).

    Returns
    -------
    figure : dict
        Plotly histogram figure.
    """
    return speed_limits(STREET_DATA, neighborhood)

# Update road type figure after dropdown selection
@APP.callback(
    Output('roadTypeFigure', 'figure'),
    [Input('dropdown', 'value')]
)
def update_road_types(neighborhood):
    """Update road types figure.

    Update road types histogram after a dropdown selection is made.
    Also triggered by neighborhood map selection via dropdown callback.

    Parameters
    ----------
    neighborhood : int
        Currently selected neighborhood (0-102).

    Returns
    -------
    figure : dict
        Plotly histogram figure.
    """
    return road_types(STREET_DATA, neighborhood)


# Run dashboard
if __name__ == '__main__':
    APP.run_server(debug=True)
