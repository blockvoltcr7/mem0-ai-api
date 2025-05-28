"""
Core Integration Tests

Essential tests for the AI Agent Mem0 API with Qdrant vector database integration.
This file contains only the most critical tests for core functionality.

Author: AI Tutor Development Team
Version: 1.0
"""

import pytest
import allure
import httpx
import asyncio
import uuid
from typing import Dict, Any

@allure.epic("Qdrant Integration")
@allure.feature("Core Functionality")
class TestCoreIntegration:
    """Essential test suite for core API functionality."""

    @allure.story("Health Check")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.health
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_health_check(self, test_client: httpx.AsyncClient, allure_environment_setup):
        """
        Test basic health check endpoint.
        
        Verifies that the API is running and responding correctly.
        """
        with allure.step("Send GET request to /health endpoint"):
            response = await test_client.get("/health")
            
            allure.attach(
                f"GET /health",
                name="Request",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify response status and content"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            allure.attach(
                str(data),
                name="Response Data",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert "status" in data, "Response missing 'status' field"
            assert "message" in data, "Response missing 'message' field"
            assert data["status"] == "healthy", f"Expected 'healthy', got '{data['status']}'"

    @allure.story("Basic Chat")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.chat
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_basic_chat(self, test_client: httpx.AsyncClient, chat_request_factory, allure_environment_setup):
        """
        Test basic chat functionality.
        
        Verifies that the chat endpoint accepts requests and returns
        properly formatted responses with AI-generated content.
        """
        user_id = f"basic_chat_{uuid.uuid4().hex[:8]}"
        
        with allure.step("Prepare and send chat request"):
            chat_request = chat_request_factory(
                user_id=user_id,
                message="Hello! Can you tell me about peptides?",
                metadata={"domain": "peptide_coaching", "test_type": "basic_functionality"}
            )
            
            allure.attach(
                str(chat_request),
                name="Chat Request",
                attachment_type=allure.attachment_type.JSON
            )
            
            response = await test_client.post("/api/v1/chat", json=chat_request)
        
        with allure.step("Verify response structure and content"):
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            
            data = response.json()
            allure.attach(
                str(data),
                name="Chat Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Validate required fields
            required_fields = ["response", "memories_found", "memories_created", "user_id"]
            for field in required_fields:
                assert field in data, f"Response missing required field: {field}"
            
            assert isinstance(data["response"], str), "Response should be a string"
            assert len(data["response"]) > 0, "Response should not be empty"
            assert data["user_id"] == user_id, f"User ID mismatch"
            assert data["memories_found"] == 0, "First conversation should find no memories"
            assert data["memories_created"] >= 1, "Should create at least one memory"

    @allure.story("Memory Persistence")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.memory
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_memory_persistence(self, test_client: httpx.AsyncClient, chat_request_factory, allure_environment_setup):
        """
        Test memory persistence across conversations.
        
        Verifies that the system remembers previous conversations
        and provides context-aware responses.
        """
        user_id = f"memory_test_{uuid.uuid4().hex[:8]}"
        
        with allure.step("First conversation - Establish context"):
            first_request = chat_request_factory(
                user_id=user_id,
                message="I'm interested in BPC-157 for recovery. What are the benefits?",
                metadata={"domain": "peptide_coaching", "context": "recovery_consultation"}
            )
            
            first_response = await test_client.post("/api/v1/chat", json=first_request)
            assert first_response.status_code == 200, "First conversation should succeed"
            
            first_data = first_response.json()
            allure.attach(
                str(first_data),
                name="First Chat Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert first_data["memories_found"] == 0, "First conversation should find no memories"
            assert first_data["memories_created"] >= 1, "First conversation should create memory"
        
        # Wait for memory to be stored
        await asyncio.sleep(2)
        
        with allure.step("Second conversation - Test memory retrieval"):
            second_request = chat_request_factory(
                user_id=user_id,
                message="What about dosage recommendations for what we discussed?",
                metadata={"domain": "peptide_coaching", "context": "dosage_consultation"}
            )
            
            second_response = await test_client.post("/api/v1/chat", json=second_request)
            assert second_response.status_code == 200, "Second conversation should succeed"
            
            second_data = second_response.json()
            allure.attach(
                str(second_data),
                name="Second Chat Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Verify memory retrieval and context awareness"):
            # Second conversation should find previous memories
            assert second_data["memories_found"] >= 1, f"Expected at least 1 memory found, got {second_data['memories_found']}"
            
            # Response should reference previous context
            second_response_text = second_data["response"].lower()
            context_keywords = ["bpc-157", "bpc", "recovery", "dosage", "discussed", "mentioned"]
            found_context = [keyword for keyword in context_keywords if keyword in second_response_text]
            
            allure.attach(
                f"Found context keywords: {found_context}",
                name="Context Analysis",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert len(found_context) > 0, f"Response should reference previous context. Response: {second_data['response']}"

    @allure.story("User Isolation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.memory
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_user_isolation(self, test_client: httpx.AsyncClient, chat_request_factory, allure_environment_setup):
        """
        Test user memory isolation.
        
        Verifies that different users have completely isolated
        memory spaces and cannot access each other's conversations.
        """
        user1_id = f"isolation_user1_{uuid.uuid4().hex[:8]}"
        user2_id = f"isolation_user2_{uuid.uuid4().hex[:8]}"
        
        with allure.step("User 1 - Create conversation about TB-500"):
            user1_request = chat_request_factory(
                user_id=user1_id,
                message="Tell me about TB-500 peptide for healing.",
                metadata={"domain": "peptide_coaching", "peptide": "TB-500"}
            )
            
            user1_response = await test_client.post("/api/v1/chat", json=user1_request)
            assert user1_response.status_code == 200, "User 1 conversation should succeed"
            
            user1_data = user1_response.json()
            allure.attach(
                str(user1_data),
                name="User 1 Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert user1_data["memories_found"] == 0, "User 1 should have no previous memories"
            assert user1_data["memories_created"] >= 1, "User 1 should create memory"
        
        with allure.step("User 2 - Create conversation about different topic"):
            user2_request = chat_request_factory(
                user_id=user2_id,
                message="I want to know about Ipamorelin for growth hormone.",
                metadata={"domain": "peptide_coaching", "peptide": "Ipamorelin"}
            )
            
            user2_response = await test_client.post("/api/v1/chat", json=user2_request)
            assert user2_response.status_code == 200, "User 2 conversation should succeed"
            
            user2_data = user2_response.json()
            allure.attach(
                str(user2_data),
                name="User 2 Response",
                attachment_type=allure.attachment_type.JSON
            )
            
            assert user2_data["memories_found"] == 0, "User 2 should have no previous memories"
            assert user2_data["memories_created"] >= 1, "User 2 should create memory"
        
        # Wait for memories to be stored
        await asyncio.sleep(2)
        
        with allure.step("User 1 - Follow-up conversation to test isolation"):
            user1_followup = chat_request_factory(
                user_id=user1_id,
                message="What's the recommended dosage for the healing peptide we discussed?",
                metadata={"domain": "peptide_coaching"}
            )
            
            user1_followup_response = await test_client.post("/api/v1/chat", json=user1_followup)
            assert user1_followup_response.status_code == 200, "User 1 follow-up should succeed"
            
            user1_followup_data = user1_followup_response.json()
            allure.attach(
                str(user1_followup_data),
                name="User 1 Follow-up Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Verify user isolation"):
            # User 1 should find their own memories
            assert user1_followup_data["memories_found"] >= 1, "User 1 should find their own memories"
            
            # User 1's response should reference TB-500, not Ipamorelin
            user1_response_text = user1_followup_data["response"].lower()
            
            # Should contain TB-500 related content
            tb500_keywords = ["tb-500", "tb500", "healing"]
            found_tb500 = [kw for kw in tb500_keywords if kw in user1_response_text]
            
            # Should NOT contain Ipamorelin content
            ipamorelin_in_response = "ipamorelin" in user1_response_text
            
            allure.attach(
                f"User 1 memories found: {user1_followup_data['memories_found']}\n"
                f"TB-500 keywords found: {found_tb500}\n"
                f"Contains Ipamorelin: {ipamorelin_in_response}",
                name="User Isolation Verification",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert len(found_tb500) > 0, f"User 1 should reference TB-500 context: {found_tb500}"
            assert not ipamorelin_in_response, f"User 1 should not access User 2's Ipamorelin conversation" 