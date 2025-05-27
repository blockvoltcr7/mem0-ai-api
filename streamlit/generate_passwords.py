#!/usr/bin/env python3
"""
Generate password hashes for streamlit-authenticator.

This script generates bcrypt password hashes for use in the authentication system.
"""

import streamlit_authenticator as stauth

def generate_password_hash(password: str) -> str:
    """Generate a bcrypt hash for the given password."""
    hasher = stauth.Hasher()
    return hasher.hash(password)

if __name__ == "__main__":
    # Generate hashes for demo passwords
    demo_password = "demo123"
    test_password = "demo123"
    
    demo_hash = generate_password_hash(demo_password)
    test_hash = generate_password_hash(test_password)
    
    print(f"Demo password hash: {demo_hash}")
    print(f"Test password hash: {test_hash}")
    
    # Update config.yaml format
    print("\nConfig YAML format:")
    print(f"""credentials:
  usernames:
    demo_user:
      email: demo@healthcoach.ai
      name: Demo User
      password: {demo_hash}
    test_user:
      email: test@healthcoach.ai
      name: Test User
      password: {test_hash}""") 