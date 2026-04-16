"""
Advanced Examples for the Claude Web Scraper Agent

This module demonstrates advanced usage patterns, custom configurations,
and integration scenarios for the web scraper agent.
"""

from web_scraper_agent import WebScraperAgent, Config


# ============================================================================
# EXAMPLE 1: Custom Configuration for Different Tasks
# ============================================================================

def example_quick_scrape():
    """
    Quick scraping with optimized settings for speed.
    Reduces timeouts and iterations for fast operations.
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Quick Scrape Mode")
    print("="*70)
    
    # Override config for quick operations
    original_timeout = Config.REQUEST_TIMEOUT
    original_max_iter = Config.MAX_ITERATIONS
    
    Config.REQUEST_TIMEOUT = 15
    Config.MAX_ITERATIONS = 5
    
    agent = WebScraperAgent()
    response = agent.run("Quickly summarize what's on example.com")
    
    # Restore config
    Config.REQUEST_TIMEOUT = original_timeout
    Config.MAX_ITERATIONS = original_max_iter
    
    print(f"\nResult:\n{response}")


# ============================================================================
# EXAMPLE 2: Deep Content Analysis
# ============================================================================

def example_content_analysis():
    """
    Deep analysis of website content with extended iterations.
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Deep Content Analysis")
    print("="*70)
    
    # Increase iterations for complex analysis
    original_max_iter = Config.MAX_ITERATIONS
    Config.MAX_ITERATIONS = 15
    
    agent = WebScraperAgent()
    
    task = """
    Visit https://example.com and:
    1. Get the main content
    2. Find all linked pages
    3. Search for keywords like 'information' and 'more'
    4. Get metadata
    5. Provide a structured analysis of the site
    """
    
    response = agent.run(task)
    
    Config.MAX_ITERATIONS = original_max_iter
    print(f"\nAnalysis Result:\n{response}")


# ============================================================================
# EXAMPLE 3: Multi-Site Comparison
# ============================================================================

def example_multi_site_comparison():
    """
    Compare content across multiple websites.
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Multi-Site Comparison")
    print("="*70)
    
    agent = WebScraperAgent()
    
    sites = [
        "https://www.wikipedia.org",
        "https://www.github.com",
    ]
    
    comparisons = {}
    
    for site in sites:
        print(f"\nAnalyzing {site}...")
        task = f"Get the title and main purpose of {site} in 2-3 sentences"
        response = agent.run(task)
        comparisons[site] = response
    
    print("\n" + "="*70)
    print("COMPARISON RESULTS")
    print("="*70)
    for site, result in comparisons.items():
        print(f"\n{site}:")
        print(f"  {result[:200]}...")


# ============================================================================
# EXAMPLE 4: Link Extraction and Analysis
# ============================================================================

def example_link_analysis():
    """
    Extract and analyze links from a website.
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Link Extraction and Analysis")
    print("="*70)
    
    agent = WebScraperAgent()
    
    task = """
    From https://example.com:
    1. Extract all available links
    2. Categorize them by type (internal/external)
    3. List the top navigation links
    4. Identify any social media links
    """
    
    response = agent.run(task)
    print(f"\nLink Analysis:\n{response}")


# ============================================================================
# EXAMPLE 5: Search and Extract
# ============================================================================

def example_search_and_extract():
    """
    Search for specific content and extract relevant information.
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Search and Extract")
    print("="*70)
    
    agent = WebScraperAgent()
    
    task = """
    On the website https://example.com:
    1. Search for any email addresses or contact information
    2. Look for phone numbers or contact forms
    3. Find any pricing or product information
    4. Extract any important sections or headings
    """
    
    response = agent.run(task)
    print(f"\nExtraction Result:\n{response}")


# ============================================================================
# EXAMPLE 6: Metadata Extraction
# ============================================================================

def example_metadata_extraction():
    """
    Extract comprehensive metadata from multiple pages.
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Metadata Extraction")
    print("="*70)
    
    agent = WebScraperAgent()
    
    task = """
    Get the complete metadata for https://example.com including:
    - Title
    - Description
    - Keywords
    - Author
    - Canonical URL
    - Then explain what this site is about based on metadata
    """
    
    response = agent.run(task)
    print(f"\nMetadata Results:\n{response}")


