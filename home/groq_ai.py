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

    
