import os

from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings


load_dotenv()

class DatabaseSettings(BaseSettings):
    MYSQL_USER: str | None = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD: str | None = os.environ.get("MYSQL_PASSWORD")
    MYSQL_HOST: str | None = os.environ.get("MYSQL_HOST")
    MYSQL_PORT: str | None = os.environ.get("MYSQL_PORT")
    MYSQL_DATABASE: str | None = os.environ.get("MYSQL_DATABASE")
    db_url: str | None = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    sync_db_url: str | None = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

class ApplicationSettings(BaseSettings):
    PROJECT_NAME: str = "Base"
    PROJECT_VERSION: str = "0.1.0"
    PROJECT_DESCRIPTION: str = "For Backend Project Base"
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "SECRET_KEY")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT")

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
