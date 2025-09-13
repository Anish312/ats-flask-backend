# Stage 1: build
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: runtime
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
