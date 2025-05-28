#!/usr/bin/env python3
"""
Chat Endpoint

Main chat endpoint for the AI Agent API.
Provides a single endpoint for conversational AI with persistent memory.

Author: AI Tutor Development Team
Version: 1.0
"""

import logging
from fastapi import APIRouter, HTTPException, status
from app.models.chat_models import ChatRequest, ChatResponse
from app.services.ai_agent_service import ai_agent_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])

@router.post(
    "/chat", 
    response_model=ChatResponse, 
    summary="Chat with AI Agent",
    description="""
    **Chat with the AI agent using persistent memory.**
    
    This endpoint provides conversational AI capabilities with:
    - 🧠 **Persistent memory** across conversations
    - 🔍 **Context-aware responses** based on user history  
    - 👤 **Automatic user creation** if not exists
    - 📝 **Session-based memory grouping** (optional)
    - 🏷️ **Metadata support** for enhanced context
    
    ### Example Request:
    ```json
    {
      "user_id": "user123",
      "message": "Tell me about BPC-157 peptide benefits",
      "session_id": "consultation_2024",
      "metadata": {
        "domain": "peptide_coaching",
        "context": "health_consultation"
      }
    }
    ```
    
    ### Response includes:
    - AI-generated response text
    - Memory statistics (memories found/created)
    - Processing metadata
    """,
    responses={
        200: {
            "description": "Successful chat response",
            "content": {
                "application/json": {
                    "example": {
                        "response": "BPC-157 is a synthetic peptide derived from body protection compound...",
                        "user_id": "user123",
                        "session_id": "consultation_2024",
                        "memories_found": 2,
                        "memories_created": 1,
                        "metadata": {
                            "model_used": "gpt-4",
                            "response_time_ms": 1250,
                            "memory_retrieval_time_ms": 45
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request - invalid input",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "error_code": "invalid_user_id",
                            "message": "user_id is required and cannot be empty",
                            "suggestions": ["Provide a valid user_id in the request"]
                        }
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "error_code": "internal_error",
                            "message": "An unexpected error occurred while processing your request",
                            "suggestions": [
                                "Try again in a few moments",
                                "Check if all required services are running",
                                "Contact support if the problem persists"
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with the AI agent using persistent memory.
    
    This endpoint provides conversational AI capabilities with:
    - Persistent memory across conversations
    - Context-aware responses based on user history
    - Automatic user creation if not exists
    - Session-based memory grouping (optional)
    
    Args:
        request: Chat request containing user message and metadata
        
    Returns:
        ChatResponse: AI response with memory statistics
        
    Raises:
        HTTPException: If the request fails or system is unavailable
    """
    try:
        logger.info(f"Processing chat request for user: {request.user_id}")
        
        # Validate that the user_id is provided and not empty
        if not request.user_id or not request.user_id.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_code": "invalid_user_id",
                    "message": "user_id is required and cannot be empty",
                    "suggestions": ["Provide a valid user_id in the request"]
                }
            )
        
        # Validate that the message is provided and not empty
        if not request.message or not request.message.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "error_code": "invalid_message",
                    "message": "message is required and cannot be empty",
                    "suggestions": ["Provide a valid message in the request"]
                }
            )
        
        # Check if user exists (for logging purposes)
        user_exists = ai_agent_service.check_user_exists(request.user_id)
        if not user_exists:
            logger.info(f"New user detected: {request.user_id}")
        else:
            memory_count = ai_agent_service.get_user_memory_count(request.user_id)
            logger.info(f"Existing user: {request.user_id} with {memory_count} memories")
        
        # Generate AI response using the service
        result = await ai_agent_service.generate_response(
            user_message=request.message,
            user_id=request.user_id,
            session_id=request.session_id,
            metadata=request.metadata
        )
        
        # Return structured response
        return ChatResponse(**result)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": "internal_error",
                "message": "An unexpected error occurred while processing your request",
                "suggestions": [
                    "Try again in a few moments",
                    "Check if all required services are running",
                    "Contact support if the problem persists"
                ]
            }
        ) 