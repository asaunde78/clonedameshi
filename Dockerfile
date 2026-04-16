FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_TOOL_BIN_DIR=/usr/local/bin
WORKDIR /app
COPY ./src /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked
ENV PATH="/app/.venv/bin:$PATH"
ENTRYPOINT []

CMD ["uv", "run", "main.py"]