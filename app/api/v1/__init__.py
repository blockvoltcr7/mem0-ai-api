from fastapi import APIRouter
from app.api.v1.endpoints import hello_world_v1, chat, health

# Create the main v1 router
api_router = APIRouter()

# Include routes from endpoints
api_router.include_router(hello_world_v1.router, tags=["hello"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(health.router, tags=["health"]) 