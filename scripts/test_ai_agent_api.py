#!/usr/bin/env python3
"""
AI Agent API Test Script

Simple script to test the AI Agent Mem0 API functionality.
Useful for manual testing and verification.

Author: AI Tutor Development Team
Version: 1.0
"""

import requests
import json
import time
import uuid

def test_api_endpoints():
    """Test the AI Agent API endpoints."""
    
    base_url = "http://localhost:8000/api/v1"
    
    print("🤖 Testing AI Agent Mem0 API")
    print("=" * 50)
    
    # Test health endpoints
    print("\n1. Testing Health Endpoints")
    print("-" * 30)
    
    try:
        # Basic health check
        response = requests.get(f"{base_url}/health")
        print(f"Basic Health: {response.status_code}")
        if response.status_code == 200:
            print(f"Status: {response.json()['status']}")
        
        # Detailed health check
        response = requests.get(f"{base_url}/health/detailed")
        print(f"Detailed Health: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"Overall Status: {health_data['status']}")
            for service, info in health_data['services'].items():
                print(f"  {service}: {info['status']}")
    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   uvicorn app.main:app --reload")
        return
    
    # Test chat endpoint
    print("\n2. Testing Chat Endpoint")
    print("-" * 30)
    
    test_user_id = f"test_user_{uuid.uuid4().hex[:8]}"
    
    # First conversation
    chat_request = {
        "user_id": test_user_id,
        "message": "Hello! I'm interested in learning about BPC-157 peptide.",
        "metadata": {
            "domain": "peptide_coaching",
            "test_session": "api_test"
        }
    }
    
    print(f"User ID: {test_user_id}")
    print(f"Message: {chat_request['message']}")
    
    try:
        start_time = time.time()
        response = requests.post(f"{base_url}/chat", json=chat_request)
        end_time = time.time()
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Time: {(end_time - start_time):.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Memories Found: {data['memories_found']}")
            print(f"Memories Created: {data['memories_created']}")
            print(f"API Response Time: {data['response_time_ms']}ms")
            print(f"AI Response: {data['response'][:100]}...")
            
            # Second conversation to test memory
            print("\n3. Testing Memory Persistence")
            print("-" * 30)
            
            second_request = {
                "user_id": test_user_id,
                "message": "What peptide did I just ask about?",
                "metadata": {"domain": "peptide_coaching"}
            }
            
            response2 = requests.post(f"{base_url}/chat", json=second_request)
            if response2.status_code == 200:
                data2 = response2.json()
                print(f"Memories Found: {data2['memories_found']}")
                print(f"AI Response: {data2['response'][:100]}...")
                
                if data2['memories_found'] > 0:
                    print("✅ Memory persistence working!")
                else:
                    print("⚠️  No memories found - check Mem0 configuration")
            
        else:
            print(f"❌ Chat request failed: {response.text}")
    
    except Exception as e:
        print(f"❌ Error testing chat endpoint: {str(e)}")
    
    # Test error handling
    print("\n4. Testing Error Handling")
    print("-" * 30)
    
    # Test invalid request
    invalid_request = {"message": "Test without user_id"}
    response = requests.post(f"{base_url}/chat", json=invalid_request)
    print(f"Invalid request status: {response.status_code}")
    
    if response.status_code == 422:
        print("✅ Validation error handling working")
    
    # Test empty user_id
    empty_user_request = {"user_id": "", "message": "Test with empty user_id"}
    response = requests.post(f"{base_url}/chat", json=empty_user_request)
    print(f"Empty user_id status: {response.status_code}")
    
    if response.status_code == 400:
        print("✅ Empty user_id error handling working")
    
    print("\n" + "=" * 50)
    print("🎉 API testing completed!")

if __name__ == "__main__":
    test_api_endpoints() 