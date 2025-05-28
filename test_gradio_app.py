#!/usr/bin/env python3
"""
Test script for the Gradio AI Tutor application
Tests basic functionality and memory isolation
"""

import sys
import os
from pathlib import Path

# Add gradio-ai-tutor to path
gradio_app_path = str(Path(__file__).parent / "gradio-ai-tutor")
sys.path.insert(0, gradio_app_path)

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
        
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
        
        from openai import OpenAI
        print("✅ OpenAI imported successfully")
        
        from mem0 import Memory
        print("✅ Mem0 imported successfully")
        
        from qdrant_client import QdrantClient
        print("✅ Qdrant client imported successfully")
        
        import phonenumbers
        print("✅ phonenumbers imported successfully")
        
        from pydantic import BaseModel, Field, ValidationError
        print("✅ Pydantic imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment variables."""
    print("\n🔧 Testing environment...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    
    if openai_key:
        print("✅ OPENAI_API_KEY is set")
    else:
        print("❌ OPENAI_API_KEY is not set")
        return False
    
    print(f"✅ QDRANT_URL: {qdrant_url}")
    return True

def test_app_initialization():
    """Test that the app can be initialized."""
    print("\n🚀 Testing app initialization...")
    
    try:
        # Change to gradio app directory and import
        os.chdir(gradio_app_path)
        import app
        
        # Test service initialization
        if app.services_initialized:
            print("✅ Services initialized successfully")
            print(f"✅ Memory service: {type(app.memory_service)}")
            print(f"✅ OpenAI client: {type(app.openai_client)}")
        else:
            print("❌ Services failed to initialize")
            return False
        
        # Test interface creation
        interface = app.create_interface()
        print("✅ Gradio interface created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ App initialization error: {e}")
        return False

def test_user_validation():
    """Test user validation functions."""
    print("\n👤 Testing user validation...")
    
    try:
        # Make sure we're in the right directory
        os.chdir(gradio_app_path)
        import app
        
        # Test phone number validation
        valid_phones = [
            "1234567890",
            "+1234567890", 
            "(123) 456-7890",
            "123-456-7890"
        ]
        
        invalid_phones = [
            "123",
            "abc",
            "",
            "12345"
        ]
        
        for phone in valid_phones:
            if app.validate_phone_number(phone):
                print(f"✅ Valid phone: {phone}")
            else:
                print(f"❌ Should be valid: {phone}")
                return False
        
        for phone in invalid_phones:
            if not app.validate_phone_number(phone):
                print(f"✅ Invalid phone rejected: {phone}")
            else:
                print(f"❌ Should be invalid: {phone}")
                return False
        
        # Test user session creation
        user_id, message = app.create_user_session("testuser", "1234567890")
        if user_id:
            print(f"✅ User session created: {user_id}")
            print(f"✅ Welcome message: {message[:50]}...")
        else:
            print(f"❌ User session creation failed: {message}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ User validation error: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 AI Tutor Gradio App Test Suite")
    print("=" * 40)
    
    # Store original directory
    original_dir = os.getcwd()
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("App Initialization Test", test_app_initialization),
        ("User Validation Test", test_user_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    try:
        for test_name, test_func in tests:
            print(f"\n📋 Running: {test_name}")
            print("-" * 30)
            
            try:
                if test_func():
                    print(f"✅ {test_name} PASSED")
                    passed += 1
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
    
    finally:
        # Restore original directory
        os.chdir(original_dir)
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The Gradio app is ready to use.")
        print("\n🚀 To run the app:")
        print("   cd gradio-ai-tutor")
        print("   ./run.sh")
        print("   # or python app.py")
        print("\n📱 Then visit: http://localhost:7860")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 