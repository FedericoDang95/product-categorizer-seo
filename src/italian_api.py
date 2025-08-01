"""API Flask per il servizio di categorizzazione prodotti in italiano"""

import os
import json
import time
import logging
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bleach

# Importa i moduli personalizzati
from src.italian_categorizer import ItalianProductCategorizer
from src.validators import ProductInput
from src.exceptions import ProductCategorizerError, InvalidInputError, CategoryNotFoundError, ValidationError, RateLimitError
from src.monitoring import MetricsCollector

# Configura il logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crea l'applicazione Flask
app = Flask(__name__)

# Configura CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configura il limitatore di richieste
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Imposta la dimensione massima del contenuto
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Inizializza il categorizzatore e il collector di metriche
categorizer = ItalianProductCategorizer()
metrics = MetricsCollector()

# Context manager per la gestione degli errori
class error_handler:
    """Context manager per la gestione centralizzata degli errori"""
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False
        
        # Gestione degli errori personalizzati
        if issubclass(exc_type, ProductCategorizerError):
            logger.error(f"Errore di categorizzazione: {str(exc_val)}")
            response = jsonify({
                "error": "product_categorizer_error",
                "message": str(exc_val)
            })
            response.status_code = 400
            return True
        
        if issubclass(exc_type, InvalidInputError):
            logger.error(f"Errore di input: {str(exc_val)}")
            response = jsonify({
                "error": "invalid_input_error",
                "message": str(exc_val)
            })
            response.status_code = 400
            return True
        
        if issubclass(exc_type, CategoryNotFoundError):
            logger.error(f"Categoria non trovata: {str(exc_val)}")
            response = jsonify({
                "error": "category_not_found_error",
                "message": str(exc_val)
            })
            response.status_code = 404
            return True
        
        if issubclass(exc_type, ValidationError):
            logger.error(f"Errore di validazione: {str(exc_val)}")
            response = jsonify({
                "error": "validation_error",
                "message": str(exc_val)
            })
            response.status_code = 400
            return True
        
        if issubclass(exc_type, RateLimitError):
            logger.error(f"Limite di richieste superato: {str(exc_val)}")
            response = jsonify({
                "error": "rate_limit_error",
                "message": str(exc_val)
            })
            response.status_code = 429
            return True
        
        # Gestione degli errori generici
        logger.error(f"Errore non gestito: {str(exc_val)}")
        response = jsonify({
            "error": "internal_server_error",
            "message": "Si è verificato un errore interno del server"
        })
        response.status_code = 500
        return True

@app.route('/api/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """Endpoint per il controllo dello stato di salute dell'API"""
    return jsonify({
        "status": "ok",
        "version": "1.0.0",
        "language": "it"
    })

@app.route('/api/metrics', methods=['GET'])
def get_metrics() -> Dict[str, Any]:
    """Endpoint per ottenere le metriche del servizio"""
    return jsonify(metrics.get_metrics())

@app.route('/api/categorize', methods=['POST'])
@limiter.limit("10 per minute")
def categorize_product() -> Dict[str, Any]:
    """Endpoint per la categorizzazione di un prodotto"""
    start_time = time.time()
    
    with error_handler():
        # Ottieni i dati dalla richiesta
        data = request.get_json()
        if not data:
            raise InvalidInputError("Nessun dato JSON fornito")
        
        # Sanitizza l'input
        sanitized_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[key] = bleach.clean(value)
            else:
                sanitized_data[key] = value
        
        # Valida l'input con Pydantic
        try:
            product_input = ProductInput(**sanitized_data)
            
            # Forza la lingua italiana
            product_input.language = "it"
            
        except Exception as e:
            raise ValidationError(f"Errore di validazione dell'input: {str(e)}")
        
        # Categorizza il prodotto
        result = categorizer.categorize_product(product_input)
        
        # Prepara la risposta
        response = {
            "product_id": result.product_id,
            "title": result.title,
            "categories": result.categories,
            "keywords": result.keywords,
            "confidence": result.confidence,
            "language": result.language,
            "seo_suggestions": result.seo_suggestions,
            "processing_time": round(time.time() - start_time, 3)
        }
        
        # Aggiorna le metriche
        metrics.record_response_time(time.time() - start_time)
        
        return jsonify(response)

@app.route('/api/categories', methods=['GET'])
def get_categories() -> Dict[str, Any]:
    """Endpoint per ottenere tutte le categorie disponibili"""
    with error_handler():
        # Ottieni le categorie dal categorizzatore
        categories = categorizer.category_tree
        
        # Prepara la risposta
        response = {
            "categories": categories,
            "language": "it"
        }
        
        return jsonify(response)

@app.route('/api/seo/keywords', methods=['POST'])
@limiter.limit("20 per minute")
def generate_seo_keywords() -> Dict[str, Any]:
    """Endpoint per generare parole chiave SEO per un prodotto"""
    with error_handler():
        # Ottieni i dati dalla richiesta
        data = request.get_json()
        if not data:
            raise InvalidInputError("Nessun dato JSON fornito")
        
        # Sanitizza l'input
        category = bleach.clean(data.get('category', ''))
        subcategory = bleach.clean(data.get('subcategory', ''))
        product_terms = [bleach.clean(term) for term in data.get('product_terms', [])]
        
        if not category or not product_terms:
            raise InvalidInputError("Categoria e termini di prodotto sono obbligatori")
        
        # Importa la funzione di generazione delle parole chiave
        from src.italian_support import generate_italian_seo_keywords
        
        # Genera le parole chiave SEO
        keywords = generate_italian_seo_keywords(category, subcategory, product_terms)
        
        # Prepara la risposta
        response = {
            "category": category,
            "subcategory": subcategory,
            "product_terms": product_terms,
            "keywords": keywords,
            "language": "it"
        }
        
        return jsonify(response)

@app.route('/api/analyze/title', methods=['POST'])
@limiter.limit("20 per minute")
def analyze_title() -> Dict[str, Any]:
    """Endpoint per analizzare un titolo di prodotto"""
    with error_handler():
        # Ottieni i dati dalla richiesta
        data = request.get_json()
        if not data:
            raise InvalidInputError("Nessun dato JSON fornito")
        
        # Sanitizza l'input
        title = bleach.clean(data.get('title', ''))
        
        if not title:
            raise InvalidInputError("Il titolo è obbligatorio")
        
        # Importa la funzione di analisi del titolo
        from src.italian_support import analyze_italian_product_title
        
        # Analizza il titolo
        analysis = analyze_italian_product_title(title)
        
        # Prepara la risposta
        response = {
            "title": title,
            "analysis": analysis,
            "language": "it"
        }
        
        return jsonify(response)

# Funzione per avviare l'applicazione
def run_app(host: str = "0.0.0.0", port: int = 5000, debug: bool = False) -> None:
    """Avvia l'applicazione Flask"""
    app.run(host=host, port=port, debug=debug)

# Esegui l'applicazione se il modulo viene eseguito direttamente
if __name__ == "__main__":
    # Ottieni le configurazioni dall'ambiente o usa i valori predefiniti
    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", 5000))
    debug = os.environ.get("API_DEBUG", "False").lower() == "true"
    
    # Avvia l'applicazione
    run_app(host, port, debug)