# ============================================================================
# EXAMPLE 7: Custom Tool Chain
# ============================================================================

def example_custom_tool_chain():
    """
    Use a specific sequence of tools to accomplish a goal.
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Custom Tool Chain")
    print("="*70)
    
    agent = WebScraperAgent()
    
    # Use tools in sequence
    task = """
    Perform these steps exactly:
    1. First, use get_metadata on https://example.com
    2. Then use scrape_website on the same URL
    3. Then use extract_links on the same URL
    4. Finally, provide a summary incorporating all three results
    """
    
    response = agent.run(task)
    print(f"\nTool Chain Result:\n{response}")


# ============================================================================
# EXAMPLE 8: Large Scale Content Processing
# ============================================================================

def example_large_content():
    """
    Handle and process large amounts of content.
    """
    print("\n" + "="*70)
    print("EXAMPLE 8: Large Content Processing")
    print("="*70)
    
    # Increase content length for this
    original_max_content = Config.MAX_CONTENT_LENGTH
    Config.MAX_CONTENT_LENGTH = 100000
    
    agent = WebScraperAgent()
    
    task = """
    Download and process the full content from https://example.com:
    1. Extract the main sections
    2. Identify key topics
    3. Find repeated information
    4. Create a structured outline
    """
    
    response = agent.run(task)
    
    Config.MAX_CONTENT_LENGTH = original_max_content
    print(f"\nContent Analysis:\n{response}")


# ============================================================================
# EXAMPLE 9: Error Handling and Resilience
# ============================================================================

def example_error_resilience():
    """
    Handle errors gracefully and retry strategies.
    """
    print("\n" + "="*70)
    print("EXAMPLE 9: Error Handling")
    print("="*70)
    
    agent = WebScraperAgent()
    
    # Mix valid and potentially problematic URLs
    urls = [
        "https://example.com",  # Valid
        "https://this-domain-definitely-does-not-exist-12345.com",  # Fails
        "https://github.com",  # Valid
    ]
    
    for url in urls:
        print(f"\nProcessing: {url}")
        task = f"Try to get information from {url}. If it fails, explain why."
        response = agent.run(task)
        print(f"Result: {response[:150]}...")


# ============================================================================
# EXAMPLE 10: Configuration Management
# ============================================================================

def example_config_management():
    """
    Demonstrate configuration best practices.
    """
    print("\n" + "="*70)
    print("EXAMPLE 10: Configuration Management")
    print("="*70)
    
    print(f"Current Configuration:")
    print(f"  API Key: {Config.ANTHROPIC_API_KEY[:20]}...")
    print(f"  Model: {Config.CLAUDE_MODEL}")
    print(f"  Request Timeout: {Config.REQUEST_TIMEOUT}s")
    print(f"  Max Content Length: {Config.MAX_CONTENT_LENGTH} chars")
    print(f"  Max Iterations: {Config.MAX_ITERATIONS}")
    print(f"  Temperature: {Config.TEMPERATURE}")
    print(f"  Ollama URL: {Config.OLLAMA_API_URL}")
    print(f"  User Agent: {Config.USER_AGENT}")
    
    print("\nTo modify configuration, edit the Config class in web_scraper_agent.py")


# ============================================================================
# MAIN - Run Examples
# ============================================================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                Claude Web Scraper Agent - Advanced Examples                ║
║                                                                            ║
║ This script demonstrates advanced usage patterns for the web scraper     ║
║ agent. Uncomment the examples you want to run.                           ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Uncomment examples to run:
    
    # example_quick_scrape()                    # Fast and simple
    # example_content_analysis()               # Deep analysis
    # example_multi_site_comparison()          # Compare multiple sites
    # example_link_analysis()                  # Extract and analyze links
    # example_search_and_extract()             # Search for content
    # example_metadata_extraction()            # Get metadata
    # example_custom_tool_chain()              # Use tools in sequence
    # example_large_content()                  # Process large content
    # example_error_resilience()               # Handle errors
    example_config_management()              # View configuration
    
    print("\n" + "="*70)
    print("Examples completed! Uncomment more examples in the script to run them.")
    print("="*70)
