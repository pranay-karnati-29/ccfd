FROM python:3.12-slim

# libgomp1 is required at runtime by xgboost (OpenMP support) - without it,
# "import xgboost" fails on slim base images.
# build-essential is a safety net in case any pip package needs to compile.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render sets $PORT itself; 10000 is just Render's documented default.
EXPOSE 10000

# Shell form so $PORT is expanded at container start.
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
