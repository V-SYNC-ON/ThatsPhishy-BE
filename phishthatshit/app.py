from flask import Flask, request, jsonify
import numpy as np
import pickle
from FeatureExtractor import FeatureExtraction
import os

file = open("random_forest.pkl","rb")
forest = pickle.load(file)
file.close()

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            url = request.form["url"]
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1, 30)

            y_pred = forest.predict(x)[0]
            # 1 is safe, -1 is unsafe
            y_pro_phishing = forest.predict_proba(x)[0, 0]
            y_pro_non_phishing = forest.predict_proba(x)[0, 1]

            # Prepare the response data as a dictionary
            response_data = {
                "prediction": int(y_pred),
                "phishing_probability": round(y_pro_phishing * 100, 2),
                "non_phishing_probability": round(y_pro_non_phishing * 100, 2),
            }

            return jsonify(response_data)

        except Exception as e:
            error_message = str(e)
            response_data = {
                "error": error_message
            }
            return jsonify(response_data), 400  # Return a 400 Bad Request status code for errors

if __name__ == "__main__":
    app.run(debug=True)