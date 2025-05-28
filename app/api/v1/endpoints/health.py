#!/usr/bin/env python3
"""
Health Endpoint

Enhanced health check endpoint for monitoring system components.
Provides detailed status of Mem0, Qdrant, and OpenAI services.

Author: AI Tutor Development Team
Version: 1.0
"""

import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from app.models.chat_models import HealthStatus
from app.core.mem0_manager import mem0_manager

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

@router.get(
    "/health/detailed", 
    response_model=HealthStatus, 
    summary="Detailed System Health Check",
    description="""
    **Perform comprehensive health check of all system components.**
    
    This endpoint provides detailed monitoring of:
    - 🧠 **Mem0 memory system** - Initialization and functionality status
    - 🗄️ **Qdrant vector database** - Connection and collection status  
    - 🤖 **OpenAI API** - Connectivity and model availability
    - ⚙️ **Overall system health** - Aggregated status assessment
    
    ### Status Levels:
    - **healthy**: All systems operational
    - **degraded**: Some non-critical issues detected
    - **unhealthy**: Critical systems unavailable
    
    ### Use Cases:
    - Production monitoring and alerting
    - Debugging system issues
    - Pre-deployment health verification
    - Load balancer health checks (detailed)
    """,
    responses={
        200: {
            "description": "Health check completed successfully",
            "content": {
                "application/json": {
                    "example": {
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
                }
            }
        }
    }
)
async def detailed_health_check() -> HealthStatus:
    """
    Perform detailed health check of all system components.
    
    This endpoint checks the status of:
    - Mem0 memory system
    - Qdrant vector database
    - OpenAI API connectivity
    
    Returns:
        HealthStatus: Detailed status of all system components
        
    Raises:
        HTTPException: If critical systems are unavailable
    """
    try:
        logger.info("Performing detailed health check")
        
        # Get status from Mem0 manager
        services_status = mem0_manager.get_status()
        
        # Determine overall system status
        overall_status = "healthy"
        
        # Check if any critical services are down
        if services_status["mem0"]["status"] != "initialized":
            overall_status = "degraded"
            logger.warning("Mem0 system not initialized")
        
        if services_status["qdrant"]["status"] != "connected":
            overall_status = "degraded"
            logger.warning("Qdrant not connected")
        
        if services_status["openai"]["status"] != "available":
            overall_status = "degraded"
            logger.warning("OpenAI not available")
        
        # If Mem0 is not initialized, consider it unhealthy
        if services_status["mem0"]["status"] != "initialized":
            overall_status = "unhealthy"
        
        health_status = HealthStatus(
            status=overall_status,
            services=services_status,
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Health check completed with status: {overall_status}")
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        
        # Return unhealthy status with error information
        error_status = HealthStatus(
            status="unhealthy",
            services={
                "mem0": {"status": "error", "error": str(e)},
                "qdrant": {"status": "unknown"},
                "openai": {"status": "unknown"}
            },
            timestamp=datetime.utcnow()
        )
        
        return error_status

@router.get(
    "/health", 
    summary="Basic Health Check",
    description="""
    **Simple health check endpoint for basic monitoring.**
    
    This endpoint provides a lightweight health status check suitable for:
    - 🔄 **Load balancer health checks** - Fast response for traffic routing
    - 📊 **Basic monitoring** - Simple up/down status
    - 🚀 **Quick status verification** - Minimal resource usage
    
    ### Response Format:
    Returns a simple JSON object with status, message, and timestamp.
    
    ### Status Values:
    - **healthy**: System is fully operational
    - **degraded**: System running but with some issues
    - **unhealthy**: Critical system failures detected
    """,
    responses={
        200: {
            "description": "Basic health status",
            "content": {
                "application/json": {
                    "examples": {
                        "healthy": {
                            "summary": "System healthy",
                            "value": {
                                "status": "healthy",
                                "message": "AI Agent API is running successfully",
                                "timestamp": "2024-01-15T10:30:00Z"
                            }
                        },
                        "degraded": {
                            "summary": "System degraded",
                            "value": {
                                "status": "degraded",
                                "message": "AI Agent API is running but some services may be unavailable",
                                "timestamp": "2024-01-15T10:30:00Z"
                            }
                        }
                    }
                }
            }
        }
    }
)
async def basic_health_check() -> dict:
    """
    Basic health check endpoint for simple monitoring.
    
    Returns:
        dict: Simple status response
    """
    try:
        # Quick check if Mem0 is initialized
        is_healthy = mem0_manager.is_healthy()
        
        if is_healthy:
            return {
                "status": "healthy",
                "message": "AI Agent API is running successfully",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            return {
                "status": "degraded",
                "message": "AI Agent API is running but some services may be unavailable",
                "timestamp": datetime.utcnow().isoformat()
            }
            
    except Exception as e:
        logger.error(f"Basic health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "message": f"AI Agent API encountered an error: {str(e)}",
            "timestamp": datetime.utcnow().isoformat()
        } 