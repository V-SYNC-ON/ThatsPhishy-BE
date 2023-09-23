import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from pymongo import MongoClient
from decouple import config
from utils.ModelUtils import get_prediction
from utils.URLUtils import  get_domain,  reformat_url, url_exists,is_mongodb_alive,present_in_hosts,normalize
from utils.URLUtils import get_response,url_doesnt_exist,something_went_wrong
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
        data = request.get_json()
        url = data.get('url')
        language=data.get('language')

        if present_in_hosts(url)==True :
            print("in hosts")
            response=get_response(language,0,url)
            return make_response(jsonify(response), 200)
        
        url=reformat_url(url)
        domain=get_domain(url)

        if(url_exists(url)==False) :
            return make_response(jsonify({"error": url_doesnt_exist(language)}), 400)

        cached = collection.find_one({"domain":domain})
        if cached:
            prediction=cached["prediction"]
        else:

            prediction =  normalize(get_prediction(url))
            print(prediction)
            collection.insert_one({
                "prediction":prediction,
                "domain":domain,
            })
        response=get_response(language,prediction,domain)
        return make_response(jsonify(response), 200)
    
    except Exception as e:
        print(e)
        return make_response(jsonify({'Error': something_went_wrong(language)}), 500)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    if(is_mongodb_alive(client)==False):
        print("error connecting to db")
        exit(1)
    app.run(host='0.0.0.0', port=port)
