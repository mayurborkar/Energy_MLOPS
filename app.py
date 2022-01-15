from flask import Flask, request, render_template, jsonify
import numpy as np
import yaml
import joblib
import os

params_path = "params.yaml"
webapp_root = "webapp"

static_path = os.path.join(webapp_root, "static")
template_path = os.path.join(webapp_root, "templates")


app = Flask(__name__, static_folder=static_path, template_folder=template_path)


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
    prediction1 = model1.predict(data)
    prediction2 = model2.predict(data)
    print(prediction1)
    print(prediction2)
    return prediction1[0], prediction2[0]


def api_response(request):
    try:
        data = np.array([list(request.json.values())])
        response = predict(data)
        response = {"response": response}
        return response
    except Exception as e:
        print(e)
        error = {"error": "Something Went Wrong!! Try Again"}
        return error


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if request.form:
                data = dict(request.form).values()
                data = [list(map(float, data))]
                response = predict(data)
                return render_template("index.html", response=response)

            elif request.json:
                response = api_response(request)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error": "Something Went Wrong!! Try Again"}
            return render_template("404.html", error=error)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
