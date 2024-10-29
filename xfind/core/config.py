# Discord: @codaxy
# Telegram: @virgingod

from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    # SIPNI
    SIPNI_EMAIL: str
    SIPNI_PASSWORD: str

    # JWT
    JWT_TOKEN_SECRET: str


Settings = _Settings(_env_file=".env")  # type: ignore
