"""
Basic tests for the Gradio Health Coach AI - Peptide Therapy Assistant
"""

import pytest
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import gradio as gr
        import openai
        import mem0
        import qdrant_client
        import pydantic
        print("✅ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration."""
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    
    if not openai_key:
        print("⚠️ Warning: OPENAI_API_KEY not set - app will fail to initialize")
        return False
    
    print(f"✅ OPENAI_API_KEY configured")
    print(f"✅ QDRANT_URL: {qdrant_url}")
    return True

def test_demo_users_configuration():
    """Test demo users configuration."""
    try:
        from app import DEMO_USERS
        
        expected_users = ["john", "jane", "jarvis"]
        actual_users = list(DEMO_USERS.keys())
        
        assert set(expected_users) == set(actual_users), f"Expected {expected_users}, got {actual_users}"
        
        # Validate user data structure
        for user_key, user_data in DEMO_USERS.items():
            assert "name" in user_data, f"User {user_key} missing 'name'"
            assert "email" in user_data, f"User {user_key} missing 'email'"
            assert "user_id" in user_data, f"User {user_key} missing 'user_id'"
        
        print("✅ Demo users configured correctly")
        print(f"   Users: {', '.join(user_data['name'] for user_data in DEMO_USERS.values())}")
        return True
    except Exception as e:
        print(f"❌ Demo users test failed: {e}")
        return False

def test_user_health_model():
    """Test UserHealth data model."""
    try:
        from app import UserHealth
        
        # Test default initialization
        profile = UserHealth()
        assert profile.peptide_usage is None
        assert profile.bpc157_usage is None
        assert profile.health_goals == []
        assert profile.medical_conditions == []
        assert profile.current_medications == []
        assert profile.onboarding_completed is False
        
        # Test with data
        profile_data = UserHealth(
            peptide_usage=True,
            bpc157_usage=True,
            bpc157_dosage="250mcg daily",
            bpc157_duration="1-3 months",
            health_goals=["Tissue repair and healing"],
            medical_conditions=["None"],
            current_medications=["Vitamin D"],
            onboarding_completed=True
        )
        
        assert profile_data.peptide_usage is True
        assert profile_data.bpc157_usage is True
        assert profile_data.bpc157_dosage == "250mcg daily"
        assert "Tissue repair and healing" in profile_data.health_goals
        
        print("✅ UserHealth model working correctly")
        return True
    except Exception as e:
        print(f"❌ UserHealth model test failed: {e}")
        return False

def test_app_initialization():
    """Test that the app can be imported and basic functions work."""
    try:
        from app import get_user_profile, save_user_profile, create_user_session, UserHealth
        
        # Test user profile management
        test_user_id = "test_user"
        profile = get_user_profile(test_user_id)
        assert isinstance(profile, UserHealth)
        
        # Test saving profile
        profile.peptide_usage = True
        save_user_profile(test_user_id, profile)
        
        # Test retrieving saved profile
        retrieved_profile = get_user_profile(test_user_id)
        assert retrieved_profile.peptide_usage is True
        
        # Test user session creation
        user_id, user_name, user_email, status = create_user_session("john")
        assert user_id == "john_demo_user"
        assert user_name == "John Smith"
        assert "✅" in status
        
        print("✅ App initialization and basic functions working")
        return True
    except Exception as e:
        print(f"❌ App initialization test failed: {e}")
        return False

def test_gradio_interface():
    """Test that the Gradio interface can be created."""
    try:
        from app import create_interface
        
        # This will test that the interface can be created without errors
        app = create_interface()
        assert app is not None
        
        print("✅ Gradio interface created successfully")
        return True
    except Exception as e:
        print(f"❌ Gradio interface test failed: {e}")
        return False

def run_all_tests():
    """Run all tests."""
    print("🧬 Testing Health Coach AI - Peptide Therapy Assistant (Gradio)")
    print("=" * 60)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("Environment Variables", test_environment_variables),
        ("Demo Users Configuration", test_demo_users_configuration),
        ("UserHealth Model", test_user_health_model),
        ("App Initialization", test_app_initialization),
        ("Gradio Interface", test_gradio_interface),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
    else:
        print("⚠️ Some tests failed. Please check the configuration and dependencies.")
    
    return passed == total

if __name__ == "__main__":
    run_all_tests() 