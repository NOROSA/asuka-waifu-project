from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    api_base: str = Field(
        "https://generativelanguage.googleapis.com/v1beta/openai", env="API_BASE"
    )
    model_name: str = Field("gemini-2.0-flash", env="MODEL_NAME")
    temperature: float = 0.7
    max_tokens: int | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()