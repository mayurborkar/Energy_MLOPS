# Read Data From Data Source
# Save It Into Data/raw & Data/processed Folder

from get_data import read_params, get_data
import argparse
import  os

def load_and_save(config_path):
    config = read_params(config_path)
    data = get_data(config_path)

    data.drop(['ID'], axis=1, inplace=True)

    data=data.set_axis(['relative_compactness', 'surface_area', 'wall_area', 'roof_area', 'overall_height', 
                    'orientation', 'glazing_area', 'glazing_area_distribution','heating_load','cooling_load'],
                    axis=1)

    raw_data_path = config["load_data"]["raw_dataset_csv"]

    data.to_csv(raw_data_path, sep=",", index=False)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)
