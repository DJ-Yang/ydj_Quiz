import os
import urllib.parse
import json
from dotenv import load_dotenv
from pydantic import validator, ValidationError
from pydantic_settings import BaseSettings
from typing import Dict

load_dotenv()

class DatabaseSettings(BaseSettings):
    MYSQL_USER: str | None
    MYSQL_PASSWORD: str | None
    MYSQL_HOST: str | None
    MYSQL_PORT: str | None
    MYSQL_DATABASE: str | None
    
    @property
    def db_url(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    @property
    def sync_db_url(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "Base"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "For Backend Project Base"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "SECRET_KEY")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT")
    EXCEPT_PATH_REGEX: str = r"^(/health|/metrics)$"

    db: DatabaseSettings = DatabaseSettings()

    class Config:
        env_file = ".env"
        extra = "allow"

    if ENVIRONMENT == "production":
        echo: bool = False
    else:
        echo: bool = True

try:
    settings = ApplicationSettings()
except ValidationError as e:
    print("Validation errors:", e.errors())
    print("Failed to load or validate configuration:", e)
