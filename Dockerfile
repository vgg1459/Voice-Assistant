FROM python:3.11-slim

WORKDIR /app

# System deps + tini + Ollama
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg \
      libsndfile1 \
      curl \
      ca-certificates \
      zstd \
      tini && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# Create an entrypoint INSIDE the image (no separate file needed)
RUN printf '%s\n' \
'#!/bin/sh' \
'set -eu' \
'' \
'echo "=== Starting Ollama + Streamlit ==="' \
'' \
'export OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"' \
'export OLLAMA_MAX_LOADED_MODELS="${OLLAMA_MAX_LOADED_MODELS:-1}"' \
'export OLLAMA_NUM_PARALLEL="${OLLAMA_NUM_PARALLEL:-1}"' \
'' \
'# Start Ollama' \
'ollama serve > /tmp/ollama.log 2>&1 &' \
'OLLAMA_PID=$!' \
'' \
'# Wait for Ollama' \
'echo "Waiting for Ollama..."' \
'i=0; while [ $i -lt 60 ]; do' \
'  if curl -fsS http://localhost:11434/api/tags >/dev/null 2>&1; then' \
'    echo "✓ Ollama ready"' \
'    break' \
'  fi' \
'  i=$((i+1))' \
'  sleep 1' \
'done' \
'if [ $i -ge 60 ]; then' \
'  echo "ERROR: Ollama did not start in time"' \
'  cat /tmp/ollama.log || true' \
'  exit 1' \
'fi' \
'' \
'# Ensure model (lowercase)' \
'MODEL="${OLLAMA_MODEL:-qwen2.5:7b-instruct}"' \
'echo "Ensuring model: $MODEL"' \
'ollama list | awk "{print tolower(\\$1)}" | grep -q "^$(echo "$MODEL" | tr "[:upper:]" "[:lower:]")$" || ollama pull "$MODEL"' \
'' \
'echo "Starting Streamlit on 0.0.0.0:8501"' \
'exec streamlit run ui.py --server.address=0.0.0.0 --server.port=8501' \
> /usr/local/bin/start.sh && chmod +x /usr/local/bin/start.sh

EXPOSE 8501

# Run as one container with proper init handling
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/usr/local/bin/start.sh"]
