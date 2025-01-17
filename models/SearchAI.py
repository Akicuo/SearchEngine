import requests, json


from openai import OpenAI


def stream(api_key:str, system_prompt:str,query:str):
    global client
    client = OpenAI(api_key=api_key,
    base_url="https://api.novita.ai/v3/openai"
)
    model = "meta-llama/llama-3.1-70b-instruct"
    stream = True
    max_tokens = 8048

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
            yield chunk.choices[0].delta.content or ""
    else:
        # Currently set to return this
        return chat_completion_res.choices[0].message.content


