"""Load Seattle neighborhoods datasets and reformat for dashboard."""
import json
import os
import pickle


def prep_map_data(json_path, data_path):
    """Prepare neighborhood map dataset

    Load, reformat, and save neighborhood map dataset into lists
    required for Plotly choropleth map. Raises FileNotFoundError if
    file at json_path does not exist, and overwrites file at data_path
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


if __name__ == '__main__':
    # Create directory for cleaned data if none exists
    if not os.path.exists('cleaned'):
        os.mkdir('cleaned')

    # Paths to raw and cleaned datasets
    JSON_PATH = 'raw/zillow-neighborhoods/zillow-neighborhoods.geojson'
    DATA_PATH = 'cleaned/nbhd_data.pkl'

    # Prepare data
    prep_map_data(JSON_PATH, DATA_PATH)
