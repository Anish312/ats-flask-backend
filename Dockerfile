# Use slim Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install CPU-only torch separately
RUN pip install --no-cache-dir torch==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK corpora (optional: can do at runtime to reduce image size)
RUN python -m nltk.downloader punkt stopwords wordnet

# Download SpaCy English model
RUN python -m spacy download en_core_web_sm

# Copy app code
COPY . .

# Expose Render port
EXPOSE 5000

# Start FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
