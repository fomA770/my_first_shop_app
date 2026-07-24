#config.py
from pydantic_settings import BaseSettings
from pydantic import Field
import os

class Settings(BaseSettings):
    DATABASE_URL: str = ""
    SECRET_KEY: str = Field(default="CEKRЕЕнО!") #TODO
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    class Config:
        env_file = ".env"

settings = Settings()

# ✅ ДОБАВЬТЕ ЭТО ДЛЯ ДИАГНОСТИКИ!
print("=" * 50)
print("🔍 ЗНАЧЕНИЯ НАСТРОЕК ИЗ .env:")
print(f"  DATABASE_URL: {settings.DATABASE_URL}")
print(f"  SECRET_KEY: {settings.SECRET_KEY[:10]}...")
print(f"  ALGORITHM: {settings.ALGORITHM}")
print(f"  ACCESS_TOKEN_EXPIRE_MINUTES: {settings.ACCESS_TOKEN_EXPIRE_MINUTES}")
print(f"  ТЕКУЩАЯ РАБОЧАЯ ДИРЕКТОРИЯ: {os.getcwd()}") # Добавим для проверки путей
print("=" * 50)