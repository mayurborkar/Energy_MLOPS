from flask import Flask, request, render_template, jsonify
from prediction_service import prediction
import os

webapp_root = "webapp"

static_path = os.path.join(webapp_root, "static")
template_path = os.path.join(webapp_root, "templates")


app = Flask(__name__, static_folder=static_path, template_folder=template_path)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if request.form:
                data_req = dict(request.form)
                response = prediction.form_response(data_req)
                return render_template("index.html", response=response)

            elif request.json:
                response = prediction.api_response(request.json)
                return jsonify(response)

        except Exception as e:
            print(e)
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
