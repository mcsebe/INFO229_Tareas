FROM python:3.8-slim AS base
RUN apt-get update && apt-get install --no-install-recommends --yes python3
RUN python3 -m pip install --upgrade pip
RUN pip install fastapi
RUN pip install sqlalchemy
RUN pip install uvicorn
RUN pip install mysql-connector-python

COPY app/ app/

CMD ["uvicorn","app.main:app","--reload"]
