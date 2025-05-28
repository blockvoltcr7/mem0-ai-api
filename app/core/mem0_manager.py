#!/usr/bin/env python3
"""
Mem0 Manager

This module provides Mem0 memory system initialization and management
for the AI Agent API. Based on proven patterns from integration tests.

Author: AI Tutor Development Team
Version: 1.0
"""

import logging
from typing import Optional
from openai import OpenAI
from mem0 import Memory
from app.core.config import settings
from app.db.qdrant_client import qdrant_manager

logger = logging.getLogger(__name__)

class Mem0Manager:
    """Manages Mem0 memory system with Qdrant backend."""
    
    def __init__(self):
        self.memory: Optional[Memory] = None
        self.openai_client: Optional[OpenAI] = None
        self._initialized = False
    
    async def initialize(self) -> bool:
        """
        Initialize Mem0 memory system with Qdrant backend.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            # Validate required settings
            if not settings.openai_api_key:
                logger.error("OPENAI_API_KEY not configured")
                return False
            
            # Initialize Qdrant client first
            if not qdrant_manager.initialize():
                logger.error("Failed to initialize Qdrant client")
                return False
            
            # Ensure collection exists
            if not qdrant_manager.ensure_collection_exists(settings.mem0_collection_name):
                logger.error(f"Failed to ensure collection exists: {settings.mem0_collection_name}")
                return False
            
            # Configure Mem0 with Qdrant backend
            config = {
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": settings.ai_model,
                        "temperature": settings.ai_temperature,
                        "max_tokens": settings.ai_max_tokens
                    }
                },
                "vector_store": {
                    "provider": "qdrant",
                    "config": {
                        "collection_name": settings.mem0_collection_name,
                        "client": qdrant_manager.get_client(),
                        "embedding_model_dims": 1536,
                        "on_disk": False
                    }
                }
            }
            
            # Initialize Mem0 memory
            self.memory = Memory.from_config(config)
            
            # Initialize OpenAI client
            self.openai_client = OpenAI(api_key=settings.openai_api_key)
            
            logger.info("Mem0 memory system initialized successfully")
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Mem0 manager: {str(e)}")
            self.memory = None
            self.openai_client = None
            self._initialized = False
            return False
    
    def get_memory(self) -> Optional[Memory]:
        """
        Get the Mem0 memory instance.
        
        Returns:
            Memory instance or None if not initialized
        """
        return self.memory
    
    def get_openai_client(self) -> Optional[OpenAI]:
        """
        Get the OpenAI client instance.
        
        Returns:
            OpenAI client or None if not initialized
        """
        return self.openai_client
    
    def is_healthy(self) -> bool:
        """
        Check if Mem0 system is healthy.
        
        Returns:
            bool: True if system is healthy
        """
        if not self._initialized or not self.memory or not self.openai_client:
            return False
        
        try:
            # Test Qdrant connection through memory system
            if not qdrant_manager.is_healthy():
                return False
            
            # Test OpenAI client (simple model list call)
            models = self.openai_client.models.list()
            if not models:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Mem0 health check failed: {str(e)}")
            return False
    
    def get_status(self) -> dict:
        """
        Get detailed status of Mem0 system components.
        
        Returns:
            dict: Status information for each component
        """
        status = {
            "mem0": {"status": "initialized" if self._initialized else "not_initialized"},
            "qdrant": {
                "status": "connected" if qdrant_manager.is_healthy() else "disconnected",
                "collection": settings.mem0_collection_name
            },
            "openai": {"status": "available" if self.openai_client else "unavailable"}
        }
        
        return status

# Global Mem0 manager instance
mem0_manager = Mem0Manager() 