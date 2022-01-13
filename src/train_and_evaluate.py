# Load Train And Test
# Create The Model
# Save The Metrics

from sklearn.metrics import mean_squared_error, mean_absolute_error,r2_score
from sklearn.ensemble import RandomForestRegressor
from get_data import read_params, get_data
from sklearn.linear_model import Ridge
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import argparse
import warnings
import joblib
import json
import sys
import os

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2

def train_and_evaluate(config_path):
    config = read_params(config_path)

    train_data_path = config["split_data"]["train_path"]
    test_data_path = config["split_data"]["test_path"]
    random_state = config["base"]["random_state"]

    model_dir = config["model_dir"]

    # alpha = config["estimators"]["Ridge"]["params"]["alpha"]
    max_depth = config["estimators"]["RandomForestRegressor"]["params"]["max_depth"]
    max_features = config["estimators"]["RandomForestRegressor"]["params"]["max_features"]
    n_estimators = config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
    # bootstrap = config["estimators"]["RandomForestRegressor"]["params"]["bootstrap"]

    target_col1 = [config["base"]["target_col1"]]
    target_col2 = [config["base"]["target_col2"]]
    
    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y1 = train[target_col1]
    test_y1 = test[target_col1]

    train_y2 = train[target_col2]
    test_y2 = test[target_col2]

    train_x = train.drop(target_col1, axis=1).drop(target_col2, axis=1)
    test_x = test.drop(target_col1, axis=1).drop(target_col2, axis=1)

    rfr = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features, 
                                bootstrap=True)

    rfr2 = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features, 
                                bootstrap=True)

    # ridge = Ridge(alpha=alpha)

    rfr.fit(train_x, train_y1)
    rfr2.fit(train_x, train_y2)

    # ridge.fit(train_x, train_y1)
    # ridge.fit(train_x, train_y2)

    predicted_qualities1 = rfr.predict(test_x)
    predicted_qualities2 = rfr2.predict(test_x)
    
    (rmse1, mae1, r21) = eval_metrics(test_y1, predicted_qualities1)
    (rmse2, mae2, r22) = eval_metrics(test_y2, predicted_qualities2)

    print("RMSE For Heating Load: %s" % rmse1)
    print("RMSE For Cooling Load: %s" % rmse2)
    print("MAE For Heating Load: %s" % mae1)
    print("MAE For Cooling Load: %s" % mae2)
    print("R2 Score For Heating Load: %s" % r21)
    print("R2 Score For Cooling Load: %s" % r22)

    scores_file = config["reports"]["scores"]
    params_file = config["reports"]["params"]

    with open(scores_file, "w") as f:
        scores = {
            "rmse1": rmse1,
            "mae1": mae1,
            "r21": r21,

            "rmse22": rmse2,
            "mae2": mae2,
            "r22": r22
        }
        json.dump(scores, f, indent=4)

    with open(params_file, "w") as f:
        scores = {
            "max_depth": max_depth,
            "max_features": max_features,
            "n_estimators": n_estimators
        }
        json.dump(scores, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    model_path2 = os.path.join(model_dir, "model2.joblib")

    joblib.dump(rfr, model_path)
    joblib.dump(rfr2, model_path2)

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)