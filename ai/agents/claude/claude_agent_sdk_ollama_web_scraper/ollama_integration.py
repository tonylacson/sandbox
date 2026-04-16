"""
Ollama Integration Guide

This guide explains how to integrate the Claude Web Scraper Agent with Ollama
for local, offline LLM processing alongside Claude.
"""

import json
import requests
from typing import Optional


# ============================================================================
# OLLAMA INTEGRATION UTILITIES
# ============================================================================

class OllamaIntegration:
    """Utilities for integrating Ollama with the scraping agent."""
    
    def __init__(self, api_url: str = "http://localhost:11434", model: str = "qwen2.5-coder"):
        """
        Initialize Ollama integration.
        
        Args:
            api_url: URL of Ollama API
            model: Model name to use
        """
        self.api_url = api_url
        self.model = model
        self.timeout = 90
    
    def is_ollama_running(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Ollama not accessible: {e}")
            return False
    
    def list_available_models(self) -> list:
        """Get list of available models in Ollama."""
        try:
            response = requests.get(f"{self.api_url}/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """
        Download a model if not already present.
        
        Args:
            model_name: Name of model to pull
            
        Returns:
            True if successful
        """
        print(f"Pulling model {model_name}...")
        try:
            response = requests.post(
                f"{self.api_url}/pull",
                json={"name": model_name},
                timeout=600  # Long timeout for download
            )
            print(f"Pull response: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error pulling model: {e}")
            return False
    
    def process_content_with_ollama(
        self,
        content: str,
        instruction: str,
        model: Optional[str] = None
    ) -> str:
        """
        Process content using a local Ollama model.
        
        Args:
            content: Content to process
            instruction: Instruction for what to do with content
            model: Model to use (defaults to self.model)
            
        Returns:
            Processed result from model
        """
        if model is None:
            model = self.model
        
        # Limit content size for local processing
        max_chars = 30000
        if len(content) > max_chars:
            content = content[:max_chars] + "\n[... content truncated ...]"
        
        try:
            print(f"Processing with Ollama model: {model}")
            
            response = requests.post(
                f"{self.api_url}/generate",
                json={
                    "model": model,
                    "prompt": f"Follow this instruction: {instruction}\n\nContent:\n{content}",
                    "stream": False,
                    "temperature": 0.7
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response from model")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error processing with Ollama: {str(e)}"
    
    def chat_with_ollama(self, messages: list, model: Optional[str] = None) -> str:
        """
        Have a conversation with Ollama model.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model to use (defaults to self.model)
            
        Returns:
            Model response
        """
        if model is None:
            model = self.model
        
        try:
            response = requests.post(
                f"{self.api_url}/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "No response")
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"


# ============================================================================
# HYBRID PROCESSING
# ============================================================================

class HybridScraperProcessor:
    """
    Use Claude for agent decisions and Ollama for content processing.
    Best of both worlds: Claude's intelligence + local processing.
    """
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        """Initialize hybrid processor."""
        self.ollama = OllamaIntegration(api_url=ollama_url)
        self.models = self.ollama.list_available_models()
        
        if not self.models:
            print("Warning: No Ollama models available. Install with: ollama pull <model>")
    
    def summarize_with_local_model(self, content: str, model: str = "qwen2.5-coder") -> str:
        """Summarize content using local model."""
        print(f"Summarizing with local model: {model}")
        return self.ollama.process_content_with_ollama(
            content,
            "Provide a concise summary of the following content. Focus on the main points.",
            model
        )
    
    def extract_info_with_local_model(
        self,
        content: str,
        query: str,
        model: str = "qwen2.5-coder"
    ) -> str:
        """Extract specific information using local model."""
        print(f"Extracting info with local model: {model}")
        return self.ollama.process_content_with_ollama(
            content,
            f"Extract and provide information relevant to: {query}",
            model
        )
    
    def sentiment_analysis_with_local_model(
        self,
        content: str,
        model: str = "qwen2.5-coder"
    ) -> str:
        """Analyze sentiment using local model."""
        print(f"Analyzing sentiment with local model: {model}")
        return self.ollama.process_content_with_ollama(
            content,
            "Analyze the sentiment of this content. Is it positive, negative, or neutral? Explain.",
            model
        )
    
    def categorize_with_local_model(
        self,
        content: str,
        categories: list,
        model: str = "qwen2.5-coder"
    ) -> str:
        """Categorize content using local model."""
        categories_str = ", ".join(categories)
        print(f"Categorizing with local model: {model}")
        return self.ollama.process_content_with_ollama(
            content,
            f"Categorize this content into one of these categories: {categories_str}. Explain your choice.",
            model
        )


# ============================================================================
# SETUP AND TESTING
# ============================================================================

def setup_ollama():
    """
    Guide user through Ollama setup.
    """
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                      Ollama Setup Guide                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

1. INSTALL OLLAMA:
   - Visit: https://ollama.ai
   - Download and install for your OS
   - Start the Ollama service

2. PULL A MODEL:
   Open terminal and run:
   
   ollama pull llama2                    # 7B general purpose model
   ollama pull qwen2.5-coder           # 7B coding model (recommended)
   ollama pull mistral                  # 7B fast model
   ollama pull neural-chat             # 7B chat model

3. LIST INSTALLED MODELS:
   ollama list

4. VERIFY OLLAMA IS RUNNING:
   curl http://localhost:11434/tags
   
5. STOP OLLAMA:
   Ctrl+C in the Ollama terminal or use system tray

RECOMMENDED SETUP:
- For general web scraping: qwen2.5-coder
- For fast processing: mistral
- For conversational: neural-chat
    """)


def test_ollama_integration():
    """Test if Ollama is working correctly."""
    print("\n" + "="*70)
    print("Testing Ollama Integration")
    print("="*70)
    
    ollama = OllamaIntegration()
    
    print("\n1. Checking if Ollama is running...")
    if ollama.is_ollama_running():
        print("   ✓ Ollama is running!")
    else:
        print("   ✗ Ollama is not running. Please start it first.")
        return
    
    print("\n2. Listing available models...")
    models = ollama.list_available_models()
    if models:
        print(f"   ✓ Found {len(models)} model(s):")
        for model in models:
            print(f"     - {model}")
    else:
        print("   ✗ No models found. Run 'ollama pull <model>' first.")
        return
    
    print("\n3. Testing content processing...")
    test_content = """
    Artificial Intelligence is transforming technology. Machine learning models
    can now perform complex tasks like image recognition, language translation,
    and code generation.
    """
    
    test_model = models[0] if models else None
    if test_model:
        result = ollama.process_content_with_ollama(
            test_content,
            "Summarize this in one sentence.",
            test_model
        )
        print(f"   ✓ Model response:\n   {result[:150]}...")
    
    print("\n" + "="*70)
    print("Ollama integration test complete!")
    print("="*70)


# ============================================================================
# EXAMPLE: HYBRID WORKFLOW
# ============================================================================

def example_hybrid_workflow():
    """
    Example of using Claude for agent decisions and Ollama for processing.
    """
    print("\n" + "="*70)
    print("Example: Hybrid Claude + Ollama Workflow")
    print("="*70)
    
    processor = HybridScraperProcessor()
    
    # Example scraped content (simulated)
    sample_content = """
    Product Review: Amazing AI Assistant
    
    This AI tool is incredible! It helps me write better code, understand
    complex concepts, and automate tedious work. The responses are quick and
    accurate. I've been using it for 3 months now and couldn't imagine working
    without it. Highly recommended for developers, writers, and students.
    
    Rating: 5/5 stars
    """
    
    print("\n1. Summarizing with local model...")
    summary = processor.summarize_with_local_model(sample_content)
    print(f"   Summary: {summary}")
    
    print("\n2. Analyzing sentiment...")
    sentiment = processor.sentiment_analysis_with_local_model(sample_content)
    print(f"   Sentiment: {sentiment}")
    
    print("\n3. Categorizing content...")
    categories = ["Product Review", "Tutorial", "News", "Opinion"]
    category = processor.categorize_with_local_model(sample_content, categories)
    print(f"   Category: {category}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║           Claude Web Scraper Agent - Ollama Integration                   ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Uncomment to run:
    setup_ollama()                    # Show setup instructions
    # test_ollama_integration()        # Test Ollama connection
    # example_hybrid_workflow()        # See hybrid processing example
