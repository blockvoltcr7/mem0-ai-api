#!/usr/bin/env python3
"""
Chat Models

Pydantic models for the AI Agent Chat API.
Defines request and response schemas for chat endpoints.

Author: AI Tutor Development Team
Version: 1.0
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Contains all necessary information for a chat interaction including
    user identification, message content, and optional context metadata.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "user_id": "user123",
                    "message": "I'm interested in learning about BPC-157 peptide for healing.",
                    "session_id": "peptide_consultation_2024",
                    "metadata": {
                        "domain": "peptide_coaching",
                        "location": "SF",
                        "urgency": "normal"
                    }
                },
                {
                    "user_id": "athlete_456",
                    "message": "What are the benefits of TB-500 for recovery?",
                    "metadata": {
                        "domain": "sports_medicine",
                        "athlete_type": "endurance"
                    }
                }
            ]
        }
    )
    
    user_id: str = Field(
        ..., 
        description="Unique user identifier for memory persistence. Must be consistent across conversations.",
        min_length=1, 
        max_length=100,
        examples=["user123", "athlete_456", "client_789"]
    )
    
    message: str = Field(
        ..., 
        description="User's message or question to the AI agent. Can be conversational or specific queries.",
        min_length=1, 
        max_length=5000,
        examples=[
            "Tell me about BPC-157 peptide benefits",
            "What's the recommended dosage for TB-500?",
            "I'm experiencing joint pain, what peptides might help?"
        ]
    )
    
    session_id: Optional[str] = Field(
        None, 
        description="Optional session identifier for grouping related conversations. Useful for organizing consultations or topics.",
        max_length=100,
        examples=["consultation_2024", "recovery_protocol", "initial_assessment"]
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        None, 
        description="Optional metadata for enhanced context and memory filtering. Can include domain, preferences, or session context.",
        examples=[
            {"domain": "peptide_coaching", "experience_level": "beginner"},
            {"context": "post_workout", "goals": ["recovery", "muscle_growth"]},
            {"medical_history": "previous_injuries", "current_medications": "none"}
        ]
    )

class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Contains the AI's response along with memory statistics and metadata
    about the conversation processing.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "response": "BPC-157 is a peptide that has shown promising results for healing and tissue repair. However, it's important to note that it's not FDA-approved for human use and should only be considered under medical supervision. What specific aspect of BPC-157 are you most interested in learning about?",
                    "memories_found": 2,
                    "memories_created": 1,
                    "user_id": "user123",
                    "response_time_ms": 1250,
                    "metadata": {
                        "model_used": "gpt-4",
                        "memory_retrieval_time_ms": 45,
                        "context_tokens": 1200
                    }
                }
            ]
        }
    )
    
    response: str = Field(
        ..., 
        description="AI assistant's response to the user's message, incorporating relevant memory context.",
        examples=[
            "Based on our previous discussion about your recovery goals, BPC-157 could be beneficial for tissue repair...",
            "I remember you mentioned joint pain earlier. Here are some peptide options that might help..."
        ]
    )
    
    memories_found: int = Field(
        ..., 
        description="Number of relevant memories retrieved from the user's conversation history.",
        ge=0,
        examples=[0, 2, 5]
    )
    
    memories_created: int = Field(
        ..., 
        description="Number of new memories created and stored from this conversation.",
        ge=0,
        examples=[0, 1, 2]
    )
    
    user_id: str = Field(
        ..., 
        description="User identifier that was used for this conversation.",
        examples=["user123", "athlete_456"]
    )
    
    session_id: Optional[str] = Field(
        None,
        description="Session identifier if provided in the request.",
        examples=["consultation_2024", "recovery_protocol"]
    )
    
    metadata: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional metadata about the response processing, including performance metrics.",
        examples=[
            {
                "model_used": "gpt-4",
                "response_time_ms": 1250,
                "memory_retrieval_time_ms": 45,
                "context_tokens": 1200,
                "memory_relevance_score": 0.85
            }
        ]
    )

class HealthStatus(BaseModel):
    """
    Health status model for system monitoring.
    
    Provides comprehensive status information about all system components
    including Mem0, Qdrant, and OpenAI services.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "healthy",
                    "services": {
                        "mem0": {
                            "status": "initialized",
                            "collection_name": "peptide_health_coaching_memories",
                            "memory_count": 42
                        },
                        "qdrant": {
                            "status": "connected",
                            "collections": 11,
                            "url": "https://example.qdrant.tech"
                        },
                        "openai": {
                            "status": "available",
                            "models": 75,
                            "default_model": "gpt-4"
                        }
                    },
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            ]
        }
    )
    
    status: str = Field(
        ..., 
        description="Overall system health status. Can be 'healthy', 'degraded', or 'unhealthy'.",
        examples=["healthy", "degraded", "unhealthy"]
    )
    
    services: Dict[str, Dict[str, Any]] = Field(
        ..., 
        description="Detailed status information for each system component (Mem0, Qdrant, OpenAI).",
        examples=[
            {
                "mem0": {"status": "initialized", "collection_name": "peptide_health_coaching_memories"},
                "qdrant": {"status": "connected", "collections": 11},
                "openai": {"status": "available", "models": 75}
            }
        ]
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, 
        description="UTC timestamp when the health check was performed.",
        examples=["2024-01-15T10:30:00Z", "2024-01-15T14:45:30Z"]
    ) 