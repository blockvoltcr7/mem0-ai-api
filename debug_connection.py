#!/usr/bin/env python3
"""
Debug Connection Script

Test Qdrant and OpenAI connections independently to diagnose issues.
"""

import os
from qdrant_client import QdrantClient
from openai import OpenAI
from app.core.config import settings

def test_qdrant_connection():
    """Test Qdrant connection."""
    print("🔍 Testing Qdrant Connection")
    print("-" * 40)
    
    try:
        print(f"URL: {settings.qdrant_url}")
        print(f"Port: {settings.qdrant_port}")
        print(f"HTTPS: {settings.qdrant_use_https}")
        
        # Use the same pattern as the working test files
        protocol = "https" if settings.qdrant_use_https else "http"
        qdrant_url = f"{protocol}://{settings.qdrant_url}"
        
        print(f"Connecting to: {qdrant_url}")
        
        # Create Qdrant client using the proven working pattern
        # Critical: port=None prevents :6333 from being appended to URL
        client = QdrantClient(
            url=qdrant_url,
            port=None,  # Critical: prevents :6333 from being appended to URL
            timeout=30,
            prefer_grpc=False  # Force REST API usage
        )
        
        # Test connection
        collections = client.get_collections()
        print(f"✅ Connected successfully!")
        print(f"Collections found: {len(collections.collections)}")
        
        for collection in collections.collections:
            print(f"  - {collection.name}")
        
        return True, client
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False, None

def test_openai_connection():
    """Test OpenAI connection."""
    print("\n🔍 Testing OpenAI Connection")
    print("-" * 40)
    
    try:
        print(f"API Key: {settings.openai_api_key[:10]}...")
        
        client = OpenAI(api_key=settings.openai_api_key)
        
        # Test with a simple model list call
        models = client.models.list()
        print(f"✅ Connected successfully!")
        print(f"Models available: {len(models.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def test_mem0_initialization():
    """Test Mem0 initialization."""
    print("\n🔍 Testing Mem0 Initialization")
    print("-" * 40)
    
    try:
        from mem0 import Memory
        
        # Test Qdrant connection first
        qdrant_ok, qdrant_client = test_qdrant_connection()
        if not qdrant_ok:
            print("❌ Cannot initialize Mem0 - Qdrant connection failed")
            return False
        
        # Test OpenAI connection
        openai_ok = test_openai_connection()
        if not openai_ok:
            print("❌ Cannot initialize Mem0 - OpenAI connection failed")
            return False
        
        # Configure Mem0
        config = {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": settings.ai_model,
                    "temperature": settings.ai_temperature,
                    "max_tokens": settings.ai_max_tokens
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": settings.mem0_collection_name,
                    "client": qdrant_client,
                    "embedding_model_dims": 1536,
                    "on_disk": False
                }
            }
        }
        
        print(f"Collection: {settings.mem0_collection_name}")
        
        # Initialize Mem0
        memory = Memory.from_config(config)
        print("✅ Mem0 initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Mem0 initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 AI Agent Connection Debug")
    print("=" * 50)
    
    # Test individual components
    qdrant_ok, _ = test_qdrant_connection()
    openai_ok = test_openai_connection()
    
    if qdrant_ok and openai_ok:
        mem0_ok = test_mem0_initialization()
        
        if mem0_ok:
            print("\n🎉 All connections successful!")
        else:
            print("\n❌ Mem0 initialization failed")
    else:
        print("\n❌ Basic connections failed")
    
    print("\n" + "=" * 50) 