"""
Application configuration settings using Pydantic BaseSettings.
"""

from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = Field("Expense Manager", env="APP_NAME")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    DEBUG: bool = Field(True, env="DEBUG")
    API_V1_PREFIX: str = Field("/api/v1", env="API_V1_PREFIX")

    # Database
    DB_HOST: str = Field("localhost", env="DB_HOST")
    DB_PORT: int = Field(3306, env="DB_PORT")
    DB_USER: str = Field("root", env="DB_USER")
    DB_PASSWORD: str = Field("password", env="DB_PASSWORD")
    DB_NAME: str = Field("expense_db", env="DB_NAME")
    DB_POOL_SIZE: int = Field(10, env="DB_POOL_SIZE")
    DB_TIMEOUT: int = Field(30, env="DB_TIMEOUT")

    # Email (Optional example for notifications)
    EMAIL_HOST: Optional[str] = Field(None, env="EMAIL_HOST")
    EMAIL_PORT: Optional[int] = Field(None, env="EMAIL_PORT")
    EMAIL_USER: Optional[str] = Field(None, env="EMAIL_USER")
    EMAIL_PASSWORD: Optional[str] = Field(None, env="EMAIL_PASSWORD")
    EMAIL_USE_TLS: Optional[bool] = Field(True, env="EMAIL_USE_TLS")

    # JWT Authentication
    JWT_SECRET_KEY: str = Field("your-secret-key", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")

    # Redis Cache (optional)
    REDIS_HOST: Optional[str] = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: Optional[int] = Field(6379, env="REDIS_PORT")
    REDIS_DB: Optional[int] = Field(0, env="REDIS_DB")
    REDIS_PASSWORD: Optional[str] = Field(None, env="REDIS_PASSWORD")

    # File storage paths
    EXPORT_DIR: str = Field("exports", env="EXPORT_DIR")
    LOG_DIR: str = Field("logs", env="LOG_DIR")
    TEMP_DIR: str = Field("temp", env="TEMP_DIR")

    # Rate Limiting
    RATE_LIMIT: int = Field(100, env="RATE_LIMIT")
    RATE_LIMIT_INTERVAL: int = Field(60, env="RATE_LIMIT_INTERVAL")  # seconds

    # Localization
    DEFAULT_LANGUAGE: str = Field("en", env="DEFAULT_LANGUAGE")
    SUPPORTED_LANGUAGES: str = Field("en,fa", env="SUPPORTED_LANGUAGES")

    # Analytics/Monitoring
    ENABLE_METRICS: bool = Field(False, env="ENABLE_METRICS")
    SENTRY_DSN: Optional[str] = Field(None, env="SENTRY_DSN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
