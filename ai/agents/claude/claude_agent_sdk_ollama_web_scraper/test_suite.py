"""
Test Suite for Claude Web Scraper Agent

Run this file to verify the agent is working correctly.
Tests API connectivity, tools, and basic functionality.
"""

import sys
from web_scraper_agent import (
    Config,
    WebScraperAgent,
    scrape_website,
    extract_links,
    search_content_on_page,
    get_metadata,
    TOOLS
)


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")


def check_api_key():
    """Check if API key is configured."""
    print_header("1. Checking API Key Configuration")
    
    if not Config.ANTHROPIC_API_KEY or Config.ANTHROPIC_API_KEY == "your-api-key-here":
        print_error("API key not configured!")
        print("  Action: Edit web_scraper_agent.py and set Config.ANTHROPIC_API_KEY")
        print("  Get key from: https://console.anthropic.com/api_keys")
        return False
    else:
        # Show masked key
        masked_key = Config.ANTHROPIC_API_KEY[:10] + "...[hidden]"
        print_success(f"API key configured: {masked_key}")
        return True


def check_tools():
    """Check if all tools are registered."""
    print_header("2. Checking Available Tools")
    
    required_tools = [
        "scrape_website",
        "extract_links",
        "search_content_on_page",
        "get_metadata"
    ]
    
    all_present = True
    for tool_name in required_tools:
        if tool_name in TOOLS:
            print_success(f"Tool registered: {tool_name}")
        else:
            print_error(f"Tool missing: {tool_name}")
            all_present = False
    
    return all_present


def check_tool_functions():
    """Test that tool functions work."""
    print_header("3. Testing Tool Functions")
    
    try:
        print("  Testing scrape_website()...")
        result = scrape_website("https://example.com")
        if result.get("status") == "success":
            print_success(f"scrape_website() works - got {result['content_length']} chars")
        else:
            print_error(f"scrape_website() failed: {result.get('error')}")
    except Exception as e:
        print_error(f"scrape_website() error: {str(e)}")
    
    try:
        print("  Testing extract_links()...")
        result = extract_links("https://example.com")
        if result.get("status") == "success":
            print_success(f"extract_links() works - found {result['links_found']} links")
        else:
            print_error(f"extract_links() failed: {result.get('error')}")
    except Exception as e:
        print_error(f"extract_links() error: {str(e)}")
    
    try:
        print("  Testing get_metadata()...")
        result = get_metadata("https://example.com")
        if result.get("status") == "success":
            print_success(f"get_metadata() works - title: {result['title']}")
        else:
            print_error(f"get_metadata() failed: {result.get('error')}")
    except Exception as e:
        print_error(f"get_metadata() error: {str(e)}")


def check_configuration():
    """Display current configuration."""
    print_header("4. Current Configuration")
    
    print(f"  API Key:            {Config.ANTHROPIC_API_KEY[:15]}...")
    print(f"  Model:              {Config.CLAUDE_MODEL}")
    print(f"  Request Timeout:    {Config.REQUEST_TIMEOUT}s")
    print(f"  Max Content:        {Config.MAX_CONTENT_LENGTH} chars")
    print(f"  Max Iterations:     {Config.MAX_ITERATIONS}")
    print(f"  Temperature:        {Config.TEMPERATURE}")
    print(f"  Ollama URL:         {Config.OLLAMA_API_URL}")
    print(f"  User Agent:         {Config.USER_AGENT[:40]}...")


def check_agent_creation():
    """Test that agent can be created."""
    print_header("5. Testing Agent Creation")
    
    try:
        agent = WebScraperAgent()
        print_success("Agent created successfully")
        print(f"  Model: {agent.model}")
        print(f"  Max iterations: {Config.MAX_ITERATIONS}")
        return agent
    except Exception as e:
        print_error(f"Failed to create agent: {str(e)}")
        return None


def check_agent_tools(agent):
    """Check that agent has access to tools."""
    print_header("6. Checking Agent Tools")
    
    try:
        tools = agent.get_tool_definitions()
        print_success(f"Agent has {len(tools)} tools available:")
        for tool in tools:
            print(f"  - {tool['name']}: {tool['description']}")
        return len(tools) == 4
    except Exception as e:
        print_error(f"Error getting tools: {str(e)}")
        return False


def test_simple_task(agent):
    """Test a simple agent task."""
    print_header("7. Testing Simple Agent Task")
    
    if agent is None:
        print_warning("Skipping - agent creation failed")
        return False
    
    try:
        print("  Running: 'What's on example.com?'")
        print("  (This will use your API quota, so keeping it brief)")
        
        # Use a simple task to test
        response = agent.run("Get the title of example.com")
        
        if response and len(response) > 0:
            print_success("Agent responded successfully")
            print(f"  Response preview: {response[:100]}...")
            return True
        else:
            print_warning("Agent returned empty response")
            return False
            
    except Exception as e:
        print_error(f"Agent task failed: {str(e)}")
        return False


def run_all_tests(run_agent_test=False):
    """Run all tests."""
    print(f"""
{Colors.BOLD}{Colors.BLUE}
╔════════════════════════════════════════════════════════════════════════════╗
║          Claude Web Scraper Agent - Test Suite                            ║
╚════════════════════════════════════════════════════════════════════════════╝
{Colors.END}
    """)
    
    results = {}
    
    # Run tests
    results['api_key'] = check_api_key()
    
    if not results['api_key']:
        print_warning("\nCannot continue without API key. Please configure it first.")
        return results
    
    results['tools'] = check_tools()
    check_tool_functions()
    check_configuration()
    
    agent = check_agent_creation()
    results['agent'] = agent is not None
    
    if agent:
        results['agent_tools'] = check_agent_tools(agent)
        
        if run_agent_test:
            results['agent_task'] = test_simple_task(agent)
    
    # Print summary
    print_header("Test Summary")
    
    tests = [
        ('API Key', results.get('api_key', False)),
        ('Tools Registered', results.get('tools', False)),
        ('Agent Creation', results.get('agent', False)),
        ('Agent Tools', results.get('agent_tools', False)),
        ('Agent Task', results.get('agent_task', False)) if run_agent_test else None,
    ]
    
    passed = sum(1 for name, result in tests if result is not None and result)
    total = sum(1 for _, result in tests if result is not None)
    
    for name, result in tests:
        if result is None:
            continue
        if result:
            print_success(f"{name}")
        else:
            print_error(f"{name}")
    
    print(f"\n{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.END}\n")
    
    # Recommendations
    if results.get('api_key') and results.get('agent'):
        print_success("All basic checks passed! Agent is ready to use.")
        print("\nNext steps:")
        print("  1. Run: python web_scraper_agent.py")
        print("  2. Try advanced examples: python advanced_examples.py")
        print("  3. See README.md for full documentation")
    elif results.get('api_key'):
        print_warning("Some components failed. Please check the errors above.")
    else:
        print_error("API key not configured. Cannot proceed.")
    
    return results


if __name__ == "__main__":
    # Parse command line arguments
    run_agent_test = "--full" in sys.argv
    
    if run_agent_test:
        print("\nRunning FULL test suite (including API call)...")
        print("This will use your API quota.")
    else:
        print("\nRunning QUICK test suite (no API calls)...")
        print("Use --full flag to include API calls: python test_suite.py --full")
    
    results = run_all_tests(run_agent_test=run_agent_test)
    
    # Exit code
    if all(v for k, v in results.items() if v is not None):
        sys.exit(0)  # All tests passed
    else:
        sys.exit(1)  # Some tests failed
