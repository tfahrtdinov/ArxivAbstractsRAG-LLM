FROM python:3.12-slim
LABEL authors="tfahrtdinov"

# uv install
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache --no-dev --no-group script

CMD ["/app/.venv/bin/uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
