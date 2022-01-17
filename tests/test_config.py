from prediction_service.prediction import form_response, api_response
import prediction_service
import logging
import pytest
import joblib
import json
import os

input_data = {
    "incorrect_range": 
    {"relative_compactness": 1.0, 
    "surface_area": 1000.0, 
    "wall_area": 417.0, 
    "roof_area": 221.0, 
    "overall_height": 8.0, 
    "orientation": 6.0, 
    "glazing_area": 0.5, 
    "glazing_area_distribution":6.0, 
    },

    "correct_range":
    {"relative_compactness": 0.78, 
    "surface_area": 555.5, 
    "wall_area": 350.5, 
    "roof_area": 210.5, 
    "overall_height":4.5, 
    "orientation": 4.0, 
    "glazing_area": 0.3, 
    "glazing_area_distribution": 4.0, 
    },

    "incorrect_col":
    {"relative compactness": 0.78, 
    "surface area": 555.5, 
    "wall area": 350.5, 
    "roof area": 210.5, 
    "overall height": 12, 
    "orientation": 4.0, 
    "glazing area": 0.3, 
    "glazing area distribution": 4.0,
    "alcohol" : 42.0
    },
}

TARGET_range1 = {
    "min": 6.01,
    "max": 43.1
}

TARGET_range2 = {
    "min": 10.9,
    "max": 48.03
}

def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert  TARGET_range1["min"] <= res <= TARGET_range1["max"]
    assert  TARGET_range2["min"] <= res <= TARGET_range2["max"]

def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert  TARGET_range1["min"] <= res["response"] <= TARGET_range1["max"]
    assert  TARGET_range2["min"] <= res["response"] <= TARGET_range2["max"]

def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)

def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message

def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message
