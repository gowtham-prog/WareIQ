import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: int = os.getenv("MAIL_PORT", 587)
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "your-email@gmail.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "your-password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "your-email@gmail.com")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "FastAPI App")
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    class Config:
        env_file = ".env"

