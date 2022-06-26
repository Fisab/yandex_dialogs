from fastapi import FastAPI

from pixoo_app.handlers import health
from pixoo_app.handlers import pixoo


def init_app() -> FastAPI:
    app = FastAPI(
        title='pixo_app', swagger_ui_parameters={'defaultModelsExpandDepth': -1}
    )

    app.include_router(health.router)
    app.include_router(pixoo.router)

    return app


app = init_app()
