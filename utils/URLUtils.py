import math
from urllib.parse import urlparse
from URLFeatureExtractor import URLFeatureExtractor
from pymongo.errors import ConnectionFailure
import requests
import os
from utils.ResponseText  import statuses,generate_description


def get_features(url):
    extractor = URLFeatureExtractor(url)
    return extractor.get_all_features()

def get_domain(url):
    return urlparse(url).netloc

def get_status(language,prediction):
    if prediction < 50:
        return statuses[language]["risky"]
    elif prediction < 75:
        return statuses[language]["not recommended"]
    else:
        return statuses[language]["safe"]

def get_description(language,prediction,domain):
    if prediction < 50:
        return generate_description(language, "risky", domain)
    elif prediction < 75:
        return generate_description(language, "not recommended", domain)
    else:
        return generate_description(language, "safe", domain)

def reformat_url(url):
    if not url.startswith('https://') and not url.startswith('http://'):
        url = 'https://' + url
    parts = url.split('//')
    if len(parts) == 2:
        domain = parts[1]
        domain_parts = domain.split('.')
        if len(domain_parts) == 2:
            url = url.replace('//', '//www.')
    
    return url
    
def url_exists(url):
    try:
        domain = urlparse(url).netloc
        parsed_url = 'https://' + domain
        response = requests.get(parsed_url, timeout=5)
        if response.status_code != 404:
            return True
        else:
            print(response)
            return False
    except requests.exceptions.RequestException as e:
        print(e)
        return False

def is_mongodb_alive(client):
    try:
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        return False
    
set_url=set()
def load_urls_into_set():
    relative='utils/hosts.txt'
    absolute_path = os.path.abspath(relative)
    try:
        with open(absolute_path, 'r') as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        print("File not found: hosts.txt ")
        return set()

def present_in_hosts(url):
    global set_url 
    if not set_url:
        set_url = load_urls_into_set()
    return url in set_url

def normalize(val):
    if val <= 50:
        normalized_val = 20 + ((val - 1) / 49) * 30
    else:
        normalized_val = val
    return round(normalized_val)

def get_response(language,prediction,domain):
    response={
        "prediction":prediction,
        "status":get_status("English",prediction),
        "language-status":get_status(language,prediction),
        "description":get_description(language,prediction,domain),
        "domain":domain,
    }
    return response

def something_went_wrong(language):
    return generate_description(language, "error", "")
def url_doesnt_exist(language):
    return generate_description(language, "not_found", "")
