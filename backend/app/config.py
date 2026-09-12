from  pydantic_settings  import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/yuz_tut"

    
    redis_url: str = "redis://redis:6379/0"

    
    jwt_secret: str 
    jwt_algorithm: str 
    access_token_expire_minutes: int 
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )   

settings = Settings()
