# Discord: @codaxy
# Telegram: @virgingod

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference  # type: ignore

from xfind.main.routes import router


async def aiohttp_close_session() -> None:
    from xfind.services.aiohttp_helper import AiohttpHelper

    session = AiohttpHelper.get_session()
    await session.close()


app = FastAPI(
    title="xFind - API",
    description="API para realizar consultas de dados do xFind",
    on_shutdown=[aiohttp_close_session],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RootResponse(BaseModel):
    Hello: str = "World"


@app.get("/", response_model=RootResponse)
async def root():
    return JSONResponse(content={"Hello": "World"}, status_code=200)


@app.get("/v1/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title,
    )


app.include_router(router, prefix="")
