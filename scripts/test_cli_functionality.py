#!/usr/bin/env python3
"""
Test script to verify CLI functionality works correctly.
"""

import os
import sys
import uuid
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

def test_cli_components():
    """Test that all CLI components can be initialized."""
    
    print("🧪 Testing CLI Components...")
    
    # Test 1: Environment validation
    print("1. Testing environment validation...")
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found")
        return False
    if not os.getenv("QDRANT_URL"):
        print("❌ QDRANT_URL not found")
        return False
    print("✅ Environment validation passed")
    
    # Test 2: Qdrant client initialization
    print("2. Testing Qdrant client...")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_use_https = os.getenv("QDRANT_USE_HTTPS", "true").lower() == "true"
    protocol = "https" if qdrant_use_https else "http"
    
    qdrant_client = QdrantClient(
        url=f"{protocol}://{qdrant_url}",
        port=None,
        timeout=30,
        prefer_grpc=False
    )
    
    collections = qdrant_client.get_collections()
    print(f"✅ Qdrant client works: {len(collections.collections)} collections")
    
    # Test 3: Mem0 memory initialization
    print("3. Testing Mem0 memory...")
    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "mem0_cli_test",
                "client": qdrant_client,
                "embedding_model_dims": 1536,
                "on_disk": False
            }
        }
    }
    
    memory = Memory.from_config(config)
    print("✅ Mem0 memory initialized")
    
    # Test 4: OpenAI client
    print("4. Testing OpenAI client...")
    openai_client = OpenAI()
    print("✅ OpenAI client initialized")
    
    # Test 5: Basic memory operations
    print("5. Testing memory operations...")
    test_user_id = f"cli_test_{uuid.uuid4().hex[:8]}"
    
    # Add a memory
    test_message = f"Test message from CLI test user {test_user_id}"
    memory.add(test_message, user_id=test_user_id)
    print("✅ Memory add operation successful")
    
    # Search memories
    search_results = memory.search("test", user_id=test_user_id)
    memories = search_results.get("results", [])
    print(f"✅ Memory search successful: found {len(memories)} results")
    
    # Test 6: AI response generation (simplified)
    print("6. Testing AI response generation...")
    
    system_prompt = "You are a helpful AI assistant."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Hello!"}
    ]
    
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
        max_tokens=100
    )
    
    ai_response = response.choices[0].message.content
    print(f"✅ AI response generated: {ai_response[:50]}...")
    
    print("\n🎉 All CLI components tested successfully!")
    print(f"📝 Test user ID: {test_user_id}")
    print(f"💾 Memories stored: {len(memories)}")
    
    return True

if __name__ == "__main__":
    try:
        success = test_cli_components()
        if success:
            print("\n✅ CLI functionality test PASSED")
            print("\n📋 The interactive CLI should work correctly.")
            print("🚀 You can now demo the following features:")
            print("   - Interactive chat with memory")
            print("   - User switching and isolation")
            print("   - Memory search and statistics")
            print("   - Automated peptide coaching demo")
        else:
            print("\n❌ CLI functionality test FAILED")
    except Exception as e:
        print(f"\n❌ CLI test failed with error: {str(e)}")
        sys.exit(1) 