"""Application configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Plum Claims AI"

    class Config:
        env_file = ".env"


settings = Settings()