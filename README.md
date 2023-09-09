# Phishing Detection API

This is a Flask-based API for predicting whether a given URL is likely to be a phishing website. The API uses a pre-trained machine learning model to make predictions based on extracted URL features. It's a simple and efficient way to integrate phishing detection into your applications or services.

## Usage

1. **Endpoint**: `/predict`
   - **Method**: POST
   - **Input**: JSON object with a "url" field containing the URL to be analyzed.
   - **Output**: JSON response with the prediction result.

Example:
```json
{
    "url": "https://example.com"
}
```

The API responds with a JSON object containing the prediction result, which is a probability score indicating the likelihood of the URL being a phishing site.

Example Response:

```json
{
    "prediction": 0.92
}
```

## Setup

- Install the required Python packages listed in `requirements.txt`.
- Run the Flask application using python app.py. By default, it runs on port 8080.

## Configuration
You can configure the port number by setting the PORT environment variable.

## Dependencies
```
- Flask
- flask-cors
- pandas
- torch
- featureExtractor
```
  
Author(s): 
Priyanka A, Sivadhas S
