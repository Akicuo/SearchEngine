from requests import get, post
from colorama import Fore
"""

"""
URL_SERVICE = "https://laylan.click/api/"
class SearchAgentEngine():
    def __init__(self, API_Key):
        self.api_key = API_Key

    def LogImprovedSearch(self, query:str) -> None:
        search = post(f"{URL_SERVICE}log", 
                      json={"auth": self.api_key, 
                            "query": query}).json()
        if search["response_"] == 200:
            print(Fore.GREEN+" ⦁ Search query logged successfully")
        else:
            print(Fore.RED+" ⦁ Error logging search query")
        Fore.RESET

    def Search(self, query:str) -> None:
        search = post(f"{URL_SERVICE}search", 
                      json={"auth": self.api_key, 
                            "query": query}).json()
        if search["response_"] == 200:
            print(Fore.GREEN+" ⦁ Successfully retrieved response")
            Fore.RESET
            return search["scs"]
        else:
            print(Fore.RED+" ⦁ Error retrieving response")
            Fore.RESET
            return []
        
    def KeyIsUsable(self):
        key = post(f"{URL_SERVICE}key", json={"auth": self.api_key}).json()
        if key["response_"] == 200:
            return True
        else:
            return False
        
        