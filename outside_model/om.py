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
    def make_stream_request(self, system_prompt, query):
        global client
        model = "meta-llama/llama-3.1-8b-instruct"
        stream = True 
        max_tokens = 8192

        chat_completion_res = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": query,
                }
            ],
            stream=stream,
            max_tokens=max_tokens,
        )

        if stream:
            for chunk in chat_completion_res:
                print(chunk.choices[0].delta.content or "")
        else:
            print(chat_completion_res.choices[0].message.content)
                
        