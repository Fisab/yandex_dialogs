FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

COPY food_app ./food_app
COPY super_app ./super_app
COPY utils ./utils

RUN python3 -m pip install -r requirements.txt


CMD ["uvicorn", "super_app.__main__:app", "--host", "0.0.0.0", "--port", "80"]
