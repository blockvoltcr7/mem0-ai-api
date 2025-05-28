"""
Pytest Configuration for Qdrant Integration Tests

Provides fixtures and configuration for testing the AI Agent Mem0 API
with Qdrant vector database integration.

Author: AI Tutor Development Team
Version: 1.0
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
import pytest_asyncio
import asyncio
import httpx
import allure
from typing import AsyncGenerator, Dict, Any
from app.core.config import settings

# Test configuration
TEST_BASE_URL = "http://localhost:8000"
TEST_TIMEOUT = 30.0

# @pytest.fixture(scope="session")
# def event_loop():
#     """Create an instance of the default event loop for the test session."""
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope="function")
async def test_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Create an async HTTP client for testing the API.
    
    This fixture provides a function-scoped HTTP client that can be used
    for individual tests.
    """
    async with httpx.AsyncClient(
        base_url=TEST_BASE_URL,
        timeout=TEST_TIMEOUT
    ) as client:
        yield client

@pytest.fixture(scope="function")
def test_user_data() -> Dict[str, Any]:
    """
    Provide test user data for chat requests.
    
    Returns a dictionary with test user information that can be
    customized for different test scenarios.
    """
    return {
        "user_id": "test_user_qdrant_001",
        "session_id": "qdrant_test_session_2024",
        "metadata": {
            "domain": "qdrant_testing",
            "test_type": "integration",
            "environment": "test"
        }
    }

@pytest.fixture(scope="function")
def peptide_coaching_user() -> Dict[str, Any]:
    """
    Provide test data for peptide coaching scenario.
    
    Returns user data specifically for testing peptide coaching
    conversations and memory persistence.
    """
    return {
        "user_id": "peptide_coach_test_001",
        "session_id": "peptide_consultation_2024",
        "metadata": {
            "domain": "peptide_coaching",
            "experience_level": "beginner",
            "goals": ["recovery", "muscle_growth"],
            "test_scenario": "peptide_coaching"
        }
    }

@pytest.fixture(scope="function")
def sports_medicine_user() -> Dict[str, Any]:
    """
    Provide test data for sports medicine scenario.
    
    Returns user data for testing sports medicine conversations
    and context-aware responses.
    """
    return {
        "user_id": "sports_med_test_001",
        "session_id": "sports_consultation_2024",
        "metadata": {
            "domain": "sports_medicine",
            "athlete_type": "endurance",
            "sport": "cycling",
            "test_scenario": "sports_medicine"
        }
    }

@pytest.fixture(scope="function")
def chat_request_factory():
    """
    Factory fixture for creating chat requests.
    
    Returns a function that can create chat request payloads
    with customizable parameters.
    """
    def _create_chat_request(
        user_id: str,
        message: str,
        session_id: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        request = {
            "user_id": user_id,
            "message": message
        }
        if session_id:
            request["session_id"] = session_id
        if metadata:
            request["metadata"] = metadata
        return request
    
    return _create_chat_request

@pytest.fixture(scope="function")
def allure_environment_setup():
    """
    Set up Allure environment information.
    
    Adds environment details to Allure reports for better
    test result tracking and debugging.
    """
    allure.dynamic.feature("Qdrant Integration")
    allure.dynamic.label("test_environment", "integration")
    allure.dynamic.label("api_base_url", TEST_BASE_URL)

@pytest_asyncio.fixture(scope="function")
async def setup_test_environment():
    """
    Set up the test environment before running tests.
    
    This fixture ensures the API is ready and all services
    are properly initialized before tests begin.
    """
    # Wait for the application to be ready
    await asyncio.sleep(1)
    
    # Verify basic connectivity
    async with httpx.AsyncClient(base_url=TEST_BASE_URL, timeout=TEST_TIMEOUT) as client:
        try:
            response = await client.get("/health")
            if response.status_code != 200:
                pytest.fail(f"API health check failed: {response.status_code}")
        except Exception as e:
            pytest.fail(f"Failed to connect to API: {str(e)}")

@pytest_asyncio.fixture(scope="function")
async def clean_test_memories(test_client: httpx.AsyncClient, test_user_data: Dict[str, Any]):
    """
    Clean up test memories after each test.
    
    This fixture ensures that test memories don't interfere
    with subsequent tests by cleaning up after each test.
    """
    yield
    
    # Note: In a real implementation, you might want to add
    # a cleanup endpoint or direct Qdrant cleanup here
    # For now, we rely on unique user IDs per test

# Pytest markers for test categorization
pytest_plugins = ["allure_pytest"]

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "health: mark test as health check test"
    )
    config.addinivalue_line(
        "markers", "chat: mark test as chat functionality test"
    )
    config.addinivalue_line(
        "markers", "memory: mark test as memory persistence test"
    )
    config.addinivalue_line(
        "markers", "error: mark test as error handling test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    ) 