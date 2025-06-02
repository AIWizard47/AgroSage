# utils/groq_ai.py
import requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_ai(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    data = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [{
            "role": "user",
            "content": f"You are a smart agricultural assistant. Answer only farming-related questions. {prompt}"
        }]
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

    
