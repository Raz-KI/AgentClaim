from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str

    database_url: str

    gemini_api_key: str

    supabase_url: str

    supabase_anon_key: str

    class Config:
        env_file = ".env"


settings = Settings()