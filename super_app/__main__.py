from fastapi import FastAPI
from food_app.handlers import health
from food_app.__main__ import app as food_app


def init_app() -> FastAPI:
	app = FastAPI()

	app.mount('/food_app', food_app)
	app.include_router(health.router)

	return app


app = init_app()
