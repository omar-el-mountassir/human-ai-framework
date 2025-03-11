FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH="/app:$PYTHONPATH" \
    UV_CACHE_DIR=/opt/uv-cache/ \
    UV_COMPILE_BYTECODE=1

# Install UV
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.cargo/bin/uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md ./

# Install dependencies first (for better caching)
RUN --mount=type=cache,target=/opt/uv-cache/ \
    uv pip install -e .

# Copy the rest of the application
COPY . .

# Install the application
RUN --mount=type=cache,target=/opt/uv-cache/ \
    uv pip install -e .

# Create a non-root user to run the application
RUN useradd -m appuser
USER appuser

# Set the entrypoint
ENTRYPOINT ["haif"]
CMD ["--config", "config", "--env", "production"] 