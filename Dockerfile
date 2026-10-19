# ==========================================
# Multi-Stage Dockerfile for VoiceForm AI
# Compatible with Hugging Face Spaces, Render, Railway, and Docker
# ==========================================

# Stage 1: Build the React 19 Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Python 3.12 Backend + FFmpeg + Whisper
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=7860 \
    HOME=/home/user

# Install system dependencies (FFmpeg is required for Whisper speech recognition)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root user (UID 1000) for Hugging Face Spaces & security
RUN useradd -m -u 1000 user
ENV PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Install PyTorch CPU and backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend application and sample datasets
COPY backend/ ./backend/
COPY datasets/ ./datasets/

# Copy built frontend assets from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure proper permissions for user
RUN chown -R user:user /app /home/user

USER user

# Hugging Face Spaces exposes port 7860 by default; also responds to $PORT if set
EXPOSE 7860

WORKDIR /app/backend

# Launch production server with dynamic port fallback
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
