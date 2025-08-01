# Multi-stage build per ottimizzare le dimensioni dell'immagine
FROM python:3.11-slim as builder

# Installa dipendenze di sistema necessarie per la compilazione
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Crea directory di lavoro
WORKDIR /app

# Copia requirements e installa dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Scarica modelli NLTK necessari
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger')"

# Stage finale - immagine di produzione
FROM python:3.11-slim

# Crea utente non-root per sicurezza
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Installa solo le dipendenze runtime necessarie
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crea directory dell'applicazione
WORKDIR /app

# Copia dipendenze Python dal builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copia dati NLTK dal builder stage
COPY --from=builder /root/nltk_data /home/appuser/nltk_data

# Copia codice sorgente
COPY src/ ./src/
COPY examples/ ./examples/
COPY tests/ ./tests/
COPY README.md .

# Crea directory per logs e cache
RUN mkdir -p /app/logs /app/cache && \
    chown -R appuser:appuser /app

# Imposta variabili d'ambiente
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH \
    NLTK_DATA=/home/appuser/nltk_data \
    FLASK_APP=src/api.py \
    FLASK_ENV=production \
    LOG_LEVEL=INFO \
    CACHE_DIR=/app/cache

# Esponi porta
EXPOSE 5000

# Cambia all'utente non-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando di avvio
CMD ["python", "src/api.py"]

# Labels per metadata
LABEL maintainer="Product Categorizer Team" \
      version="1.0.0" \
      description="Intelligent Product Categorizer with SEO Optimization" \
      org.opencontainers.image.source="https://github.com/your-org/product-categorizer-seo"