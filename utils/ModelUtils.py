import pandas as pd
from MLModel import MLP
import torch
import torch.nn as nn
from utils.URLUtils import get_features

def get_prediction(url):

    model=run_model()
    scaler=preprocess()
    input_data=get_features(url)
    input_data_scaled = scaler.transform(pd.DataFrame(input_data))
    input_tensor = torch.Tensor(input_data_scaled)
    with torch.no_grad():
        output = 100-(round(model(input_tensor).item()*100))
    return output

def run_model():
    model = MLP(dropout=0.4)
    model.load_state_dict(torch.load("phishing_model.pkl", map_location=torch.device('cpu')))
    model.eval()
    return model

def preprocess():
    with open("scaler.pkl", "rb") as scaler_file:
        scaler = torch.load(scaler_file, map_location=torch.device('cpu'))
    return scaler