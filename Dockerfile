# syntax=docker/dockerfile:1

# Build for linux/amd64 architecture
FROM --platform=linux/amd64 python:3.13-slim AS base

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies (production only)
RUN uv sync --frozen --no-dev

# Copy source code
COPY src ./src

# Expose default port
EXPOSE 9009

# Set entrypoint to run the server module
# Accepts --host, --port, --card-url arguments
ENTRYPOINT ["uv", "run", "--", "python", "-m", "agentbeats.server"]

# Default command (can be overridden)
CMD ["--host", "0.0.0.0", "--port", "9009"]
