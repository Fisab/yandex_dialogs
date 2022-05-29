from fastapi import FastAPI

from food_app.handlers import health
from food_app.handlers import papa_johns
from food_app.handlers import config


def init_app() -> FastAPI:
    app = FastAPI()

    app.include_router(health.router)
    app.include_router(papa_johns.router)
    app.include_router(config.router)

    return app


app = init_app()
