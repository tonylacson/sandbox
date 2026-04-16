## QUICK START GUIDE

### 1. Install Ollama (5 minutes)

- Download from https://ollama.ai
- Install and start: `ollama serve`

### 2. Pull a Model (2 minutes)

```bash
ollama pull qwen2.5-coder
```

### 3. Install Python Packages (1 minute)

```bash
pip install -r requirements.txt
```

### 4. Run the Agent!

```bash
python web_scraper_agent.py
```

---

## Configuration

All settings are in the `Config` class. Default setup works out of the box:

```python
class Config:
    OLLAMA_API_URL = "http://localhost:11434/api"
    OLLAMA_MODEL = "qwen2.5-coder"
    # ... other settings
```
