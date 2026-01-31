from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

LLM_SERVER_PORT = os.getenv("LLM_SERVER_PORT", "8080")
LLM_SERVER_BASE_URL = f"http://localhost:{LLM_SERVER_PORT}/v1"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/meubanco")
print("DATABASE_URL:", DATABASE_URL)
MODELO_LLM = os.getenv("MODELO_LLM", "mlx-community/Qwen3-4B-Instruct-2507-4bit")
APP_NAME = os.getenv("APP_NAME", "API FastAPI com OpenAI-like")
DEBUG = os.getenv("DEBUG", "True")

class Settings(BaseSettings):
    APP_NAME: str = APP_NAME
    DEBUG: bool = DEBUG

    LLM_SERVER_BASE_URL: str = LLM_SERVER_BASE_URL
    ALLOW_ORIGINS: str = "*"

    JWT_SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = DATABASE_URL
    MODELO_LLM: str  = MODELO_LLM

settings = Settings()