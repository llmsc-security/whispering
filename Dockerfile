# Dockerfile for Sharrnah--whispering
# Based on Python 3.11-slim for audio processing
# Note: This is a CPU-only build. For GPU support, use cuda images.

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for audio processing
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

# Create entrypoint script with NLTK data download
RUN echo '#!/bin/bash\n\
set -e\n\
\necho "Starting Whispering Tiger audio processing..."\n\
\necho "Downloading NLTK data..."\n\
python -c "import nltk; nltk.download(\"wordnet\", quiet=True); nltk.download(\"punkt\", quiet=True); nltk.download(\"punkt_tab\", quiet=True)"\n\
\ncd /app\n\
\necho "Starting websocket server on 0.0.0.0:5000..."\n\
exec python audioWhisper.py --websocket_ip 0.0.0.0 --websocket_port 5000 "$@"\n\
' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose websocket port
EXPOSE 5000

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
