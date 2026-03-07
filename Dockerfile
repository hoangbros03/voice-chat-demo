# Multi-stage Dockerfile for voice-chat-demo services
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the entire workspace
COPY . .

# Install uv package manager for faster dependency resolution
RUN pip install --no-cache-dir uv

# Install dependencies using uv
RUN uv sync --all-extras

# Expose ports for all services
EXPOSE 8000 8001 8002

# Default command (can be overridden)
CMD ["python", "-m", "uvicorn", "services.fastrtc_core.main:app", "--host", "0.0.0.0", "--port", "8000"]
