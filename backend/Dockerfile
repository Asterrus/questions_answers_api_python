FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PATH="/app/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# ENV UV_PROJECT_ENVIRONMENT=/opt/venv
# ENV VIRTUAL_ENV=/opt/venv

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

COPY ./pyproject.toml ./uv.lock /app/

COPY ./app /app/app
COPY ./tests /app/tests
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/alembic.ini
COPY ./scripts /app/scripts

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN chmod +x /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/run_migrations.py

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
