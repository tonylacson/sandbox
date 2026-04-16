import requests
import json

# Initialize client with local Ollama settings
api_url = "http://localhost:11434/api/chat"
model = "qwen2.5-coder"

# Example Tool Definition
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city name"
                }
            },
            "required": ["location"]
        }
    }
}]

def get_weather(location: str) -> str:
    """Mock weather function - replace with real API call"""
    return f"The weather in {location} is sunny and 72°F"

# Create Message with tools
response = requests.post(api_url, json={
    "model": model,
    "messages": [{"role": "user", "content": "What's the weather in Seattle?"}],
    "tools": tools,
    "stream": False
},
timeout=90)

if response.status_code == 200:
    result = response.json()
    message = result.get("message", {})

    # Check if the model wants to use a tool
    tool_calls = message.get("tool_calls", [])
    if tool_calls:
        print("Model wants to use tools:")
        for tool_call in tool_calls:
            function_name = tool_call.get("function", {}).get("name")
            function_args = json.loads(tool_call.get("function", {}).get("arguments", "{}"))

            print(f"Tool: {function_name}")
            print(f"Args: {function_args}")

            # Execute the tool
            if function_name == "get_weather":
                result = get_weather(**function_args)
                print(f"Tool Result: {result}")
    else:
        # Regular response
        message_content = message.get("content", "")
        print(f"Response: {message_content}")
else:
    print(f"Error: {response.status_code} - {response.text}")
