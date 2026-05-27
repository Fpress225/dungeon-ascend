from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="AUTH_")

    app_name: str = "DungeonAscend Auth Service"
    host: str = "0.0.0.0"
    port: int = 8001
    database_url: str = "sqlite:///./auth.db"
    secret_key: str = "change-me-in-production-use-long-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


settings = Settings()
