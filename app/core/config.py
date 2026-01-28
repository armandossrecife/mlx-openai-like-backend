from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    LLM_SERVER_BASE_URL: str = "http://localhost:8080"
    ALLOW_ORIGINS: str = "*"

    JWT_SECRET_KEY: str = "CHANGE_ME_SUPER_SECRET"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24

    DATABASE_URL: str = "sqlite:///./app.db"
    MODELO_LLM: str  = "mlx-community/Qwen3-4B-Instruct-2507-4bit"

settings = Settings()