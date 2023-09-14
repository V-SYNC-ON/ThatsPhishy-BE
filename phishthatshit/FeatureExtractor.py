import ipaddress
import re
import urllib.request
import socket
import requests
from googlesearch import search
import whois
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import date

class FeatureExtraction:
    def __init__(self, url):
        self.url = url
        self.domain = ""
        self.whois_response = None
        self.response = None
        self.soup = None
        self.features = []

        try:
            self.response = requests.get(url)
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
        except requests.exceptions.RequestException:
            pass

        try:
            self.urlparse = urlparse(url)
            self.domain = self.urlparse.netloc
        except:
            pass

        try:
            self.whois_response = whois.whois(self.domain)
        except:
            pass

    def extract_features(self):
        self.features.append(self.using_ip())
        self.features.append(self.long_url())
        self.features.append(self.short_url())
        self.features.append(self.symbol())
        self.features.append(self.redirecting())
        self.features.append(self.prefix_suffix())
        self.features.append(self.subdomains())
        self.features.append(self.https())
        self.features.append(self.domain_reg_len())
        self.features.append(self.favicon())
        self.features.append(self.non_std_port())
        self.features.append(self.https_domain_url())
        self.features.append(self.request_url())
        self.features.append(self.anchor_url())
        self.features.append(self.links_in_script_tags())
        self.features.append(self.server_form_handler())
        self.features.append(self.info_email())
        self.features.append(self.abnormal_url())
        self.features.append(self.website_forwarding())
        self.features.append(self.status_bar_cust())
        self.features.append(self.disable_right_click())
        self.features.append(self.using_popup_window())
        self.features.append(self.iframe_redirection())
        self.features.append(self.age_of_domain())
        self.features.append(self.dns_recording())
        self.features.append(self.website_traffic())
        self.features.append(self.page_rank())
        self.features.append(self.google_index())
        self.features.append(self.links_pointing_to_page())
        self.features.append(self.stats_report())

    def using_ip(self):
        try:
            ipaddress.ip_address(self.url)
            return -1
        except ValueError:
            return 1

    def long_url(self):
        if len(self.url) < 54:
            return 1
        elif 54 <= len(self.url) <= 75:
            return 0
        else:
            return -1

    def short_url(self):
        short_url_patterns = [
            'bit\.ly', 'goo\.gl', 'shorte\.st', 'go2l\.ink', 'x\.co', 'ow\.ly', 't\.co', 'tinyurl', 'tr\.im',
            'is\.gd', 'cli\.gs', 'yfrog\.com', 'migre\.me', 'ff\.im', 'tiny\.cc', 'url4\.eu', 'twit\.ac', 'su\.pr',
            'twurl\.nl', 'snipurl\.com', 'short\.to', 'BudURL\.com', 'ping\.fm', 'post\.ly', 'Just\.as', 'bkite\.com',
            'snipr\.com', 'fic\.kr', 'loopt\.us', 'doiop\.com', 'short\.ie', 'kl\.am', 'wp\.me', 'rubyurl\.com',
            'om\.ly', 'to\.ly', 'bit\.do', 'lnkd\.in', 'db\.tt', 'qr\.ae', 'adf\.ly', 'goo\.gl', 'bitly\.com', 'cur\.lv',
            'tinyurl\.com', 'ow\.ly', 'bit\.ly', 'ity\.im', 'q\.gs', 'is\.gd', 'po\.st', 'bc\.vc', 'twitthis\.com',
            'u\.to', 'j\.mp', 'buzurl\.com', 'cutt\.us', 'u\.bb', 'yourls\.org', 'x\.co', 'prettylinkpro\.com',
            'scrnch\.me', 'filoops\.info', 'vzturl\.com', 'qr\.net', '1url\.com', 'tweez\.me', 'v\.gd', 'tr\.im',
            'link\.zip\.net'
        ]
        for pattern in short_url_patterns:
            if re.search(pattern, self.url):
                return -1
        return 1

    def symbol(self):
        if '@' in self.url:
            return -1
        return 1

    def redirecting(self):
        if self.url.rfind('//') > 6:
            return -1
        return 1

    def prefix_suffix(self):
        if '-' in self.domain:
            return -1
        return 1

    def subdomains(self):
        dot_count = len(re.findall(r'\.', self.url))
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1

    def https(self):
        if 'https' in self.urlparse.scheme:
            return 1
        return -1

    def domain_reg_len(self):
        try:
            expiration_date = self.whois_response.expiration_date
            creation_date = self.whois_response.creation_date
            if len(expiration_date):
                expiration_date = expiration_date[0]
            if len(creation_date):
                creation_date = creation_date[0]
            age = (expiration_date.year - creation_date.year) * 12 + (expiration_date.month - creation_date.month)
            if age >= 12:
                return 1
            return -1
        except AttributeError:
            return -1

    def favicon(self):
        try:
            for head in self.soup.find_all('head'):
                for head_link in self.soup.find_all('link', href=True):
                    dots = [x.start(0) for x in re.finditer('\.', head_link['href'])]
                    if self.url in head_link['href'] or len(dots) == 1 or self.domain in head_link['href']:
                        return 1
            return -1
        except:
            return -1

    def non_std_port(self):
        try:
            port = self.domain.split(":")
            if len(port) > 1:
                return -1
            return 1
        except:
            return -1

    def https_domain_url(self):
        if 'https' in self.domain:
            return -1
        return 1

    def request_url(self):
        try:
            elements = self.soup.find_all(['img', 'audio', 'embed', 'iframe'], src=True)
            success = 0
            i = 0
            for element in elements:
                dots = [x.start(0) for x in re.finditer('\.', element['src'])]
                if self.url in element['src'] or self.domain in element['src'] or len(dots) == 1:
                    success += 1
                i += 1
            percentage = success / float(i) * 100
            if percentage < 22.0:
                return 1
            elif 22.0 <= percentage < 61.0:
                return 0
            else:
                return -1
        except:
            return -1

    def anchor_url(self):
        try:
            i, unsafe = 0, 0
            elements = self.soup.find_all('a', href=True)
            for element in elements:
                href = element['href'].lower()
                if "#" in href or "javascript" in href or "mailto" in href or not (self.url in href or self.domain in href):
                    unsafe += 1
                i += 1
            percentage = unsafe / float(i) * 100
            if percentage < 31.0:
                return 1
            elif 31.0 <= percentage < 67.0:
                return 0
            else:
                return -1
        except:
            return -1

    def links_in_script_tags(self):
        try:
            i, success = 0, 0
            elements = self.soup.find_all(['link', 'script'], href=True)
            for element in elements:
                dots = [x.start(0) for x in re.finditer('\.', element['href'])]
                if self.url in element['href'] or self.domain in element['href'] or len(dots) == 1:
                    success += 1
                i += 1
            percentage = success / float(i) * 100
            if percentage < 17.0:
                return 1
            elif 17.0 <= percentage < 81.0:
                return 0
            else:
                return -1
        except:
            return -1

    def server_form_handler(self):
        try:
            if len(self.soup.find_all('form', action=True)) == 0:
                return 1
            else:
                for form in self.soup.find_all('form', action=True):
                    if form['action'] == "" or form['action'] == "about:blank":
                        return -1
                    elif self.url not in form['action'] and self.domain not in form['action']:
                        return 0
                    else:
                        return 1
        except:
            return -1

    def info_email(self):
        try:
            if re.findall(r"[mail\(\)|mailto:?]", str(self.soup)):
                return -1
            else:
                return 1
        except:
            return -1

    def abnormal_url(self):
        try:
            if self.response.text == str(self.whois_response):
                return 1
            else:
                return -1
        except:
            return -1

    def website_forwarding(self):
        try:
            if len(self.response.history) <= 1:
                return 1
            elif 1 < len(self.response.history) <= 4:
                return 0
            else:
                return -1
        except:
            return -1

    def status_bar_cust(self):
        try:
            if re.findall("<script>.+onmouseover.+</script>", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def disable_right_click(self):
        try:
            if re.findall(r"event.button ?== ?2", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def using_popup_window(self):
        try:
            if re.findall(r"alert\(", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def iframe_redirection(self):
        try:
            if re.findall(r"<iframe>|<frameBorder>", self.response.text):
                return 1
            else:
                return -1
        except:
            return -1

    def age_of_domain(self):
        try:
            creation_date = self.whois_response.creation_date
            if len(creation_date):
                creation_date = creation_date[0]
            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1
        except:
            return -1

    def dns_recording(self):
        try:
            creation_date = self.whois_response.creation_date
            if len(creation_date):
                creation_date = creation_date[0]
            today = date.today()
            age = (today.year - creation_date.year) * 12 + (today.month - creation_date.month)
            if age >= 6:
                return 1
            return -1
        except:
            return -1

    def website_traffic(self):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + self.url).read(), "xml").find("REACH")['RANK']
            if int(rank) < 100000:
                return 1
            return 0
        except:
            return -1

    def page_rank(self):
        try:
            rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": self.domain})
            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            if 0 < global_rank < 100000:
                return 1
            return -1
        except:
            return -1

    def google_index(self):
        try:
            site = search(self.url, 5)
            if site:
                return 1
            else:
                return -1
        except:
            return 1

    def links_pointing_to_page(self):
        try:
            number_of_links = len(re.findall(r"<a href=", self.response.text))
            if number_of_links == 0:
                return 1
            elif 0 < number_of_links <= 2:
                return 0
            else:
                return -1
        except:
            return -1


    # 30. StatsReport
    def StatsReport(self):
        try:
            url_match = re.search(
        'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', self.url)
            ip_address = socket.gethostbyname(self.domain)
            ip_match = re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                                '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                                '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                                '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                                '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                                '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match:
                return -1
            elif ip_match:
                return -1
            return 1
        except:
            return 1
    
    def getFeaturesList(self):
        return self.features