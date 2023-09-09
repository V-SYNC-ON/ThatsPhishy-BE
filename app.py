import os

from flask import Flask, request, jsonify
from flask_cors import CORS

import pandas as pd
import torch
import torch.nn as nn

from URLFeatureExtractor import URLFeatureExtractor

app = Flask(__name__)
CORS(app)

with open("scaler.pkl", "rb") as scaler_file:
   scaler = torch.load(scaler_file, map_location=torch.device('cpu'))

class MLP(nn.Module):
    def __init__(self,dropout=0.4):
        super(MLP,self).__init__()
        self.network=nn.Sequential(
            nn.Linear(in_features=55,out_features=300), 
            nn.ReLU(),
            nn.BatchNorm1d(num_features=300),
            nn.Dropout(p=dropout),
            
            nn.Linear(in_features=300,out_features=100),
            nn.ReLU(),
            nn.BatchNorm1d(num_features=100),
            
            nn.Linear(in_features=100,out_features=1),
            nn.Sigmoid()
        )
    def forward(self,x):
        x=self.network(x)
        return x
    
def getFeaturesOfUrl(url):
    extractor = URLFeatureExtractor(url)
    return extractor.get_all_features()

model = MLP(dropout=0.4)
model.load_state_dict(torch.load("phishing_model.pkl", map_location=torch.device('cpu')))
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = data.get('url')

        input_data=getFeaturesOfUrl(url)

        input_data_scaled = scaler.transform(pd.DataFrame(input_data))
        input_tensor = torch.Tensor(input_data_scaled)

        with torch.no_grad():
            output = model(input_tensor).item()

        response = {
            'prediction': output
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
