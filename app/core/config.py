from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")
    database_url_sync: str | None = Field(default=None, alias="DATABASE_URL_SYNC")
    app_host: str = Field(default="127.0.0.1", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
