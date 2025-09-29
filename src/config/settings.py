import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

load_dotenv()

class ClaudeConfig(BaseModel):
    api_key: str = Field(..., description="Claude API key")
    model: str = Field(default="claude-3-sonnet-20240229", description="Claude model to use")

class AppConfig(BaseModel):
    node_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="info", description="Logging level")

class GoPhishConfig(BaseModel):
    api_url: Optional[str] = Field(default=None, description="GoPhish API URL")
    api_key: Optional[str] = Field(default=None, description="GoPhish API key")

class Config(BaseModel):
    claude: ClaudeConfig
    app: AppConfig
    gophish: GoPhishConfig

def load_config() -> Config:
    """Load configuration from environment variables."""
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        raise ValueError("CLAUDE_API_KEY environment variable is required")

    return Config(
        claude=ClaudeConfig(
            api_key=claude_api_key,
            model=os.getenv("CLAUDE_MODEL", "claude-3-sonnet-20240229")
        ),
        app=AppConfig(
            node_env=os.getenv("NODE_ENV", "development"),
            log_level=os.getenv("LOG_LEVEL", "info")
        ),
        gophish=GoPhishConfig(
            api_url=os.getenv("GOPHISH_API_URL"),
            api_key=os.getenv("GOPHISH_API_KEY")
        )
    )

def validate_config() -> bool:
    """Validate configuration."""
    try:
        load_config()
        return True
    except ValueError as e:
        raise e