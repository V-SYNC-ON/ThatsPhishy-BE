import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient
from decouple import config
from utils.ModelUtils import get_prediction
from utils.URLUtils import get_description, get_domain, get_status, reformat_url, url_exists,is_mongodb_alive,present_in_hosts,normalize
import random
app = Flask(__name__)
CORS(app)
mongo_uri = config('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['thatsPhisy'] 
collection = db['cache']  

@app.route('/predict', methods=['POST'])
def predict():
    try:
        response = {}
        data = request.get_json()
        url = data.get('url')
        url=reformat_url(url)
        domain_name=get_domain(url)
        if present_in_hosts(domain_name)==True :
            output=0
            status = get_status(output)
            description = get_description(output, url)
            response = {
                'prediction': output,
                'domain': domain_name,
                'status': status,
                'description': description
            }
            return make_response(jsonify(response), 200)

        if(url_exists(url)==False) :
            return make_response(jsonify({"error": "The URL doesn't exist "}), 400)
        
        response = collection.find_one({'domain': domain_name})
        if not response:
            output =  normalize(get_prediction(url))

            status = get_status(output)
            description = get_description(output, url)
            response = {
                'prediction': output,
                'domain': domain_name,
                'status': status,
                'description': description
            }
            collection.insert_one(response)
        response.pop('_id', None)
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        return make_response(jsonify({'Error': 'Something Went Wrong'}), 500)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    if(is_mongodb_alive(client)==False):
        print("error connecting to db")
        exit(1)
    app.run(host='0.0.0.0', port=port)
