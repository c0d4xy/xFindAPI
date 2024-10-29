# Discord: @codaxy
# Telegram: @virgingod

from typing import Any

import jwt


class JwtHelper:
    def __init__(self, secret: str) -> None:
        self.secret = secret

    def encode(self, payload: dict[str, Any]) -> str:
        return jwt.encode(payload, self.secret, algorithm="HS256")  # type: ignore

    def decode(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, self.secret, algorithms=["HS256"])  # type: ignore
