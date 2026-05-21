from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    openai_api_key: str

    database_url: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()