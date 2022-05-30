from fastapi import FastAPI
from food_app.handlers import health
from food_app.__main__ import app as food_app
from utils.config import get_config


def init_app() -> FastAPI:
    config = get_config(root='super_app')
    app = FastAPI(root_path=config.root_path)
    print(123, config.root_path)

    app.mount('/food_app', food_app)
    app.include_router(health.router)

    return app


app = init_app()
