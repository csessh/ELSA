FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "fastapi", "run", "/app/services/quiz/main.py", "--port", "9000"]
