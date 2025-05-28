#!/usr/bin/env python3
"""
AI Agent Service

Core AI agent logic ported from the CLI implementation.
Handles memory search, context building, and AI response generation.

Author: AI Tutor Development Team
Version: 1.0
"""

import logging
import time
from typing import Dict, List, Optional, Any
from app.core.mem0_manager import mem0_manager
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIAgentService:
    """Core AI agent service for generating contextual responses using Mem0."""
    
    def __init__(self):
        self.mem0_manager = mem0_manager
    
    async def generate_response(
        self, 
        user_message: str, 
        user_id: str, 
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response using Mem0 memory context.
        Based on the CLI's generate_ai_response function.
        
        Args:
            user_message: User's input message
            user_id: Unique user identifier
            session_id: Optional session identifier
            metadata: Optional metadata for memory storage
            
        Returns:
            Dict containing response and metadata
        """
        start_time = time.time()
        
        try:
            # Get memory and OpenAI client
            memory = self.mem0_manager.get_memory()
            openai_client = self.mem0_manager.get_openai_client()
            
            if not memory or not openai_client:
                raise Exception("Mem0 system not properly initialized")
            
            # Search for relevant memories
            logger.info(f"Searching for relevant memories for user: {user_id}")
            relevant_memories = memory.search(
                query=user_message,
                user_id=user_id,
                limit=settings.memory_search_limit
            )
            
            memories_list = relevant_memories.get("results", [])
            memories_str = "\n".join(f"- {entry['memory']}" for entry in memories_list)
            
            logger.info(f"Found {len(memories_list)} relevant memories for user: {user_id}")
            
            # Construct system prompt with memory context
            system_prompt = self._build_system_prompt(memories_str)
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
            
            # Generate AI response
            logger.info(f"Generating AI response for user: {user_id}")
            response = openai_client.chat.completions.create(
                model=settings.ai_model,
                messages=messages,
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens
            )
            
            assistant_response = response.choices[0].message.content
            
            # Store conversation in memory
            conversation_messages = messages + [{"role": "assistant", "content": assistant_response}]
            
            # Prepare metadata for memory storage
            memory_metadata = metadata or {}
            if session_id:
                memory_metadata["session_id"] = session_id
            
            memory.add(conversation_messages, user_id=user_id, metadata=memory_metadata)
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            logger.info(f"Successfully generated response for user: {user_id} in {response_time_ms}ms")
            
            return {
                "response": assistant_response,
                "memories_found": len(memories_list),
                "memories_created": 1,  # We always create one from the conversation
                "user_id": user_id,
                "response_time_ms": response_time_ms
            }
            
        except Exception as e:
            logger.error(f"Failed to generate AI response for user {user_id}: {str(e)}")
            raise
    
    def _build_system_prompt(self, memories_str: str) -> str:
        """
        Build system prompt with memory context.
        Based on the CLI implementation.
        
        Args:
            memories_str: Formatted string of relevant memories
            
        Returns:
            System prompt string
        """
        base_prompt = (
            "You are a knowledgeable AI health coach specializing in peptide therapy. "
            "You provide evidence-based information while emphasizing that peptides like BPC-157 "
            "are not FDA-approved for human use and should only be used under medical supervision. "
            "Use the provided conversation history to give personalized responses."
        )
        
        if memories_str:
            return f"{base_prompt}\n\nRelevant conversation history:\n{memories_str}"
        else:
            return base_prompt
    
    def check_user_exists(self, user_id: str) -> bool:
        """
        Check if user has existing memories in the system.
        
        Args:
            user_id: User identifier to check
            
        Returns:
            bool: True if user has existing memories
        """
        try:
            memory = self.mem0_manager.get_memory()
            if not memory:
                return False
            
            # Search for any memories for this user
            results = memory.search(query="", user_id=user_id, limit=1)
            return len(results.get("results", [])) > 0
            
        except Exception as e:
            logger.error(f"Error checking if user exists: {str(e)}")
            return False
    
    def get_user_memory_count(self, user_id: str) -> int:
        """
        Get the number of memories stored for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            int: Number of memories for the user
        """
        try:
            memory = self.mem0_manager.get_memory()
            if not memory:
                return 0
            
            # Search for all memories for this user
            results = memory.search(query="", user_id=user_id, limit=100)
            return len(results.get("results", []))
            
        except Exception as e:
            logger.error(f"Error getting user memory count: {str(e)}")
            return 0

# Global AI agent service instance
ai_agent_service = AIAgentService() 