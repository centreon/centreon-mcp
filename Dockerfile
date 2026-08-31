# --- Builder ---

FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

# Set working directory:
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the project into the image
COPY pyproject.toml uv.lock ./
COPY centreon_mcp centreon_mcp

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-dev

# --- Runtime ---

FROM python:3.14-slim-bookworm

# Set working directory:
WORKDIR /app

# Copy dependencies from previous stage:
COPY --from=builder /app/.venv /app/.venv

# Exposing port:
EXPOSE 8000

RUN useradd -U -u 1000 appuser && chown -R 1000:1000 /app
USER 1000

# Run the application
ENTRYPOINT ["/app/.venv/bin/centreon-mcp-server"]