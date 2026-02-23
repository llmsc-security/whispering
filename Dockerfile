# Dockerfile for Sharrnah--whispering
# Based on Python 3.11-slim for audio processing
# Note: This is a CPU-only build. For GPU support, use cuda images.

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
# Added binutils for execstack tool to fix ctranslate2 executable stack issues
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libsndfile1 \
    libportaudio2 \
    libportaudiocpp0 \
    portaudio19-dev \
    libatlas3-base \
    libopenblas-dev \
    libsox-fmt-mp3 \
    ffmpeg \
    libsox3 \
    curl \
    git \
    binutils \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./

# Install dependencies using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV NLTK_DATA=/app/nltk_data

# Copy NLTK data from host (already downloaded on host)
# The NLTK data is expected to be at /tmp/nltk_data/ on the host
# and will be copied to /app/nltk_data/ in the container
COPY nltk_data/ /app/nltk_data/

# Ensure NLTK data directories exist and are readable
RUN mkdir -p /app/nltk_data/corpora /app/nltk_data/tokenizers && \
    chmod -R 755 /app/nltk_data

# Patch nltk __init__.py to skip wordnet import
COPY patch_nltk.py /tmp/patch_nltk.py
RUN python /tmp/patch_nltk.py

# Install sitecustomize.py for NLTK stubs (loaded automatically on Python start)
COPY sitecustomize.py /usr/local/lib/python3.11/site-packages/sitecustomize.py

# Use the existing entrypoint.sh from the repo (lowercase p)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose mapped port 11010
EXPOSE 11010

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
