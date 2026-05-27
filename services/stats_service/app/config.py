from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="STATS_")

    app_name: str = "DungeonAscend Stats Service"
    host: str = "0.0.0.0"
    port: int = 8002
    database_url: str = "sqlite:///./stats.db"
    jwt_secret_key: str = "change-me-in-production-use-long-random-string"
    jwt_algorithm: str = "HS256"
    auth_service_url: str = "http://localhost:8001"
    verify_via_auth_service: bool = False


settings = Settings()
