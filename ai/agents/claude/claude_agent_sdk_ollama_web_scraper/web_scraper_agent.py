"""
Ollama-Powered Web Scraper Agent

A web scraping agent that uses Ollama locally for LLM processing.
No API keys or external services required - all processing is local.
All settings are configured in code without environment variables.
"""

import json
import re
from typing import Any, List, Dict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# ============================================================================
# CONFIGURATION - All settings in code
# ============================================================================

class Config:
    """Centralized configuration for the agent."""
    
    # Ollama Configuration (local LLM processing)
    OLLAMA_API_URL = "http://localhost:11434/api"
    OLLAMA_MODEL = "mistral:latest"  # Smaller, faster
    # Or: "neural-chat:latest"
    # Or: "qwen3-coder:latest"
    OLLAMA_TIMEOUT = 90
    
    # Web Scraping Configuration
    REQUEST_TIMEOUT = 30
    MAX_CONTENT_LENGTH = 50000  # Max characters to process
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Agent Configuration
    MAX_ITERATIONS = 10  # Max tool calls before stopping
    TEMPERATURE = 0.7


# ============================================================================
# TOOL DEFINITIONS - Web Scraping Tools
# ============================================================================

def scrape_website(url: str) -> dict:
    """
    Scrape a website and return the text content.
    
    Args:
        url: The website URL to scrape
        
    Returns:
        Dictionary with scraped content or error message
    """
    try:
        # Validate URL
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
            
        # Fetch the webpage
        headers = {"User-Agent": Config.USER_AGENT}
        response = requests.get(
            url,
            headers=headers,
            timeout=Config.REQUEST_TIMEOUT,
            allow_redirects=True
        )
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator='\n', strip=True)
        
        # Limit content length
        if len(text) > Config.MAX_CONTENT_LENGTH:
            text = text[:Config.MAX_CONTENT_LENGTH] + "... [truncated]"
        
        # Get page title
        title = soup.title.string if soup.title else "No title"
        
        return {
            "status": "success",
            "url": url,
            "title": title,
            "content": text,
            "content_length": len(text)
        }
        
    except requests.RequestException as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Failed to fetch URL: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Error parsing content: {str(e)}"
        }


