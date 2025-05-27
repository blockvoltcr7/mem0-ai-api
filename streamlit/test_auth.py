#!/usr/bin/env python3
"""
Simple test script to verify authentication functionality.
"""

import yaml
from pathlib import Path
from yaml.loader import SafeLoader

def load_user_config():
    """Load user configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    try:
        with open(config_path, 'r') as file:
            config = yaml.load(file, Loader=SafeLoader)
        return config
    except Exception as e:
        print(f"Failed to load user configuration: {str(e)}")
        return None

def authenticate_user(username: str, password: str):
    """Authenticate user with simple username/password check."""
    config = load_user_config()
    if not config:
        return None
    
    users = config.get('credentials', {}).get('usernames', {})
    if username in users:
        user_data = users[username]
        if user_data.get('password') == password:
            return {
                'username': username,
                'name': user_data.get('name', username),
                'email': user_data.get('email', '')
            }
    return None

def test_authentication():
    """Test the authentication system."""
    print("Testing Authentication System")
    print("=" * 40)
    
    # Test cases
    test_cases = [
        ("demo_user", "demo123", True),
        ("test_user", "test123", True),
        ("admin_user", "admin123", True),
        ("demo_user", "wrong_password", False),
        ("nonexistent_user", "any_password", False),
    ]
    
    for username, password, should_succeed in test_cases:
        result = authenticate_user(username, password)
        success = result is not None
        
        status = "✅ PASS" if success == should_succeed else "❌ FAIL"
        print(f"{status} - {username}:{password} -> {'Success' if success else 'Failed'}")
        
        if success and should_succeed:
            print(f"    User: {result['name']} ({result['email']})")
    
    print("\nConfiguration loaded successfully!")
    config = load_user_config()
    if config:
        users = config.get('credentials', {}).get('usernames', {})
        print(f"Available users: {list(users.keys())}")

if __name__ == "__main__":
    test_authentication() 