#!/usr/bin/env python3
"""
Vibetest MCP Server Entry Point
Automated QA testing using Browser-Use agents
"""
import sys
import os

# Add the server directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import mcp
        import browser_use
        import playwright
        import langchain_google_genai
        import langchain_core
        import pydantic
        import screeninfo
        return True
    except ImportError:
        return False

def install_dependencies_if_needed():
    """Install dependencies if they're not available"""
    if not check_dependencies():
        print("Installing required dependencies...")
        try:
            from install_deps import install_dependencies
            if not install_dependencies():
                print("Failed to install dependencies. Please install manually:")
                print("pip install -r requirements.txt")
                print("playwright install chromium")
                return False
            print("Dependencies installed successfully!")
        except Exception as e:
            print(f"Error installing dependencies: {e}")
            return False
    return True

if __name__ == "__main__":
    # Install dependencies if needed
    if not install_dependencies_if_needed():
        sys.exit(1)
    
    # Import and run the MCP server
    try:
        from vibetest.mcp_server import run
        sys.exit(run())
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        sys.exit(1)