def extract_links(url: str) -> dict:
    """
    Extract all links from a website.
    
    Args:
        url: The website URL to extract links from
        
    Returns:
        Dictionary with list of links
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
            
        headers = {"User-Agent": Config.USER_AGENT}
        response = requests.get(
            url,
            headers=headers,
            timeout=Config.REQUEST_TIMEOUT,
            allow_redirects=True
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            text = link.get_text(strip=True)
            links.append({
                "url": absolute_url,
                "text": text if text else "No text"
            })
        
        return {
            "status": "success",
            "url": url,
            "links_found": len(links),
            "links": links[:50]  # Limit to 50 links
        }
        
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Error extracting links: {str(e)}"
        }


def search_content_on_page(url: str, search_terms: str) -> dict:
    """
    Search for specific terms in a webpage.
    
    Args:
        url: The website URL to search
        search_terms: Terms to search for (comma-separated)
        
    Returns:
        Dictionary with search results
    """
    try:
        # First scrape the page
        scrape_result = scrape_website(url)
        
        if scrape_result["status"] != "success":
            return scrape_result
        
        content = scrape_result["content"].lower()
        terms = [term.strip().lower() for term in search_terms.split(',')]
        
        results = {}
        for term in terms:
            # Find occurrences
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            matches = pattern.findall(content)
            results[term] = len(matches)
        
        return {
            "status": "success",
            "url": url,
            "search_results": results,
            "total_matches": sum(results.values())
        }
        
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Error searching content: {str(e)}"
        }


def get_metadata(url: str) -> dict:
    """
    Extract metadata from a webpage (title, description, keywords, etc).
    
    Args:
        url: The website URL
        
    Returns:
        Dictionary with metadata
    """
    try:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f"https://{url}"
            
        headers = {"User-Agent": Config.USER_AGENT}
        response = requests.get(
            url,
            headers=headers,
            timeout=Config.REQUEST_TIMEOUT,
            allow_redirects=True
        )
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        metadata = {
            "status": "success",
            "url": url,
            "title": soup.title.string if soup.title else None,
            "description": None,
            "keywords": None,
            "author": None,
            "language": None,
            "canonical_url": None
        }
        
        # Extract meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                metadata["description"] = content
            elif name == 'keywords':
                metadata["keywords"] = content
            elif name == 'author':
                metadata["author"] = content
            elif name == 'language':
                metadata["language"] = content
        
        # Extract canonical URL
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical:
            metadata["canonical_url"] = canonical.get('href')
        
        # Get response headers info
        metadata["content_type"] = response.headers.get('content-type', 'Unknown')
        metadata["status_code"] = response.status_code
        
        return metadata
        
    except Exception as e:
        return {
            "status": "error",
            "url": url,
            "error": f"Error extracting metadata: {str(e)}"
        }


# ============================================================================
# TOOL DEFINITIONS AND DISPATCH
# ============================================================================

TOOLS = {
    "scrape_website": {
        "description": "Scrape a website and extract its text content",
        "function": scrape_website,
        "params": "url (string): The URL of the website to scrape"
    },
    "extract_links": {
        "description": "Extract all links from a website",
        "function": extract_links,
        "params": "url (string): The URL to extract links from"
    },
    "search_content_on_page": {
        "description": "Search for specific terms in a webpage",
        "function": search_content_on_page,
        "params": "url (string): The webpage URL, search_terms (string): comma-separated terms to search for"
    },
    "get_metadata": {
        "description": "Extract metadata from a webpage (title, description, keywords)",
        "function": get_metadata,
        "params": "url (string): The URL of the website"
    }
}


def get_tools_prompt() -> str:
    """Generate a prompt describing available tools for the LLM."""
    tools_desc = "You have access to the following tools:\n\n"
    
    for tool_name, tool_info in TOOLS.items():
        tools_desc += f"1. {tool_name}: {tool_info['description']}\n"
        tools_desc += f"   Parameters: {tool_info['params']}\n"
        tools_desc += f"   Usage: <tool>{tool_name}|param1|param2</tool>\n\n"
    
    tools_desc += "\nWhen you need to use a tool, format it as: <tool>tool_name|parameter1|parameter2</tool>\n"
    tools_desc += "For example: <tool>scrape_website|https://example.com</tool>\n"
    tools_desc += "Or: <tool>search_content_on_page|https://example.com|API,documentation</tool>\n"
    
    return tools_desc


def parse_tool_calls(text: str) -> List[Dict[str, Any]]:
    """
    Parse tool calls from LLM response.
    Looks for patterns like <tool>tool_name|param1|param2</tool>
    
    Args:
        text: The text to parse
        
    Returns:
        List of tool calls with name and parameters
    """
    tool_calls = []
    pattern = r'<tool>(\w+)\|([^<]*)</tool>'
    
    matches = re.findall(pattern, text)
    for tool_name, params_str in matches:
        params = [p.strip() for p in params_str.split('|')]
        
        if tool_name == "scrape_website" and len(params) >= 1:
            tool_calls.append({
                "name": tool_name,
                "params": {"url": params[0]}
            })
        elif tool_name == "extract_links" and len(params) >= 1:
            tool_calls.append({
                "name": tool_name,
                "params": {"url": params[0]}
            })
        elif tool_name == "search_content_on_page" and len(params) >= 2:
            tool_calls.append({
                "name": tool_name,
                "params": {"url": params[0], "search_terms": params[1]}
            })
        elif tool_name == "get_metadata" and len(params) >= 1:
            tool_calls.append({
                "name": tool_name,
                "params": {"url": params[0]}
            })
    
    return tool_calls


def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool and return the result as a string.
    
    Args:
        tool_name: Name of the tool to execute
        tool_input: Input parameters for the tool
        
    Returns:
        Tool result as JSON string
    """
    if tool_name not in TOOLS:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    
    tool_func = TOOLS[tool_name]["function"]
    result = tool_func(**tool_input)
    return json.dumps(result)


# ============================================================================
# OLLAMA AGENT IMPLEMENTATION
# ============================================================================

