import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()