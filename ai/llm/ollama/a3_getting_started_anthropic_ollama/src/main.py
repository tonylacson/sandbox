import anthropic

client = anthropic.Anthropic(
    base_url="http://localhost:11434",
    api_key="ollama" # placeholder
)

message = client.messages.create(
    model="qwen2.5-coder",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude Agent!"}]
)
print(message.content[0].text)