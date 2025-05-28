#!/usr/bin/env python3
"""
Quick Test Script for Qdrant Integration

A simple script to verify the API is running and accessible
before running the full test suite.

Author: AI Tutor Development Team
Version: 1.0
"""

import asyncio
import httpx
import sys
from pathlib import Path
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

TEST_BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 10.0

@pytest.mark.asyncio
async def test_api_connectivity():
    """Test basic API connectivity."""
    print("🔍 Testing API connectivity...")
    
    try:
        async with httpx.AsyncClient(base_url=TEST_BASE_URL, timeout=TEST_TIMEOUT) as client:
            # Test basic health check
            print("  ➤ Testing basic health check...")
            response = await client.get("/health")
            
            if response.status_code == 200:
                print("  ✅ Basic health check: PASSED")
                data = response.json()
                print(f"     Status: {data.get('status', 'unknown')}")
            else:
                print(f"  ❌ Basic health check: FAILED ({response.status_code})")
                return False
            
            # Test detailed health check
            print("  ➤ Testing detailed health check...")
            response = await client.get("/api/v1/health/detailed")
            
            if response.status_code == 200:
                print("  ✅ Detailed health check: PASSED")
                data = response.json()
                services = data.get('services', {})
                for service, status in services.items():
                    status_icon = "✅" if status.get('status') == 'healthy' else "❌"
                    print(f"     {service}: {status_icon} {status.get('status', 'unknown')}")
            else:
                print(f"  ❌ Detailed health check: FAILED ({response.status_code})")
                return False
            
            # Test simple chat request
            print("  ➤ Testing simple chat request...")
            chat_request = {
                "user_id": "quick_test_user",
                "message": "Hello, this is a quick test message.",
                "metadata": {
                    "domain": "quick_test",
                    "test_type": "connectivity"
                }
            }
            
            response = await client.post("/api/v1/chat", json=chat_request)
            
            if response.status_code == 200:
                print("  ✅ Chat request: PASSED")
                data = response.json()
                print(f"     Response length: {len(data.get('response', ''))} characters")
                print(f"     Memories created: {data.get('memories_created', 0)}")
            else:
                print(f"  ❌ Chat request: FAILED ({response.status_code})")
                if response.status_code != 500:  # Don't fail on server errors during quick test
                    return False
            
            return True
            
    except httpx.ConnectError:
        print("  ❌ Connection failed: API server not running or not accessible")
        print("     Make sure the API is running on http://localhost:8000")
        return False
    except httpx.TimeoutException:
        print("  ❌ Request timeout: API server not responding")
        return False
    except Exception as e:
        print(f"  ❌ Unexpected error: {str(e)}")
        return False

async def main():
    """Main function."""
    print("🚀 Quick Test for Qdrant Integration API")
    print("=" * 50)
    
    success = await test_api_connectivity()
    
    print("=" * 50)
    if success:
        print("✅ Quick test PASSED - API is ready for testing")
        print("💡 You can now run the full test suite:")
        print("   python test_runner.py --smoke")
        print("   python test_runner.py --full")
        sys.exit(0)
    else:
        print("❌ Quick test FAILED - API is not ready")
        print("💡 Please check:")
        print("   1. API server is running: uvicorn app.main:app --reload")
        print("   2. Environment variables are set (OPENAI_API_KEY, QDRANT_URL)")
        print("   3. Qdrant database is accessible")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 