from requests import get, post
from colorama import Fore
import os

URL_SERVICE = "https://laylanclick.replit.app/api/"

class SearchAgentEngine():
    def __init__(self, API_Key):
        self.api_key = API_Key




    """def LogImprovedSearch(self, query:str) -> None:
        search = post(f"{URL_SERVICE}log", 
                      json={"auth": self.api_key, 
                            "query": query}).json()
        if search["response_"] == 200:
            print(Fore.GREEN+" ⦁ Search query logged successfully")
        else:
            print(Fore.RED+" ⦁ Error logging search query")
        Fore.RESET"""




    def Search(self, query:str):
        global LAYLAN_KEY
        search = get(f"{URL_SERVICE}search-discover?q={query}&auth={self.api_key}")
        return search.json()  # Parse the JSON response

        
        