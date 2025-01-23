import requests
import json
from playwright.sync_api import sync_playwright

class Serper:
    def __init__(self, api_key):
        self.base_url = "https://google.serper.dev/"
        print(f"USING API KEY = ", api_key)
        self.headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
        }

    def search_images(self, query, num_results=50):
        url = f"{self.base_url}/images"
        try:
            payload = json.dumps({
            "q": query,
            "num": num_results
            })
            response = requests.post(url, headers=self.headers, data=payload)
            
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_discover(self, query, num_results=10):
        
        url = f"{self.base_url}/search"
        try:
            payload = json.dumps({
            "q": query,
            "num": num_results
            })
            response = requests.post(url, headers=self.headers, data=payload)
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def search_news(self, query, num_results=10):
        url = f"{self.base_url}/news"
        try:
            payload = json.dumps({
            "q": query,
            "num": num_results,
            })
            response = requests.post(url, headers=self.headers, data=payload)
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_videos(self, query, num_results=10):
        url = f"{self.base_url}/videos"
        try:
            payload = json.dumps({
            "q": query,
            "num": num_results,
            })  
            response = requests.post(url, headers=self.headers, data=payload)
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
