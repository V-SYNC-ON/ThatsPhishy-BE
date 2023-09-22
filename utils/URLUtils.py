from urllib.parse import urlparse
from URLFeatureExtractor import URLFeatureExtractor
from pymongo.errors import ConnectionFailure
import requests

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
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def is_mongodb_alive(client):
    try:
        client.admin.command('ping')
        return True
    except ConnectionFailure:
        return False