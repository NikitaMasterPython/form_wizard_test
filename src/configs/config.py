import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str = os.environ.get("APP_BOT_TOKEN", "")
    TIME_OUT: int = os.environ.get("APP_TIMEOUT", 100)
    GIGA_SCOPE: str = os.environ.get("APP_GIGA_SCOPE", "")
    GIGA_AUTHORIZATION_KEY: str = os.environ.get("APP_GIGA_AUTHORIZATION_KEY", "")
    GIGA_OAUTH_URL: str = os.environ.get("APP_GIGA_OAUTH_URL", "")


settings = Settings()
