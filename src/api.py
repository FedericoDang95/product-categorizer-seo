from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import logging
from typing import Dict, Any
import bleach
from contextlib import contextmanager

from product_categorizer import ProductCategorizer, CategoryResult
from exceptions import (
    ProductCategorizerError, InvalidInputError, ValidationError,
    RateLimitError, CategoryNotFoundError
)
from validators import (
    ProductInput, BatchProductInput, CategoryInput, SEOAnalysisInput,
    validate_product_input, validate_batch_input
)

# Configurazione logging strutturato
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le route

# Configurazione rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configurazione sicurezza
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Inizializza il categorizzatore
categorizer = ProductCategorizer()

@contextmanager
def error_handler(operation: str):
    """Context manager per gestione errori centralizzata"""
    try:
        yield
    except ProductCategorizerError:
        # Re-raise errori specifici del sistema
        raise
    except Exception as e:
        logger.error(f"Errore imprevisto durante {operation}: {str(e)}")
        raise ProductCategorizerError(f"Errore interno durante {operation}") from e

def sanitize_input(text: str, max_length: int = None) -> str:
    """Sanitizza input utente"""
    if not text:
        return ""
    
    # Rimuovi tag HTML e caratteri pericolosi
    cleaned = bleach.clean(text, strip=True)
    
    # Limita lunghezza se specificata
    if max_length and len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned.strip()

@app.errorhandler(ProductCategorizerError)
def handle_categorizer_error(error):
    """Gestisce errori specifici del categorizzatore"""
    logger.warning(f"Errore categorizzatore: {error.message}")
    return jsonify({
        'error': error.message,
        'error_code': error.error_code,
        'details': error.details,
        'status': 'error'
    }), 400

@app.errorhandler(ValidationError)
def handle_validation_error(error):
    """Gestisce errori di validazione"""
    logger.warning(f"Errore validazione: {error.message}")
    return jsonify({
        'error': 'Dati di input non validi',
        'error_code': 'VALIDATION_ERROR',
        'details': error.details,
        'status': 'error'
    }), 422

@app.errorhandler(429)
def handle_rate_limit(error):
    """Gestisce errori di rate limiting"""
    return jsonify({
        'error': 'Troppi tentativi. Riprova più tardi.',
        'error_code': 'RATE_LIMIT_EXCEEDED',
        'status': 'error'
    }), 429