class WebScraperAgent:
    """Ollama-powered agent for web scraping with tool use."""
    
    def __init__(self):
        """Initialize the agent with Ollama."""
        self.api_url = Config.OLLAMA_API_URL
        self.model = Config.OLLAMA_MODEL
        self.messages = []
        self.iteration_count = 0
        self.system_prompt = f"""You are a helpful web scraping assistant. You help users gather information from websites.

{get_tools_prompt()}

Instructions:
- Always analyze the user's request and determine which tools are needed
- Use tools to gather information
- When you use a tool, wait for the result before proceeding
- Provide clear, concise responses based on the tool results
- If a tool fails, explain why and suggest alternatives
- Be thorough but efficient"""
    
    def check_ollama_running(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            # Get the base URL (remove /api if present)
            base_url = self.api_url.replace("/api", "") if self.api_url.endswith("/api") else self.api_url
            if base_url.endswith("/"):
                base_url = base_url[:-1]
            
            # Try to connect to the tags endpoint
            tags_url = f"{base_url}/api/tags"
            response = requests.get(tags_url, timeout=5)
            
            if response.status_code == 200:
                return True
            else:
                print(f"Warning: Ollama returned status {response.status_code}")
                # Still allow continuation as endpoint might be working differently
                return True
                
        except requests.exceptions.ConnectionError as e:
            print(f"Error: Could not connect to Ollama at {self.api_url}")
            print(f"Make sure Ollama is running: ollama serve")
            print(f"Details: {str(e)}")
            return False
        except requests.exceptions.Timeout:
            print(f"Error: Connection to Ollama timed out at {self.api_url}")
            print(f"Make sure Ollama is running and responsive: ollama serve")
            return False
        except Exception as e:
            print(f"Error: Failed to check Ollama status: {str(e)}")
            print(f"API URL being tested: {self.api_url}")
            return False
    
    def get_ollama_response(self, messages: List[Dict]) -> str:
        """
        Get response from Ollama.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Response text from the model
        """
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "temperature": Config.TEMPERATURE
                },
                timeout=Config.OLLAMA_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error communicating with Ollama: {str(e)}"
    
    def run(self, user_message: str) -> str:
        """
        Run the agent with a user message.
        
        Args:
            user_message: The user's request
            
        Returns:
            The agent's final response
        """
        # Check if Ollama is running
        if not self.check_ollama_running():
            return "Ollama is not running. Please start it first with 'ollama serve'"
        
        self.messages = []
        self.iteration_count = 0
        
        print(f"\n{'='*70}")
        print(f"User: {user_message}")
        print(f"{'='*70}")
        print(f"Model: {self.model}")
        print(f"Ollama API: {self.api_url}")
        
        # Agentic loop
        while self.iteration_count < Config.MAX_ITERATIONS:
            self.iteration_count += 1
            print(f"\n[Iteration {self.iteration_count}]")
            
            # Add user message to conversation
            if self.iteration_count == 1:
                self.messages.append({
                    "role": "user",
                    "content": user_message
                })
            
            # Get response from Ollama
            full_messages = [
                {"role": "system", "content": self.system_prompt},
                *self.messages
            ]
            
            response_text = self.get_ollama_response(full_messages)
            
            print(f"  Agent Response:\n{response_text[:300]}..." if len(response_text) > 300 else f"  Agent Response:\n{response_text}")
            
            # Parse for tool calls
            tool_calls = parse_tool_calls(response_text)
            
            if tool_calls:
                print(f"\n  Found {len(tool_calls)} tool call(s)")
                
                # Add the assistant's response to conversation
                self.messages.append({
                    "role": "assistant",
                    "content": response_text
                })
                
                # Process each tool call
                tool_results = []
                for tool_call in tool_calls:
                    tool_name = tool_call["name"]
                    tool_params = tool_call["params"]
                    
                    print(f"    Tool: {tool_name}")
                    print(f"    Params: {tool_params}")
                    
                    # Execute tool
                    tool_result = process_tool_call(tool_name, tool_params)
                    tool_results.append(tool_result)
                    
                    # Parse result for display
                    try:
                        result_obj = json.loads(tool_result)
                        if result_obj.get("status") == "success":
                            print(f"    Result: ✓ Success")
                        else:
                            print(f"    Result: ✗ {result_obj.get('error', 'Unknown error')}")
                    except:
                        print(f"    Result: {tool_result[:100]}")
                
                # Add tool results to messages
                self.messages.append({
                    "role": "user",
                    "content": f"Tool execution results: {json.dumps(tool_results)}"
                })
                
                # Continue loop with tool results
                continue
            else:
                # No tool calls, agent is done
                print(f"\n{'='*70}")
                print(f"Agent: {response_text}")
                print(f"{'='*70}")
                return response_text
        
        # If we hit max iterations
        return f"Agent reached maximum iterations ({Config.MAX_ITERATIONS})"


