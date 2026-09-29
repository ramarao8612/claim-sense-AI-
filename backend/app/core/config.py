"""Central settings. Every secret / URL comes from environment variables,
never hard-coded. Copy .env.example -> .env locally if you need overrides."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg2://claimsense:claimsense@localhost:5432/claimsense"
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket: str = "claimsense-docs"
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.1:8b"
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"


settings = Settings()
