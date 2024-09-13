FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
ENV TZ="Asia/Shanghai"
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY . /app
WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv uv sync --compile-bytecode --frozen --no-install-project
HEALTHCHECK --start-period=30s --start-interval=1s --retries=3 CMD [ "curl", "-f", "http://localhost:8080/ping" ]
CMD [".venv/bin/python", "bot.py"]
