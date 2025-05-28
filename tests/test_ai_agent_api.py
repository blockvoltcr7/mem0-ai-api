#!/usr/bin/env python3
"""
AI Agent API Integration Tests

Comprehensive tests for the AI Agent Mem0 API endpoints.
Tests the chat functionality, health checks, and error handling.

Author: AI Tutor Development Team
Version: 1.0
"""

import pytest
import allure
import uuid
import time
from typing import Dict, Any

@allure.epic("AI Agent API")
@allure.feature("Chat Endpoint")
class TestAIAgentChatAPI:
    """Test suite for AI Agent Chat API functionality."""

    @pytest.fixture
    def test_user_id(self):
        """Generate a unique user ID for testing."""
        user_id = f"api_test_user_{uuid.uuid4().hex[:8]}"
        allure.attach(
            user_id,
            name="Test User ID",
            attachment_type=allure.attachment_type.TEXT
        )
        return user_id

    @pytest.fixture
    def sample_chat_request(self, test_user_id):
        """Sample chat request payload."""
        return {
            "user_id": test_user_id,
            "message": "I'm interested in learning about BPC-157 peptide for healing.",
            "metadata": {
                "domain": "peptide_coaching",
                "location": "test_environment",
                "urgency": "normal"
            }
        }

    @allure.story("Basic Chat Functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_chat_endpoint_basic_functionality(self, session, api_base_url, fastapi_server, sample_chat_request):
        """Test basic chat endpoint functionality with new user."""
        
        with allure.step("Send chat request to API"):
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=sample_chat_request
            )

        with allure.step("Verify successful response"):
            assert response.status_code == 200
            allure.attach(
                str(response.status_code),
                name="Status Code",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Parse and validate response structure"):
            data = response.json()
            allure.attach(
                str(data),
                name="Response JSON",
                attachment_type=allure.attachment_type.TEXT
            )

            # Validate required fields
            assert "response" in data
            assert "memories_found" in data
            assert "memories_created" in data
            assert "user_id" in data
            assert "response_time_ms" in data

        with allure.step("Validate response content"):
            assert isinstance(data["response"], str)
            assert len(data["response"]) > 0
            assert data["user_id"] == sample_chat_request["user_id"]
            assert isinstance(data["memories_found"], int)
            assert isinstance(data["memories_created"], int)
            assert isinstance(data["response_time_ms"], int)
            
            # For new user, memories_found should be 0, memories_created should be 1
            assert data["memories_found"] == 0
            assert data["memories_created"] == 1

    @allure.story("Memory Persistence")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_chat_memory_persistence(self, session, api_base_url, fastapi_server, test_user_id):
        """Test that memories persist across multiple conversations."""
        
        # First conversation
        first_request = {
            "user_id": test_user_id,
            "message": "I'm using BPC-157 for injury recovery.",
            "metadata": {"domain": "peptide_coaching"}
        }

        with allure.step("Send first chat message"):
            response1 = session.post(
                f"{api_base_url}/api/v1/chat",
                json=first_request
            )
            assert response1.status_code == 200
            data1 = response1.json()
            
            allure.attach(
                str(data1),
                name="First Response",
                attachment_type=allure.attachment_type.TEXT
            )

        # Second conversation - should have memory from first
        second_request = {
            "user_id": test_user_id,
            "message": "What peptide am I currently using?",
            "metadata": {"domain": "peptide_coaching"}
        }

        with allure.step("Send second chat message"):
            response2 = session.post(
                f"{api_base_url}/api/v1/chat",
                json=second_request
            )
            assert response2.status_code == 200
            data2 = response2.json()
            
            allure.attach(
                str(data2),
                name="Second Response",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verify memory persistence"):
            # Second response should have found memories from first conversation
            assert data2["memories_found"] > 0
            assert data2["memories_created"] == 1
            
            # Response should reference BPC-157 based on memory
            response_text = data2["response"].lower()
            assert "bpc" in response_text or "bpc-157" in response_text

    @allure.story("Session-based Memory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_session_based_memory(self, session, api_base_url, fastapi_server, test_user_id):
        """Test session-based memory grouping."""
        
        session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        
        request_with_session = {
            "user_id": test_user_id,
            "message": "I'm planning a peptide cycle for muscle recovery.",
            "session_id": session_id,
            "metadata": {"domain": "peptide_coaching", "session_type": "planning"}
        }

        with allure.step("Send message with session ID"):
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=request_with_session
            )

        with allure.step("Verify session-based response"):
            assert response.status_code == 200
            data = response.json()
            
            allure.attach(
                str(data),
                name="Session Response",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert data["user_id"] == test_user_id
            assert isinstance(data["response"], str)
            assert len(data["response"]) > 0

    @allure.story("Error Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_chat_error_handling(self, session, api_base_url, fastapi_server):
        """Test error handling for invalid requests."""
        
        with allure.step("Test missing user_id"):
            invalid_request = {
                "message": "Test message without user_id"
            }
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=invalid_request
            )
            assert response.status_code == 422  # Validation error

        with allure.step("Test empty user_id"):
            invalid_request = {
                "user_id": "",
                "message": "Test message with empty user_id"
            }
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=invalid_request
            )
            assert response.status_code == 400
            
            error_data = response.json()
            allure.attach(
                str(error_data),
                name="Error Response",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert "error_code" in error_data["detail"]
            assert error_data["detail"]["error_code"] == "invalid_user_id"

        with allure.step("Test empty message"):
            invalid_request = {
                "user_id": "test_user",
                "message": ""
            }
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=invalid_request
            )
            assert response.status_code == 400
            
            error_data = response.json()
            assert "error_code" in error_data["detail"]
            assert error_data["detail"]["error_code"] == "invalid_message"

@allure.epic("AI Agent API")
@allure.feature("Health Endpoints")
class TestAIAgentHealthAPI:
    """Test suite for AI Agent Health API functionality."""

    @allure.story("Basic Health Check")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_basic_health_endpoint(self, session, api_base_url, fastapi_server):
        """Test basic health check endpoint."""
        
        with allure.step("Send request to basic health endpoint"):
            response = session.get(f"{api_base_url}/api/v1/health")

        with allure.step("Verify health response"):
            assert response.status_code == 200
            data = response.json()
            
            allure.attach(
                str(data),
                name="Health Response",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert "status" in data
            assert "message" in data
            assert "timestamp" in data
            assert data["status"] in ["healthy", "degraded", "unhealthy"]

    @allure.story("Detailed Health Check")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_detailed_health_endpoint(self, session, api_base_url, fastapi_server):
        """Test detailed health check endpoint."""
        
        with allure.step("Send request to detailed health endpoint"):
            response = session.get(f"{api_base_url}/api/v1/health/detailed")

        with allure.step("Verify detailed health response"):
            assert response.status_code == 200
            data = response.json()
            
            allure.attach(
                str(data),
                name="Detailed Health Response",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Validate response structure
            assert "status" in data
            assert "services" in data
            assert "timestamp" in data
            
            # Validate services structure
            services = data["services"]
            assert "mem0" in services
            assert "qdrant" in services
            assert "openai" in services
            
            # Each service should have a status
            for service_name, service_info in services.items():
                assert "status" in service_info

@allure.epic("AI Agent API")
@allure.feature("Performance")
class TestAIAgentPerformance:
    """Test suite for AI Agent API performance."""

    @allure.story("Response Time")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_chat_response_time(self, session, api_base_url, fastapi_server):
        """Test that chat responses are within acceptable time limits."""
        
        test_user_id = f"perf_test_user_{uuid.uuid4().hex[:8]}"
        request_data = {
            "user_id": test_user_id,
            "message": "Quick test message for performance testing.",
            "metadata": {"test_type": "performance"}
        }

        with allure.step("Measure chat response time"):
            start_time = time.time()
            response = session.post(
                f"{api_base_url}/api/v1/chat",
                json=request_data
            )
            end_time = time.time()
            
            response_time_seconds = end_time - start_time

        with allure.step("Verify response time is acceptable"):
            assert response.status_code == 200
            
            # Response should be within 5 seconds (generous for testing)
            assert response_time_seconds < 5.0
            
            allure.attach(
                f"{response_time_seconds:.2f} seconds",
                name="Actual Response Time",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Check if API reports response time
            data = response.json()
            if "response_time_ms" in data:
                api_reported_time = data["response_time_ms"]
                allure.attach(
                    f"{api_reported_time} ms",
                    name="API Reported Response Time",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # API reported time should be reasonable
                assert api_reported_time < 5000  # 5 seconds in milliseconds 