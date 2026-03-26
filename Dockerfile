FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

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
    uv sync --frozen --no-dev

# Exposing port:
EXPOSE 8000

# Define process to run:
ENTRYPOINT ["uv", "run", "--no-sync", "mcp"]