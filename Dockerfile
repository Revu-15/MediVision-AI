FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Create necessary directories with correct permissions
RUN mkdir -p uploads reports && chmod -R 777 uploads reports

# Create non-root user (required by Hugging Face Spaces)
RUN useradd -m -u 1000 appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 7860 8080 5000

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV HOME=/home/appuser
ENV HF_HOME=/home/appuser/.cache/huggingface

# Run with gunicorn using dynamic PORT if set, defaulting to 7860
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-7860} --timeout 300 --workers 1"]
