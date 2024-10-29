# Discord: @codaxy
# Telegram: @virgingod

import jwt
from fastapi import HTTPException, Request

from xfind.core.config import Settings

from .jwt_helper import JwtHelper

jwt_helper = JwtHelper(secret=Settings.JWT_TOKEN_SECRET)


async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header is None or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Token de autenticação não fornecido ou inválido"
        )

    token = auth_header.split(" ")[1]

    try:
        payload = jwt_helper.decode(token)
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