# ============================================================================
# MAIN
# ============================================================================

def verify_ollama_setup() -> bool:
    """
    Verify that Ollama is properly set up and accessible.
    
    Returns:
        True if setup is valid, False otherwise
    """
    print("Verifying Ollama Setup...")
    print(f"Ollama API URL: {Config.OLLAMA_API_URL}")
    print(f"Ollama Model: {Config.OLLAMA_MODEL}")
    
    agent = WebScraperAgent()
    
    # Try to connect
    print("\nAttempting to connect to Ollama...")
    if not agent.check_ollama_running():
        print("\n❌ Ollama is not accessible!")
        print("\nTroubleshooting steps:")
        print("1. Make sure Ollama is installed: visit https://ollama.ai")
        print("2. Start Ollama in a terminal: ollama serve")
        print("3. Verify it's running: curl http://localhost:11434/api/tags")
        print("4. Check if the model is installed:")
        print(f"   ollama pull {Config.OLLAMA_MODEL}")
        return False
    
    print("✓ Connected to Ollama successfully!")
    
    # Try to get model info
    try:
        base_url = Config.OLLAMA_API_URL.replace("/api", "") if Config.OLLAMA_API_URL.endswith("/api") else Config.OLLAMA_API_URL
        if base_url.endswith("/"):
            base_url = base_url[:-1]
        
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [m.get("name", "unknown") for m in models]
            print(f"\n✓ Available models: {model_names}")
            
            # Check if model exists (with or without version tag)
            model_base_name = Config.OLLAMA_MODEL.split(":")[0]  # Get model name without version tag
            model_found = False
            full_model_name = None
            
            for model_name in model_names:
                if model_name.startswith(model_base_name):
                    model_found = True
                    full_model_name = model_name
                    break
            
            if not model_found:
                print(f"\n⚠ Warning: {Config.OLLAMA_MODEL} not found!")
                print(f"Install it with: ollama pull {Config.OLLAMA_MODEL}")
                return False
            
            print(f"✓ Model '{full_model_name}' is installed")
            
            # Update config with full model name if it has a tag
            if full_model_name != Config.OLLAMA_MODEL:
                Config.OLLAMA_MODEL = full_model_name
                print(f"ℹ Updated model name to: {full_model_name}")
        else:
            print(f"⚠ Could not fetch model list (status {response.status_code})")
    except Exception as e:
        print(f"⚠ Could not fetch model list: {e}")
    
    print("\n✓ Setup verification complete!")
    return True


def main():
    """Main function to run the web scraper agent."""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    Ollama Web Scraper Agent                               ║
║                   (Local, No API Keys Required)                           ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Verify setup
    if not verify_ollama_setup():
        print("\n❌ Setup verification failed. Please fix the issues above.")
        return
    
    # Initialize agent
    agent = WebScraperAgent()
    
    # Example tasks
    tasks = [
        "Scrape https://example.com and tell me what it's about in 2-3 sentences",
    ]
    
    # Run first task
    print(f"\n{'='*70}")
    print(f"Starting Web Scraper Agent with Ollama...")
    print(f"Tools Available: {', '.join(TOOLS.keys())}")
    print(f"{'='*70}\n")
    
    response = agent.run(tasks[0])
    print(f"\nFinal Response:\n{response}")
    
    # Uncomment below to run additional tasks
    # for task in tasks[1:]:
    #     response = agent.run(task)
    #     print(f"\nFinal Response:\n{response}\n")


if __name__ == "__main__":
    main()
