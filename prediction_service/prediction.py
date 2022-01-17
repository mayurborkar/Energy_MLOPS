import numpy as np
import joblib
import json
import yaml
import os

params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")

class NotInRange(Exception):
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)

class NotInCols(Exception):
    def __init__(self, message="Not in cols"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    model_dir_path1 = config["webapp_model_dir"]["model1"]
    model_dir_path2 = config["webapp_model_dir"]["model2"]
    model1 = joblib.load(model_dir_path1)
    model2 = joblib.load(model_dir_path2)
    prediction1 = model1.predict(data).tolist()[0]
    prediction2 = model2.predict(data).tolist()[0]
    
    try:
        if 6 <= prediction1 <= 43 or 10 <= prediction2 <= 48:
            return prediction1, prediction2
        else:
            raise NotInRange
    except NotInRange:
        return "Unexpected Result"

def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
        return schema

def validate_input(dict_request):

    def _validate_cols(col):
        schema = get_schema()
        actual_val = schema.keys()
        if col not in actual_val:
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()
        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]):
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)

    return True

def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response

def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response" : response}
            return response

    except NotInRange as e:
        response = {"the_exected_range": get_schema(), "response": str(e) }
        return response

    except NotInCols as e:
        response = {"the_exected_cols": get_schema().keys(), "response": str(e) }
        return response


    except Exception as e:
        response = {"response": str(e) }
        return response

