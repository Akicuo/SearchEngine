import requests, json

def get_novita_ai_response(api_key, query, system_prompt="You are a helpful assistant"):
    url = "https://api.novita.ai/v3/openai/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "max_tokens": 2048
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    return response.json()