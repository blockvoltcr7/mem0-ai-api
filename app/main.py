import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.api.v1 import api_router
from app.core.mem0_manager import mem0_manager
from app.core.config import settings

# Configure logging based on environment settings
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    logger.info(f"Starting AI Agent API in {settings.environment} environment")
    logger.info(f"Using collection: {settings.mem0_collection_name}")
    logger.info("Initializing Mem0 system...")
    
    success = await mem0_manager.initialize()
    if success:
        logger.info("Mem0 system initialized successfully")
    else:
        logger.error("Failed to initialize Mem0 system")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Agent API")

def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="AI Agent Mem0 API",
        version="1.0.0",
        description="""
## AI Agent with Persistent Memory

This API provides conversational AI capabilities with persistent memory using **Mem0** and **Qdrant** vector database.

### Features
- 🧠 **Persistent Memory**: Conversations stored and retrieved across sessions
- 👤 **User Isolation**: Each user has their own memory space  
- 🔍 **Context-Aware**: AI responses based on conversation history
- 📊 **Health Monitoring**: Comprehensive system health checks
- 🚀 **High Performance**: Optimized for production use

### Quick Start
1. Use the `/chat` endpoint to send messages
2. Include a unique `user_id` for memory persistence
3. Optional: Add `session_id` for conversation grouping
4. Check `/health/detailed` for system status

### Example Usage
```json
{
  "user_id": "user123",
  "message": "I'm interested in BPC-157 peptide",
  "metadata": {
    "domain": "peptide_coaching",
    "session_id": "consultation_2024"
  }
}
```
        """,
        routes=app.routes,
    )
    
    # Add custom tags
    openapi_schema["tags"] = [
        {
            "name": "chat",
            "description": "Conversational AI with persistent memory"
        },
        {
            "name": "health", 
            "description": "System health and monitoring endpoints"
        },
        {
            "name": "hello",
            "description": "Basic API endpoints"
        }
    ]
    
    # Add contact and license info
    openapi_schema["info"]["contact"] = {
        "name": "AI Tutor Development Team",
        "email": "support@example.com"
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app = FastAPI(
    title="AI Agent Mem0 API", 
    version="1.0.0",
    description="Conversational AI with persistent memory using Mem0 and Qdrant",
    docs_url="/docs",  # Always enable Swagger UI
    redoc_url="/redoc",  # Always enable ReDoc
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["hello"])
async def root():
    """
    Root endpoint providing API information and status.
    
    Returns basic information about the API including version,
    environment, and current status.
    """
    return {
        "message": "AI Agent Mem0 API", 
        "version": "1.0.0",
        "environment": settings.environment,
        "status": "running",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """
    Basic health check endpoint.
    
    Returns a simple health status for basic monitoring
    and load balancer health checks.
    """
    return {"status": "healthy", "message": "API is running successfully"}

# To run this application:
# Ensure you are in the root directory of the project
# Activate your virtual environment: source .venv/bin/activate
# Run: uvicorn app.main:app --reload