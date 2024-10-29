# Discord: @codaxy
# Telegram: @virgingod

import uvicorn


def start():
    uvicorn.run("xfind.main.app:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    start()
