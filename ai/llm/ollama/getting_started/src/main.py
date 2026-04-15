import requests

# Ollama API endpoint
url = "http://localhost:11434/api/chat"

# Request payload
payload = {
    "model": "qwen2.5-coder",
    "messages": [
        {
            "role": "user",
            "content": "Write a Python script to scrape a website."
        }
    ],
    "stream": False
}

print("Making request to Ollama...")

try:
    # Make the request
    response = requests.post(url, json=payload, timeout=90)
    print(f"Response status: {response.status_code}")

    # Check for errors
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
    else:
        data = response.json()
        print("Response received:")
        print(data["message"]["content"])
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")