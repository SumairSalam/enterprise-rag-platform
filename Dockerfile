
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

WORKDIR /app

COPY requirements.txt .

# Install CPU-only PyTorch to avoid NVIDIA CUDA dependencies
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY src/ ./src/
COPY data/ ./data/

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py"]
