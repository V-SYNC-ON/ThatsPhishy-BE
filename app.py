import os

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

from utils.ModelUtils import get_prediction
from utils.URLUtils import get_description, get_domain, get_status, reformat_url, url_exists

app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url')
        url=reformat_url(url)
        if(url_exists(url)==False) :
            return make_response(jsonify({"error": "The URL doesn't exist "}), 400)

        output=get_prediction(url)
        domain_name=get_domain(url)
        status=get_status(output)
        description=get_description(output,url)
        response = {
            'prediction': output,
            'domain':domain_name,
            'status':status,
            'description':description
        }
        return make_response(jsonify(response),200)
    except Exception as e:
        print("ERROR: ",e)
        return make_response(jsonify({'Error': 'Something Went Wrong'}), 500)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
