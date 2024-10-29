# Discord: @codaxy
# Telegram: @virgingod

from aiohttp import ClientSession


class AiohttpHelper:
    __session: ClientSession | None = None

    @classmethod
    def get_session(cls) -> ClientSession:
        if not cls.__session:
            cls.__session = ClientSession()
        return cls.__session
