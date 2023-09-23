import math
from urllib.parse import urlparse
from URLFeatureExtractor import URLFeatureExtractor
from pymongo.errors import ConnectionFailure
import requests
import os

def get_features(url):
    extractor = URLFeatureExtractor(url)
    return extractor.get_all_features()

def get_domain(url):
    return urlparse(url).netloc

def get_status(output):
    if output < 50:
        return "Risky"
    elif output < 75:
        return "Not Recommended"
    else:
        return "Safe"

def get_description(output, url):
    domain = get_domain(url)
    risky = "This website " + domain + " exhibits a concerning security profile, that could potentially impact your online security"
    average = "This website " + domain + " exhibits an ordinary security profile, with moderate but manageable risks to your online security"
    safe = "This website " + domain + " is considered safe and poses no apparent risks to your online security."
    if output < 50:
        return risky
    elif output < 75:
        return average
    else:
        return safe

def reformat_url(url):
    if not url.startswith('https://') and not url.startswith('http://'):
        url = 'https://' + url
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
    except FileNotFoundError as e:
        print("File not found: hosts.txt ", e)
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
