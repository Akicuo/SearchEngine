from requests import get, post
from colorama import Fore
from openai import OpenAI
import os
from dotenv import load_dotenv


URL_SERVICE = "https://laylanclick.replit.app/api/"
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
if key is None:
    print("Please set an OPENAI_API_KEY with a .env file")
    exit(0)

client = OpenAI(
    base_url="https://api.novita.ai/v3/openai", api_key=key)

class SearchAgentEngine():
    def __init__(self, API_Key):
        self.api_key = API_Key
    def Search(self, query:str):
        global LAYLAN_KEY
        search = get(f"{URL_SERVICE}search-discover?q={query}&auth={self.api_key}")
        return search.json()  # Parse the JSON response     