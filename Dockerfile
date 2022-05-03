FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

ENTRYPOINT [ "uvicorn", "myapp.main:app", "--host", "0.0.0.0" ]