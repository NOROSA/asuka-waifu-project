from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Telegram
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    
    # Gemini (principal)
    google_api_key: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    
    # DeepSeek (fallback 1)
    deepseek_api_key: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    
    # Groq (fallback 2) 
    groq_api_key: Optional[str] = Field(None, env="GROQ_API_KEY")
    
    # Configuración heredada (por compatibilidad)
    api_base: str = Field(
        "https://generativelanguage.googleapis.com/v1beta/openai", env="API_BASE"
    )
    model_name: str = Field("gemini-2.0-flash", env="MODEL_NAME")
    temperature: float = 0.7
    max_tokens: Optional[int] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()