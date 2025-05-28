#!/usr/bin/env python3
"""
Open Swagger UI Script

Simple script to open the Swagger UI documentation in the default browser.
Useful for quick access to API testing interface.

Author: AI Tutor Development Team
Version: 1.0
"""

import webbrowser
import time
import requests
import sys

def check_server_running(url: str, max_retries: int = 5) -> bool:
    """Check if the server is running and accessible."""
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        
        if i < max_retries - 1:
            print(f"Server not ready, retrying in 2 seconds... ({i+1}/{max_retries})")
            time.sleep(2)
    
    return False

def main():
    """Main function to open Swagger UI."""
    base_url = "http://localhost:8000"
    docs_url = f"{base_url}/docs"
    
    print("🚀 AI Agent Mem0 API - Swagger UI Launcher")
    print("=" * 50)
    
    # Check if server is running
    print("Checking if server is running...")
    if not check_server_running(base_url):
        print("❌ Server is not running!")
        print("\nTo start the server, run:")
        print("uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        sys.exit(1)
    
    print("✅ Server is running!")
    
    # Get API info
    try:
        response = requests.get(base_url)
        api_info = response.json()
        print(f"📋 API: {api_info['message']} v{api_info['version']}")
        print(f"🌍 Environment: {api_info['environment']}")
        print(f"📊 Status: {api_info['status']}")
    except Exception as e:
        print(f"⚠️  Could not get API info: {e}")
    
    print(f"\n🌐 Opening Swagger UI: {docs_url}")
    
    # Open Swagger UI in browser
    try:
        webbrowser.open(docs_url)
        print("✅ Swagger UI opened in your default browser!")
        
        print("\n📚 Available Documentation URLs:")
        print(f"  • Swagger UI: {docs_url}")
        print(f"  • ReDoc: {base_url}/redoc")
        print(f"  • OpenAPI JSON: {base_url}/openapi.json")
        
        print("\n🧪 Quick Test Endpoints:")
        print(f"  • Health Check: {base_url}/health")
        print(f"  • Detailed Health: {base_url}/api/v1/health/detailed")
        print(f"  • Chat Endpoint: {base_url}/api/v1/chat")
        
        print("\n💡 Tips for Testing:")
        print("  1. Try the health endpoints first to verify system status")
        print("  2. Use the chat endpoint with a unique user_id")
        print("  3. Check the response examples in the documentation")
        print("  4. Use the 'Try it out' feature to test endpoints directly")
        
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"Please manually open: {docs_url}")

if __name__ == "__main__":
    main() 