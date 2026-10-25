FROM python:3.11-slim

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:0.12.10 /uv /uvx /bin/

ARG HTTP_PROXY
ARG HTTPS_PROXY

ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./alembic.ini

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]