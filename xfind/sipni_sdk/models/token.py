# Discord: @codaxy
# Telegram: @virgingod

from pydantic import BaseModel


class Token(BaseModel):
    accessToken: str
    tokenType: str
    refreshToken: str
    scope: str
    organization: str
    jti: str
