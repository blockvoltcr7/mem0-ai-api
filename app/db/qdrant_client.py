#!/usr/bin/env python3
"""
Qdrant Client Initialization

This module provides Qdrant client initialization and connection management
for the AI Agent Mem0 API. Based on proven patterns from integration tests.

Author: AI Tutor Development Team
Version: 1.0
"""

import logging
from typing import Optional
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.core.config import settings

logger = logging.getLogger(__name__)

class QdrantManager:
    """Manages Qdrant client connection and collection operations."""
    
    def __init__(self):
        self.client: Optional[QdrantClient] = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """
        Initialize Qdrant client connection.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if not settings.qdrant_url:
                logger.error("QDRANT_URL not configured")
                return False
            
            # Use the same pattern as the working test files
            protocol = "https" if settings.qdrant_use_https else "http"
            qdrant_url = f"{protocol}://{settings.qdrant_url}"
            
            logger.info(f"Connecting to Qdrant at: {qdrant_url}")
            
            # Create Qdrant client using the proven working pattern
            # Critical: port=None prevents :6333 from being appended to URL
            self.client = QdrantClient(
                url=qdrant_url,
                port=None,  # Critical: prevents :6333 from being appended to URL
                timeout=30,
                prefer_grpc=False  # Force REST API usage
            )
            
            # Test connection
            collections = self.client.get_collections()
            logger.info(f"Connected to Qdrant: {len(collections.collections)} collections available")
            
            self._initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client: {str(e)}")
            self.client = None
            self._initialized = False
            return False
    
    def ensure_collection_exists(self, collection_name: str) -> bool:
        """
        Ensure the specified collection exists, create if it doesn't.
        
        Args:
            collection_name: Name of the collection to ensure exists
            
        Returns:
            bool: True if collection exists or was created successfully
        """
        if not self.client:
            logger.error("Qdrant client not initialized")
            return False
        
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_names = [c.name for c in collections.collections]
            
            if collection_name not in collection_names:
                # Create collection with proper configuration for OpenAI embeddings
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=1536,  # OpenAI embedding dimension
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {collection_name}")
            else:
                logger.info(f"Collection already exists: {collection_name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to ensure collection exists: {str(e)}")
            return False
    
    def get_client(self) -> Optional[QdrantClient]:
        """
        Get the Qdrant client instance.
        
        Returns:
            QdrantClient or None if not initialized
        """
        return self.client
    
    def is_healthy(self) -> bool:
        """
        Check if Qdrant connection is healthy.
        
        Returns:
            bool: True if connection is healthy
        """
        if not self.client or not self._initialized:
            return False
        
        try:
            # Simple health check
            self.client.get_collections()
            return True
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return False

# Global Qdrant manager instance
qdrant_manager = QdrantManager() 