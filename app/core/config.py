from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings using Pydantic."""
    
    # API Keys
    openai_api_key: str = ""
    elevenlabs_api_key: str = ""
    
    # Qdrant settings
    qdrant_url: str = ""
    qdrant_port: Optional[int] = 6333
    qdrant_use_https: bool = True
    qdrant_collection_name: str = "mem0_production"  # Updated to match your env
    
    # Mem0 settings (keeping backward compatibility)
    mem0_collection_name: str = ""  # Will use qdrant_collection_name if empty
    
    # AI Agent settings
    ai_model: str = "gpt-4o-mini"
    ai_temperature: float = 0.7
    ai_max_tokens: int = 1000
    memory_search_limit: int = 5
    
    # Production settings
    environment: str = "production"
    log_level: str = "INFO"
    
    # Directory paths
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    images_dir: Path = base_dir / "output" / "images"
    audio_dir: Path = base_dir / "output" / "audio"
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix=""
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use qdrant_collection_name if mem0_collection_name is not set
        if not self.mem0_collection_name:
            self.mem0_collection_name = self.qdrant_collection_name

# Create global settings instance
settings = Settings()

# Ensure output directories exist
os.makedirs(settings.images_dir, exist_ok=True)
os.makedirs(settings.audio_dir, exist_ok=True)
