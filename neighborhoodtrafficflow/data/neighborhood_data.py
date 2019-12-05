"""Load Seattle neighborhoods datasets and reformat for dashboard."""
import csv
import json
import os
import pickle

import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon


def prep_map_data(json_path, data_path):
    """Prepare neighborhood map dataset.

    Load, reformat, and save neighborhood map dataset into lists
    required for Plotly choropleth map. Raises FileNotFoundError if
    file at json_path does not exist and overwrites file at data_path
    if already exists.

    Parameters
    ----------
    json_path : str
        Path to neighborhood geojson file.
    data_path : str
        Path to neighborhood pkl file.

    Returns
    -------
    out : None

    Raises
    ------
    FileNotFoundError : No such file or directory
        If file at json_path does not exist.
    """
    # Import neighborhood geojson file
    with open(json_path) as json_file:
        nbhd_json = json.load(json_file)

    # Add ids for choropleth map
    for feature in nbhd_json['features']:
        feature['id'] = feature['properties']['regionid']

    # Create lists for choropleth map
    num_nbhds = len(nbhd_json['features'])
    region_ids = [feature['properties']['regionid']
                  for feature in nbhd_json['features']]
    nbhd_names = [feature['properties']['name']
                  for feature in nbhd_json['features']]
    nbhd_data = [num_nbhds, nbhd_json, region_ids, nbhd_names]

    # Save list
    with open(data_path, 'wb+') as pickle_file:
        pickle.dump(nbhd_data, pickle_file)


def prep_map_info(shp_path, info_path):
    """Prepare neighborhood info dataset.

    Load, reformat, and save neighborhood info dataset to be used by
    various functions in figures.py module. Raises FileNotFoundError if
    file at shp_path does not exist and overwrites file at info_path if
    already exists.

    Parameters
    ----------
    shp_path : str
        Path to neighborhood shp file.
    info_path : str
        Path to neighborhood csv file.

    Returns
    -------
    out : None

    Raises
    ------
    FileNotFoundError : No such file or directory
        If file at shp_path does not exist.
    """
    # Import neighborhood shape file
    nbhd_json = gpd.read_file(shp_path)

    # Read shape file and write csv file
    with open(info_path, 'w+') as csv_file:
        file_writer = csv.writer(csv_file, delimiter=',')
        file_writer.writerow(['name', 'minLon', 'midLon', 'maxLon', 'minLat',
                              'midLat', 'maxLat'])

        # Extract names, centroids, and bounds
        for _, row in nbhd_json.iterrows():

            # Get polygon
            try:
                polygon = Polygon(row['geometry'])
            except NotImplementedError:
                polygon = MultiPolygon(row['geometry'])
            bounds = polygon.bounds

            # Write row
            file_writer.writerow([row['name'], bounds[0], polygon.centroid.x,
                                  bounds[2], bounds[1], polygon.centroid.y,
                                  bounds[3]])


if __name__ == '__main__':
    # Create directory for cleaned data if none exists
    if not os.path.exists('cleaned'):
        os.mkdir('cleaned')

    # Paths to raw and cleaned datasets
    JSON_PATH = 'raw/zillow-neighborhoods/zillow-neighborhoods.geojson'
    SHP_PATH = 'raw/zillow-neighborhoods/zillow-neighborhoods.shp'
    DATA_PATH = 'cleaned/nbhd_data.pkl'
    INFO_PATH = 'cleaned/nbhd_info.csv'

    # Prepare data
    prep_map_data(JSON_PATH, DATA_PATH)
    prep_map_info(SHP_PATH, INFO_PATH)
