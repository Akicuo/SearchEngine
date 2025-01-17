import requests
import json

class Serper:
    def __init__(self, api_key):
        self.base_url = "https://google.serper.dev/"
        self.headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
        }

    def search_images(self, query, num_results=10):
        url = f"{self.base_url}/images"
        try:
            response = requests.post(url, headers=self.headers, params={"q": query, "num": num_results}),
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_discover(self, query, num_results=10):
        url = f"{self.base_url}/search"
        try:
            response = requests.post(url, headers=self.headers, params={"q": query, "num": num_results}),
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    def search_news(self, query, num_results=10):
        url = f"{self.base_url}/search"
        try:
            response = requests.post(url, headers=self.headers, params={"q": query, "num": num_results}),
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}