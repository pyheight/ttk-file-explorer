import threading
import requests  
import webbrowser
from markdown import markdown  
from bs4 import BeautifulSoup 

from model.builtin_transform import convert_date_iso
from model.config_loader import get_text
from constants.information import VERSION, ENDPOINT, WEBSITE
from view.box import MessageBox as messagebox


def is_valid_url(url):  
    try:  
        response = requests.head(url)  
        return response.status_code == requests.codes.ok  
    except requests.RequestException:  
        return False  


def get_latest_release():
    try:  
        response = requests.get(ENDPOINT)  
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def open_web(url):
    def _open_web():
        try:
            webbrowser.open(url)
        except Exception:
            messagebox.error(f"{get_text('cannot_open')} {url}")

    thread = threading.Thread(target=_open_web)
    thread.start()


def get_update():
    latest_release = get_latest_release()  
    if not latest_release:  
        return None  
  
    get_version = latest_release.get('tag_name', '')  
    if get_version == VERSION:  
        return False  
  
    publish_time = convert_date_iso(latest_release.get('published_at', ''))  
    assets = latest_release.get('assets', [])  
    download_urls = [asset.get('browser_download_url') for asset in assets if asset.get('browser_download_url') and asset.get('browser_download_url').endswith('.exe')]  
  
    if len(download_urls) != 1:  
        download_url = latest_release.get('html_url', WEBSITE)  
    else:  
        download_url = download_urls[0]  

    soup = BeautifulSoup(markdown(latest_release.get('body', '')), 'html.parser')  
    text = soup.get_text(separator='\n', strip=True)  
  
    return {  
        'title': get_version,  
        'time': publish_time,  
        'download_url': download_url,  
        'text': text,  
    }
