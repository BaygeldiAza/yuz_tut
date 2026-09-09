FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN pip install --no-cache-dir \
    --proxy "$HTTP_PROXY" \
    -r requirements.txt

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]