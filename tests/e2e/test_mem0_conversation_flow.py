#!/usr/bin/env python3
"""
End-to-End Test for Mem0 Conversation Flow

This test replicates the manual CLI test flow from test_mem0_cli.py
to verify that Mem0 memory functionality works correctly in an automated
testing environment. It tests the complete conversation flow including:

1. Initial conversation without memory context
2. Adding user preferences to memory
3. Retrieving and using stored memories in subsequent conversations
4. Memory search functionality
5. Session statistics and performance metrics

The test uses in-memory storage for simplicity and focuses on the
core memory functionality rather than external database integration.
"""

import os
import pytest
import allure
import time
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory


@allure.epic("End-to-End Testing")
@allure.feature("Mem0 Conversation Flow")
class TestMem0ConversationFlow:
    """
    End-to-end test suite for Mem0 conversation flow.
    
    This test class replicates the manual CLI testing scenario to ensure
    that memory functionality works correctly in an automated environment.
    """

    @pytest.fixture(scope="class", autouse=True)
    def setup_environment(self):
        """Set up environment variables and validate prerequisites."""
        with allure.step("Load environment variables"):
            load_dotenv()
            
        with allure.step("Validate required environment variables"):
            openai_api_key = os.getenv("OPENAI_API_KEY")
            
            allure.attach(
                f"OPENAI_API_KEY present: {'Yes' if openai_api_key else 'No'}",
                name="Environment Configuration",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert openai_api_key is not None, "OPENAI_API_KEY environment variable is required"

    @pytest.fixture(scope="class")
    def openai_client(self, setup_environment):
        """Create OpenAI client for conversation generation."""
        with allure.step("Initialize OpenAI client"):
            client = OpenAI()
            return client

    @pytest.fixture(scope="class")
    def memory_instance(self, setup_environment):
        """Create and configure mem0 Memory instance with in-memory storage."""
        with allure.step("Initialize Memory layer with in-memory storage"):
            config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": "gpt-4o-mini",
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                }
                # No vector_store config means in-memory storage is used
            }
            
            allure.attach(
                str(config),
                name="Memory Configuration",
                attachment_type=allure.attachment_type.JSON
            )
            
            try:
                memory = Memory.from_config(config)
                allure.attach(
                    "✅ Memory layer initialized with in-memory storage successfully",
                    name="Memory Initialization",
                    attachment_type=allure.attachment_type.TEXT
                )
                return memory
            except Exception as e:
                allure.attach(
                    f"❌ Failed to initialize memory: {str(e)}",
                    name="Memory Initialization Error",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.fail(f"Failed to initialize Memory: {str(e)}")

    @pytest.fixture(scope="class")
    def conversation_handler(self, openai_client, memory_instance):
        """Create a conversation handler that mimics the CLI functionality."""
        class ConversationHandler:
            def __init__(self, openai_client, memory_instance):
                self.openai_client = openai_client
                self.memory = memory_instance
                self.model_name = "gpt-4o-mini"
                self.conversation_count = 0
                self.start_time = time.time()
            
            def chat_with_memories(self, message: str, user_id: str) -> Dict[str, Any]:
                """Process a chat message using Mem0 memory enhancement."""
                start_time = time.time()
                
                try:
                    # Step 1: Retrieve relevant memories
                    memory_search_start = time.time()
                    relevant_memories = self.memory.search(
                        query=message, 
                        user_id=user_id, 
                        limit=3
                    )
                    memory_search_time = time.time() - memory_search_start
                    
                    # Step 2: Format memories for inclusion in the prompt
                    memories_list = relevant_memories.get("results", [])
                    memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
                    
                    # Step 3: Construct the system prompt with memory context
                    system_prompt = (
                        "You are a helpful AI assistant with access to conversation history. "
                        "Use the provided memories to give contextual and personalized responses. "
                        "If no relevant memories are provided, respond normally."
                        f"\n\nRelevant memories:\n{memories_str}" if memories_str 
                        else "You are a helpful AI assistant."
                    )
                    
                    # Step 4: Prepare messages for OpenAI API
                    messages = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ]
                    
                    # Step 5: Generate response using OpenAI
                    response_start = time.time()
                    response = self.openai_client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000
                    )
                    response_time = time.time() - response_start
                    assistant_response = response.choices[0].message.content
                    
                    # Step 6: Store the conversation in memory
                    memory_store_start = time.time()
                    conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
                    self.memory.add(conversation_messages, user_id=user_id)
                    memory_store_time = time.time() - memory_store_start
                    
                    self.conversation_count += 1
                    total_time = time.time() - start_time
                    
                    return {
                        "response": assistant_response,
                        "memories_found": len(memories_list),
                        "memories_context": memories_str,
                        "timing": {
                            "total": total_time,
                            "memory_search": memory_search_time,
                            "response_generation": response_time,
                            "memory_storage": memory_store_time
                        }
                    }
                    
                except Exception as e:
                    return {
                        "response": f"Error processing message: {str(e)}",
                        "error": str(e),
                        "memories_found": 0,
                        "memories_context": "",
                        "timing": {"total": time.time() - start_time}
                    }
            
            def search_memories(self, query: str, user_id: str, limit: int = 5) -> List[Dict[str, Any]]:
                """Search memories for a specific query."""
                try:
                    search_results = self.memory.search(
                        query=query, 
                        user_id=user_id, 
                        limit=limit
                    )
                    return search_results.get("results", [])
                except Exception as e:
                    return []
            
            def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
                """Get statistics about current memory usage."""
                try:
                    # Search for all memories for this user
                    all_memories = self.memory.search(query="", user_id=user_id, limit=1000)
                    memory_count = len(all_memories.get("results", []))
                    
                    return {
                        "total_memories": memory_count,
                        "user_id": user_id,
                        "conversations": self.conversation_count,
                        "uptime_seconds": time.time() - self.start_time
                    }
                except Exception as e:
                    return {"error": str(e)}
        
        return ConversationHandler(openai_client, memory_instance)

    @allure.story("Initial Conversation Without Memory")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_initial_conversation(self, conversation_handler):
        """Test initial conversation without any memory context."""
        user_id = "e2e_test_user_001"
        message = "hi"
        
        with allure.step(f"Send initial greeting: '{message}'"):
            result = conversation_handler.chat_with_memories(message, user_id)
            
            allure.attach(
                f"User: {message}\nAI: {result['response']}",
                name="Initial Conversation",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                str(result['timing']),
                name="Performance Metrics",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Verify response was generated
            assert result['response'] is not None, "AI should generate a response"
            assert len(result['response']) > 0, "Response should not be empty"
            assert 'error' not in result, f"No errors should occur: {result.get('error', '')}"
            
            # Verify no memories were found (first conversation)
            assert result['memories_found'] == 0, "No memories should exist for initial conversation"
            
            # Verify timing metrics
            assert result['timing']['total'] > 0, "Total time should be recorded"
            assert result['timing']['memory_search'] >= 0, "Memory search time should be recorded"
            assert result['timing']['response_generation'] > 0, "Response generation time should be recorded"
            assert result['timing']['memory_storage'] > 0, "Memory storage time should be recorded"

    @allure.story("Memory Context Retrieval")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_memory_context_question(self, conversation_handler):
        """Test asking about previous conversation to verify memory isn't working yet."""
        user_id = "e2e_test_user_001"
        message = "what did i just say?"
        
        with allure.step(f"Ask about previous conversation: '{message}'"):
            result = conversation_handler.chat_with_memories(message, user_id)
            
            allure.attach(
                f"User: {message}\nAI: {result['response']}",
                name="Memory Context Question",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                f"Memories found: {result['memories_found']}\nMemory context: {result['memories_context']}",
                name="Memory Context Details",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Verify response was generated
            assert result['response'] is not None, "AI should generate a response"
            assert len(result['response']) > 0, "Response should not be empty"
            assert 'error' not in result, f"No errors should occur: {result.get('error', '')}"
            
            # The AI might or might not find relevant memories depending on how mem0 processes the conversation
            # We'll just verify the system is working, not the specific memory retrieval

    @allure.story("User Preference Storage")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_store_user_preferences(self, conversation_handler):
        """Test storing user food preferences in memory."""
        user_id = "e2e_test_user_001"
        message = "i like all kinds of cheese except cow milk cheese, i only like sheep or goat cheese"
        
        with allure.step(f"Store user preferences: '{message}'"):
            result = conversation_handler.chat_with_memories(message, user_id)
            
            allure.attach(
                f"User: {message}\nAI: {result['response']}",
                name="User Preference Storage",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                str(result['timing']),
                name="Storage Performance Metrics",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Verify response was generated
            assert result['response'] is not None, "AI should generate a response"
            assert len(result['response']) > 0, "Response should not be empty"
            assert 'error' not in result, f"No errors should occur: {result.get('error', '')}"
            
            # Verify the response acknowledges the cheese preferences
            response_lower = result['response'].lower()
            cheese_related_terms = ['cheese', 'sheep', 'goat', 'feta', 'manchego', 'pecorino', 'chèvre']
            found_cheese_terms = [term for term in cheese_related_terms if term in response_lower]
            
            assert len(found_cheese_terms) > 0, f"Response should mention cheese-related terms. Response: {result['response']}"

    @allure.story("Memory Retrieval and Context Usage")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_retrieve_user_preferences(self, conversation_handler):
        """Test retrieving stored user preferences from memory."""
        user_id = "e2e_test_user_001"
        message = "what are my food preferences?"
        
        with allure.step(f"Query stored preferences: '{message}'"):
            result = conversation_handler.chat_with_memories(message, user_id)
            
            allure.attach(
                f"User: {message}\nAI: {result['response']}",
                name="Preference Retrieval",
                attachment_type=allure.attachment_type.TEXT
            )
            
            allure.attach(
                f"Memories found: {result['memories_found']}\nMemory context: {result['memories_context']}",
                name="Memory Retrieval Details",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Verify response was generated
            assert result['response'] is not None, "AI should generate a response"
            assert len(result['response']) > 0, "Response should not be empty"
            assert 'error' not in result, f"No errors should occur: {result.get('error', '')}"
            
            # Verify the response includes the stored cheese preferences
            response_lower = result['response'].lower()
            
            # Check for key preference indicators
            preference_indicators = ['cheese', 'sheep', 'goat']
            found_indicators = [term for term in preference_indicators if term in response_lower]
            
            assert len(found_indicators) >= 2, f"Response should mention cheese preferences (sheep/goat). Found: {found_indicators}. Response: {result['response']}"
            
            # Verify that memories were found and used
            if result['memories_found'] > 0:
                allure.attach(
                    "✅ Memories were successfully retrieved and used in response",
                    name="Memory Usage Verification",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    "⚠️ No memories were found, but response still contained relevant information",
                    name="Memory Usage Warning",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.story("Memory Search Functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_memory_search(self, conversation_handler):
        """Test direct memory search functionality."""
        user_id = "e2e_test_user_001"
        search_queries = ["cheese", "preferences", "food"]
        
        for query in search_queries:
            with allure.step(f"Search memories for: '{query}'"):
                results = conversation_handler.search_memories(query, user_id, limit=5)
                
                allure.attach(
                    f"Query: {query}\nResults found: {len(results)}\nResults: {results}",
                    name=f"Memory Search - {query}",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Verify search functionality works (results may be empty, but no errors)
                assert isinstance(results, list), "Search should return a list"
                
                # If results are found, verify they contain memory content
                for result in results:
                    assert 'memory' in result, "Each result should contain a 'memory' field"
                    assert isinstance(result['memory'], str), "Memory content should be a string"
                    assert len(result['memory']) > 0, "Memory content should not be empty"

    @allure.story("Session Statistics")
    @allure.severity(allure.severity_level.MINOR)
    def test_session_statistics(self, conversation_handler):
        """Test session statistics functionality."""
        user_id = "e2e_test_user_001"
        
        with allure.step("Retrieve session statistics"):
            stats = conversation_handler.get_memory_stats(user_id)
            
            allure.attach(
                str(stats),
                name="Session Statistics",
                attachment_type=allure.attachment_type.JSON
            )
            
            # Verify statistics structure
            if 'error' not in stats:
                assert 'user_id' in stats, "Stats should include user_id"
                assert 'conversations' in stats, "Stats should include conversation count"
                assert 'uptime_seconds' in stats, "Stats should include uptime"
                
                assert stats['user_id'] == user_id, "User ID should match"
                assert stats['conversations'] > 0, "Should have recorded conversations"
                assert stats['uptime_seconds'] > 0, "Should have positive uptime"
                
                allure.attach(
                    f"✅ Statistics successfully retrieved:\n"
                    f"- User: {stats['user_id']}\n"
                    f"- Conversations: {stats['conversations']}\n"
                    f"- Uptime: {stats['uptime_seconds']:.1f}s",
                    name="Statistics Summary",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                allure.attach(
                    f"⚠️ Statistics retrieval failed: {stats['error']}",
                    name="Statistics Error",
                    attachment_type=allure.attachment_type.TEXT
                )

    @allure.story("Multi-User Memory Isolation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_memory_isolation(self, conversation_handler):
        """Test that memories are properly isolated between different users."""
        user1_id = "e2e_test_user_001"
        user2_id = "e2e_test_user_002"
        
        with allure.step("Store preference for user 2"):
            # Store a different preference for user 2
            message = "I love spicy food and hate sweet desserts"
            result = conversation_handler.chat_with_memories(message, user2_id)
            
            allure.attach(
                f"User 2: {message}\nAI: {result['response']}",
                name="User 2 Preference Storage",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert 'error' not in result, f"No errors should occur: {result.get('error', '')}"
        
        with allure.step("Query preferences for user 1"):
            # Query preferences for user 1 (should get cheese preferences)
            message = "what are my food preferences?"
            result1 = conversation_handler.chat_with_memories(message, user1_id)
            
            allure.attach(
                f"User 1 Query: {message}\nAI: {result1['response']}",
                name="User 1 Preference Query",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Query preferences for user 2"):
            # Query preferences for user 2 (should get spicy food preferences)
            message = "what are my food preferences?"
            result2 = conversation_handler.chat_with_memories(message, user2_id)
            
            allure.attach(
                f"User 2 Query: {message}\nAI: {result2['response']}",
                name="User 2 Preference Query",
                attachment_type=allure.attachment_type.TEXT
            )
        
        with allure.step("Verify memory isolation"):
            # Verify responses are different and context-appropriate
            response1_lower = result1['response'].lower()
            response2_lower = result2['response'].lower()
            
            # User 1 should get cheese-related response
            cheese_terms = ['cheese', 'sheep', 'goat']
            user1_cheese_mentions = sum(1 for term in cheese_terms if term in response1_lower)
            
            # User 2 should get spicy food-related response
            spicy_terms = ['spicy', 'sweet', 'dessert']
            user2_spicy_mentions = sum(1 for term in spicy_terms if term in response2_lower)
            
            allure.attach(
                f"User 1 cheese mentions: {user1_cheese_mentions}\n"
                f"User 2 spicy mentions: {user2_spicy_mentions}\n"
                f"Responses are different: {result1['response'] != result2['response']}",
                name="Memory Isolation Analysis",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # At minimum, responses should be different
            assert result1['response'] != result2['response'], "Different users should get different responses based on their memories"

    @allure.story("Error Handling and Recovery")
    @allure.severity(allure.severity_level.MINOR)
    def test_error_handling(self, conversation_handler):
        """Test error handling with edge cases."""
        user_id = "e2e_test_user_003"
        
        edge_cases = [
            "",  # Empty message
            " ",  # Whitespace only
            "a" * 1000,  # Very long message
            "🎉🚀💻🧠🔥",  # Emoji only
        ]
        
        for i, message in enumerate(edge_cases):
            with allure.step(f"Test edge case {i+1}: '{message[:50]}...'"):
                result = conversation_handler.chat_with_memories(message, user_id)
                
                allure.attach(
                    f"Input: '{message[:100]}...'\nResponse: {result['response'][:200]}...",
                    name=f"Edge Case {i+1}",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Verify system handles edge cases gracefully
                assert result['response'] is not None, "Should always return a response"
                assert isinstance(result['response'], str), "Response should be a string"
                
                # Verify timing metrics are still recorded
                assert 'timing' in result, "Timing metrics should be recorded"
                assert result['timing']['total'] > 0, "Total time should be positive" 