# Use slim Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install minimal system dependencies (only what's needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .

# Install dependencies in one layer & clean pip cache
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Download SpaCy + NLTK models in same layer
RUN python -m spacy download en_core_web_sm \
    && python -m nltk.downloader punkt stopwords wordnet \
    && rm -rf /root/.cache/*

# Copy app code last (to avoid cache busting on every change)
COPY . .

# Expose Render/Heroku port
EXPOSE 5000

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
