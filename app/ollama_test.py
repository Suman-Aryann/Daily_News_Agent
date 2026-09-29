import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen3:4b",
    "prompt": "Explain what an AI agent is in two simple sentences.",
    "stream": False
}

response = requests.post(OLLAMA_URL, json=payload)

response.raise_for_status()

result = response.json()

print("\nResponse from Qwen3:\n")
print(result["response"])