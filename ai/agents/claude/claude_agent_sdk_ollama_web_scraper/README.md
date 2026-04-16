# Ollama Web Scraper Agent

A powerful web scraping agent powered entirely by Ollama. No API keys, no subscription fees—all processing is local and completely free.

## Features

- **Completely Local** - Uses Ollama for all LLM processing (no cloud services)
- **No API Keys** - Zero external dependencies or authentication needed
- **Free to Use** - No subscription fees or API costs
- **Multiple Tools**: 
  - `scrape_website`: Get full text content from any webpage
  - `extract_links`: Find all links and their context
  - `search_content_on_page`: Search for specific terms on pages
  - `get_metadata`: Extract metadata (title, description, keywords, etc)
- **Agentic Loop**: Ollama automatically decides which tools to use
- **Error Handling**: Robust error handling for network issues and parsing failures
- **All-in-Code Configuration**: No environment variables needed

## Setup

### 1. Install Ollama

Download and install from [ollama.ai](https://ollama.ai) for your operating system.

### 2. Pull a Model

Open a terminal and download a model (recommended: qwen2.5-coder):

```bash
ollama pull qwen2.5-coder
```

Other models you can try:
- `ollama pull llama2` - General purpose
- `ollama pull mistral` - Fast and efficient
- `ollama pull neural-chat` - Conversational

### 3. Start Ollama

```bash
ollama serve
```

Keep this terminal running. Ollama will be available at `http://localhost:11434`

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Agent

```bash
python web_scraper_agent.py
```

## Configuration

All settings are in the `Config` class in `web_scraper_agent.py`:

```python
class Config:
    OLLAMA_API_URL = "http://localhost:11434/api"
    OLLAMA_MODEL = "qwen2.5-coder"           # Change model here
    REQUEST_TIMEOUT = 30
    MAX_CONTENT_LENGTH = 50000
    MAX_ITERATIONS = 10
    TEMPERATURE = 0.7
```

## Usage

### Basic Usage

```python
from web_scraper_agent import WebScraperAgent

# Create agent
agent = WebScraperAgent()

# Run a task
response = agent.run("Scrape example.com and summarize it")
print(response)
```

### Example Tasks

```python
agent = WebScraperAgent()

# Task 1: Summarize a website
agent.run("Visit https://clau.de and tell me what Anthropic does")

# Task 2: Find specific information
agent.run("Go to example.com and find all mentions of 'secure'")

# Task 3: Extract links
agent.run("Extract all links from https://news.ycombinator.com/")

# Task 4: Get metadata
agent.run("What's the description and keywords of https://github.com?")

# Task 5: Complex task
agent.run("""
Visit https://example.com, scrape its content, 
find all links to other pages, and summarize 
what the site is about
""")
```

### Run the Agent

```bash
python web_scraper_agent.py
```

## Configuration Reference

### Config Class

- **OLLAMA_API_URL**: URL to Ollama API (default: `http://localhost:11434/api`)
- **OLLAMA_MODEL**: Model to use locally (default: `qwen2.5-coder`)
- **REQUEST_TIMEOUT**: HTTP request timeout in seconds (default: 30)
- **MAX_CONTENT_LENGTH**: Maximum characters to process from a page (default: 50000)
- **MAX_ITERATIONS**: Maximum tool calls before stopping (default: 10)
- **TEMPERATURE**: Ollama's temperature setting (default: 0.7)
- **USER_AGENT**: Custom user agent for requests (default: Mozilla string)

## Tools

### scrape_website(url)
Extracts all text content from a webpage.

**Parameters:**
- `url` (string): The website URL

**Returns:**
- `status`: "success" or "error"
- `content`: Extracted text (up to MAX_CONTENT_LENGTH)
- `title`: Page title
- `content_length`: Length of extracted content

### extract_links(url)
Finds all links on a webpage.

**Parameters:**
- `url` (string): The website URL

**Returns:**
- `status`: "success" or "error"
- `links`: List of links with text (limited to 50)
- `links_found`: Total number of links found

### search_content_on_page(url, search_terms)
Searches for specific terms on a page.

**Parameters:**
- `url` (string): The website URL
- `search_terms` (string): Comma-separated search terms

**Returns:**
- `status`: "success" or "error"
- `search_results`: Count of matches for each term
- `total_matches`: Total matches found

### get_metadata(url)
Extracts metadata from a webpage.

**Parameters:**
- `url` (string): The website URL

**Returns:**
- `status`: "success" or "error"
- `title`: Page title
- `description`: Meta description
- `keywords`: Meta keywords
- `author`: Page author
- `canonical_url`: Canonical URL
- `content_type`: Content type from headers
- `status_code`: HTTP status code

## How It Works

1. **Agentic Loop**: The agent uses Claude's decision-making to plan and execute tasks
2. **Tool Selection**: Claude decides which tools to use based on the user request
3. **Iterative Refinement**: The agent can make multiple tool calls to accomplish complex tasks
4. **Error Handling**: Network errors and parsing issues are handled gracefully
5. **Content Processing**: Large pages are truncated, scripts/styles are removed, and HTML is cleaned

## Advanced Usage

### Custom Task Loop

```python
agent = WebScraperAgent()

# Define multiple related tasks
tasks = [
    "Get the homepage of github.com",
    "Extract all links from that homepage",
    "Search each link for 'GitHub'",
]

for task in tasks:
    response = agent.run(task)
    print(f"Response: {response}\n")
```

### Accessing Raw Tool Results

Tools return JSON responses that Claude parses. You can see the raw results in the console output during agent iteration.

## Troubleshooting

### "Ollama is not running"
Start Ollama first with `ollama serve` in a terminal and keep it running.

### "Model not found"
Download the model first: `ollama pull qwen2.5-coder`

### "Failed to fetch URL"
Check:
- The URL is correct and accessible
- Your internet connection is working
- The website isn't blocking your requests
- Try with a different User-Agent in config

### "Max iterations reached"
The agent used all available iterations. Increase `Config.MAX_ITERATIONS` or simplify the task.

### Content is truncated
Increase `Config.MAX_CONTENT_LENGTH` for longer pages.

### Rate limiting
Add delays between requests or reduce parallelism.

## Limitations

- Pages over 50KB are truncated (configurable)
- JavaScript-rendered content won't be scraped (use with headless browser for that)
- Some sites may require authentication or block bot traffic
- Extracting links returns top 50 to avoid overwhelming Claude
- Agent iteration is capped at 10 calls (configurable)

## Future Enhancements

- [ ] Headless browser integration for JavaScript rendering
- [ ] Session management for authenticated scraping
- [ ] Proxy support for distributed scraping
- [ ] Database integration for storing results
- [ ] Scheduling and continuous monitoring
- [ ] Multi-page crawling workflows

## License

This code is provided as-is for educational and development purposes.
