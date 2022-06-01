from fastapi import FastAPI

from food_app.handlers import health
from food_app.handlers import papa_johns


def init_app() -> FastAPI:
    app = FastAPI(
        title='food_app', swagger_ui_parameters={'defaultModelsExpandDepth': -1}
    )

    app.include_router(health.router)
    app.include_router(papa_johns.router)

    return app


app = init_app()
