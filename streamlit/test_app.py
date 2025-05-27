#!/usr/bin/env python3
"""
Test script for Health Coach AI Streamlit application.

This script tests the core components without running the full Streamlit app.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import streamlit_authenticator as stauth
from pydantic import ValidationError

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test that required environment variables are set."""
    print("🔍 Testing environment variables...")
    
    required_vars = ["OPENAI_API_KEY", "QDRANT_URL"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def test_authentication():
    """Test authentication system."""
    print("🔐 Testing authentication system...")
    
    try:
        # Test password hashing
        hasher = stauth.Hasher()
        test_hash = hasher.hash("demo123")
        print(f"✅ Password hashing works: {test_hash[:20]}...")
        
        # Test authenticator creation
        config = {
            'credentials': {
                'usernames': {
                    'test_user': {
                        'email': 'test@example.com',
                        'name': 'Test User',
                        'password': test_hash
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'test_key',
                'name': 'test_cookie'
            },
            'preauthorized': {
                'emails': ['test@example.com']
            }
        }
        
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days']
        )
        
        print("✅ Authentication system initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Authentication test failed: {str(e)}")
        return False

def test_data_models():
    """Test Pydantic data models."""
    print("📋 Testing data models...")
    
    try:
        # Import the UserHealth model
        sys.path.insert(0, str(Path(__file__).parent))
        from app import UserHealth
        
        # Test valid profile creation
        profile = UserHealth(
            peptide_usage=True,
            bpc157_usage=True,
            bpc157_dosage="250mcg daily",
            bpc157_duration="2-4 weeks",
            health_goals=["Tissue repair and healing", "Injury recovery"],
            medical_conditions=["None"],
            current_medications=["Vitamin D", "Omega-3"],
            onboarding_completed=True
        )
        
        print("✅ UserHealth model validation works")
        print(f"   - Peptide usage: {profile.peptide_usage}")
        print(f"   - BPC-157 dosage: {profile.bpc157_dosage}")
        print(f"   - Health goals: {len(profile.health_goals)} goals")
        
        # Test default values
        empty_profile = UserHealth()
        print(f"✅ Default profile creation works (onboarding: {empty_profile.onboarding_completed})")
        
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {str(e)}")
        return False

def test_memory_system_imports():
    """Test that memory system dependencies can be imported."""
    print("🧠 Testing memory system imports...")
    
    try:
        from openai import OpenAI
        print("✅ OpenAI client import successful")
        
        from mem0 import Memory
        print("✅ Mem0 Memory import successful")
        
        from qdrant_client import QdrantClient
        print("✅ Qdrant client import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system import test failed: {str(e)}")
        return False

def test_streamlit_imports():
    """Test Streamlit and related imports."""
    print("🎨 Testing Streamlit imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
        
        import streamlit_authenticator as stauth
        print("✅ Streamlit authenticator import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit import test failed: {str(e)}")
        return False

def main():
    """Run all tests."""
    print("🧬 Health Coach AI - Component Tests")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_streamlit_imports,
        test_authentication,
        test_data_models,
        test_memory_system_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("  streamlit run streamlit/app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 