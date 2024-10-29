# Discord: @codaxy
# Telegram: @virgingod

from fastapi import APIRouter

from xfind.main.routes.cpf import router as cpf

router = APIRouter()

router.include_router(cpf, prefix="/v1/query")