@app.errorhandler(413)
def handle_large_payload(error):
    """Gestisce payload troppo grandi"""
    return jsonify({
        'error': 'Payload troppo grande. Massimo 16MB.',
        'error_code': 'PAYLOAD_TOO_LARGE',
        'status': 'error'
    }), 413

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint per verificare lo stato del servizio"""
    return jsonify({
        'status': 'healthy',
        'service': 'Product Categorizer SEO',
        'version': '1.0.0'
    })

@app.route('/categorize', methods=['POST'])
@limiter.limit("10 per minute")
def categorize_product():
    """Endpoint principale per la categorizzazione dei prodotti"""
    with error_handler("categorizzazione prodotto"):
        data = request.get_json()
        
        if not data:
            raise InvalidInputError("Nessun dato JSON fornito")
        
        # Valida input usando Pydantic
        validated_input = validate_product_input(data)
        
        # Sanitizza input
        title = sanitize_input(validated_input.get('titolo', ''), 200)
        description = sanitize_input(validated_input.get('descrizione', ''), 2000)
        
        if not title and not description:
            raise InvalidInputError("Titolo o descrizione richiesti")
        
        logger.info(f"Categorizzazione richiesta per: {title[:50]}...")
        
        # Parametri opzionali
        current_tree = validated_input.get('albero_categorie', {})
        target_seo_keywords = validated_input.get('parole_chiave_seo', [])
        
        # Esegui categorizzazione
        result = categorizer.categorize_product(
            title=title,
            description=description,
            current_tree=current_tree,
            target_seo_keywords=target_seo_keywords
        )
        
        if not result:
            raise CategoryNotFoundError("Impossibile determinare una categoria adatta")
        
        # Prepara risposta
        response = {
            'categoria_principale': result.categoria_principale,
            'sottocategoria': result.sottocategoria,
            'tags_seo': result.tags_seo,
            'nuovo_albero': result.nuovo_albero,
            'confidence_score': result.confidence_score,
            'is_new_category': result.is_new_category,
            'status': 'success',
            'processing_time': getattr(result, 'processing_time', None)
        }
        
        logger.info(f"Categorizzazione completata: {result.categoria_principale}")
        return jsonify(response)

@app.route('/analyze', methods=['POST'])
def analyze_product():
    """Endpoint per l'analisi semantica del prodotto senza categorizzazione"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Nessun dato JSON fornito',
                'status': 'error'
            }), 400
        
        title = data.get('titolo', '')
        description = data.get('descrizione', '')
        
        if not title and not description:
            return jsonify({
                'error': 'Titolo o descrizione richiesti',
                'status': 'error'
            }), 400
        
        # Esegui analisi
        analysis = categorizer.analyze_product(title, description)
        
        response = {
            'product_type': analysis.product_type,
            'brand': analysis.brand,
            'model': analysis.model,
            'main_function': analysis.main_function,
            'compatibility': analysis.compatibility,
            'seo_keywords': analysis.seo_keywords,
            'confidence_score': analysis.confidence_score,
            'status': 'success'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Errore durante l'analisi: {str(e)}")
        return jsonify({
            'error': f'Errore interno del server: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/suggestions', methods=['POST'])
def get_category_suggestions():
    """Endpoint per ottenere suggerimenti di categoria"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Nessun dato JSON fornito',
                'status': 'error'
            }), 400
        
        title = data.get('titolo', '')
        description = data.get('descrizione', '')
        max_suggestions = data.get('max_suggerimenti', 5)
        
        if not title and not description:
            return jsonify({
                'error': 'Titolo o descrizione richiesti',
                'status': 'error'
            }), 400
        
        # Analizza il prodotto
        analysis = categorizer.analyze_product(title, description)
        
        # Ottieni suggerimenti
        suggestions = categorizer.get_category_suggestions(analysis, max_suggestions)
        
        response = {
            'suggestions': [
                {
                    'category_path': suggestion[0],
                    'confidence_score': suggestion[1],
                    'category_string': ' > '.join(suggestion[0])
                }
                for suggestion in suggestions
            ],
            'analysis': {
                'product_type': analysis.product_type,
                'brand': analysis.brand,
                'main_function': analysis.main_function,
                'confidence_score': analysis.confidence_score
            },
            'status': 'success'
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Errore durante la generazione suggerimenti: {str(e)}")
        return jsonify({
            'error': f'Errore interno del server: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/categories', methods=['GET'])
def get_current_categories():
    """Endpoint per ottenere l'albero delle categorie corrente"""
    try:
        return jsonify({
            'categories': categorizer.category_tree,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Errore nel recupero categorie: {str(e)}")
        return jsonify({
            'error': f'Errore interno del server: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/categories', methods=['POST'])
def update_categories():
    """Endpoint per aggiornare l'albero delle categorie"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Nessun dato JSON fornito',
                'status': 'error'
            }), 400
        
        new_tree = data.get('nuovo_albero', {})
        if not isinstance(new_tree, dict):
            return jsonify({
                'error': 'Formato albero categorie non valido',
                'status': 'error'
            }), 400
        
        # Aggiorna l'albero delle categorie
        categorizer.category_tree = new_tree
        
        return jsonify({
            'message': 'Albero categorie aggiornato con successo',
            'categories': categorizer.category_tree,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Errore nell'aggiornamento categorie: {str(e)}")
        return jsonify({
            'error': f'Errore interno del server: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/batch-categorize', methods=['POST'])
@limiter.limit("5 per minute")
def batch_categorize():
    """Endpoint per la categorizzazione in batch di più prodotti"""
    with error_handler("categorizzazione batch"):
        data = request.get_json()
        
        if not data:
            raise InvalidInputError("Nessun dato fornito")
        
        # Valida input batch usando Pydantic
        validated_batch = validate_batch_input(data)
        
        products = validated_batch.get('prodotti', [])
        batch_id = validated_batch.get('batch_id')
        current_tree = validated_batch.get('albero_categorie', {})
        target_seo_keywords = validated_batch.get('parole_chiave_seo', [])
        
        logger.info(f"Elaborazione batch {batch_id or 'anonimo'} di {len(products)} prodotti")
        
        results = []
        
        for i, product in enumerate(products):
            try:
                # Sanitizza input per ogni prodotto
                title = sanitize_input(product.get('titolo', ''), 200)
                description = sanitize_input(product.get('descrizione', ''), 2000)
                
                if not title and not description:
                    results.append({
                        'index': i,
                        'error': 'Titolo o descrizione richiesti',
                        'status': 'error'
                    })
                    continue
                
                result = categorizer.categorize_product(
                    title=title,
                    description=description,
                    current_tree=current_tree,
                    target_seo_keywords=target_seo_keywords
                )
                
                if result:
                    results.append({
                        'index': i,
                        'product_title': title[:50] + '...' if len(title) > 50 else title,
                        'categoria_principale': result.categoria_principale,
                        'sottocategoria': result.sottocategoria,
                        'tags_seo': result.tags_seo,
                        'confidence_score': result.confidence_score,
                        'is_new_category': result.is_new_category,
                        'status': 'success'
                    })
                    
                    # Aggiorna l'albero per i prodotti successivi
                    current_tree = result.nuovo_albero
                else:
                    results.append({
                        'index': i,
                        'product_title': title[:50] + '...' if len(title) > 50 else title,
                        'error': 'Categoria non determinabile',
                        'status': 'error'
                    })
                
            except Exception as e:
                logger.warning(f"Errore prodotto {i}: {str(e)}")
                results.append({
                    'index': i,
                    'product_title': product.get('titolo', 'N/A')[:50],
                    'error': str(e),
                    'status': 'error'
                })
        
        success_rate = len([r for r in results if r.get('status') == 'success']) / len(products) * 100 if products else 0
        
        response = {
            'results': results,
            'nuovo_albero': categorizer.category_tree,
            'batch_id': batch_id,
            'total_processed': len(products),
            'successful': len([r for r in results if r.get('status') == 'success']),
            'failed': len([r for r in results if r.get('status') == 'error']),
            'success_rate': round(success_rate, 2),
            'status': 'success'
        }
        
        logger.info(f"Batch {batch_id or 'anonimo'} completato: {response['successful']}/{len(products)} successi ({success_rate:.1f}%)")
        return jsonify(response)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint non trovato',
        'status': 'error'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Metodo HTTP non consentito',
        'status': 'error'
    }), 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)