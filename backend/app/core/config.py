from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Default local sqlite connection if .env is missing
    DATABASE_URL: str = "sqlite:///./gpay.db"
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()