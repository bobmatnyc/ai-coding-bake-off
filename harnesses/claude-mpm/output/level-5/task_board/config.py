"""Application configuration via environment variables."""
import os


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./task_board.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme-in-production")
    TESTING: bool = os.getenv("TESTING", "").lower() in ("true", "1", "yes")


settings = Settings()
