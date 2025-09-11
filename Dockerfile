FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK corpora
RUN python -m nltk.downloader punkt stopwords wordnet

# Download TextBlob corpora
RUN python -m textblob.download_corpora

# Download SpaCy English model
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
