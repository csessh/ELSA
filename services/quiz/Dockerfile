FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "services/quiz/main.py", "-name", "quiz_1", "-rounds", "30", "-players", "10"]

