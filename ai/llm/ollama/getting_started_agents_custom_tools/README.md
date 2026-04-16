# Ollama Agent with Custom Tools

A simple example demonstrating how to use Ollama with function calling (tools) capabilities. This code shows how to create an AI agent that can call custom functions based on user requests.

## What This Code Does

This example creates an AI agent that:
- Uses Ollama locally (no API keys required)
- Defines a custom "get_weather" tool
- Asks the model "What's the weather in Seattle?"
- The model can choose to call the weather tool or respond normally
- Demonstrates tool execution and result handling

## Prerequisites

### 1. Install Ollama
Visit [ollama.ai](https://ollama.ai) and download Ollama for your system.

### 2. Install a Compatible Model
This code works best with models that support function calling. Install one of these:

```bash
# Recommended models (support function calling)
ollama pull qwen2.5-coder:latest
ollama pull llama3.1:8b

# Alternative smaller models
ollama pull mistral:latest
```

### 3. Install Python Dependencies
```bash
pip install requests
```

## Setup Steps

1. **Start Ollama Server**
   ```bash
   ollama serve
   ```
   Keep this running in a separate terminal.

2. **Verify Installation**
   ```bash
   # Check if Ollama is running
   curl http://localhost:11434/api/tags

   # List installed models
   ollama list
   ```

3. **Run the Example**
   ```bash
   cd src
   python main.py
   ```

## Expected Output

When working correctly, you should see output like:

```
Model wants to use tools:
Tool: get_weather
Args: {'location': 'Seattle'}
Tool Result: The weather in Seattle is sunny and 72°F
```

Or if the model doesn't use tools:

```
Response: I don't have access to real-time weather data, but I can tell you that Seattle is known for its rainy weather!
```

## Code Structure

- `main.py`: Main example showing tool usage
- `tools`: Array defining available functions
- `get_weather()`: Mock weather function (replace with real API)

## Customization

### Adding New Tools

To add more tools, modify the `tools` array:

```python
tools = [{
    "type": "function",
    "function": {
        "name": "your_tool_name",
        "description": "What your tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param_name": {
                    "type": "string",
                    "description": "Parameter description"
                }
            },
            "required": ["param_name"]
        }
    }
}]
```

### Implementing Real Functions

Replace the mock `get_weather()` with real implementations:

```python
def get_weather(location: str) -> str:
    # Example: Use OpenWeatherMap API
    import requests
    api_key = "your_api_key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(url)
    # Parse and return real weather data
    return f"Real weather data for {location}"
```

## Troubleshooting

### "Connection refused" Error
- Make sure Ollama is running: `ollama serve`
- Check if port 11434 is available

### "Model not found" Error
- Install the model: `ollama pull qwen2.5-coder`
- Update the `model` variable in the code

### Model Doesn't Use Tools
- Not all models support function calling
- Try different models: `qwen2.5-coder`, `llama3.1:8b`
- Some models may respond normally instead of using tools

### Memory Issues
- Try a smaller model: `ollama pull mistral`
- Or disable GPU: `set OLLAMA_GPU=off` then `ollama serve`

## Model Compatibility

| Model | Function Calling | Recommended |
|-------|------------------|-------------|
| qwen2.5-coder | ✅ Yes | ⭐⭐⭐ |
| llama3.1:8b | ✅ Yes | ⭐⭐⭐ |
| mistral | ⚠️ Partial | ⭐⭐ |
| codellama | ❌ No | ⭐ |

## Next Steps

This is a basic example. To build more advanced agents:

1. **Multiple Tools**: Add more functions to the tools array
2. **Real APIs**: Replace mock functions with actual API calls
3. **Conversation Memory**: Add message history for multi-turn conversations
4. **Error Handling**: Add better error handling and retries
5. **Async Processing**: Use async/await for better performance

## Background

This project was initially created to use the Claude Agent SDK but was converted to use Ollama directly due to endpoint incompatibility. It demonstrates how Ollama can be used for tool calling without external API dependencies.