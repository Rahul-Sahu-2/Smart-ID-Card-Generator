from pathlib import Path
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Smart Identity Generator"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./smart_id.db"
    storage_dir: Path = Path("storage")
    jwt_secret: str = "super-secret-key-change-me"
    jwt_algorithm: str = "HS256"
    default_brand_palette: List[str] = Field(
        default_factory=lambda: ["#1D6FFF", "#6F00FF", "#00F3FF", "#F8FBFF", "#000319"]
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

