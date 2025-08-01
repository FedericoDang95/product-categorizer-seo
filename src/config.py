import os
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ModelConfig:
    """Configurazione per i modelli di ML/NLP"""
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    similarity_threshold: float = 0.7
    max_category_depth: int = 4
    min_similarity_for_merge: float = 0.85
    language_detection_confidence: float = 0.8

@dataclass
class SEOConfig:
    """Configurazione per l'ottimizzazione SEO"""
    max_keywords_per_category: int = 10
    min_search_volume: int = 100
    max_competition_threshold: float = 0.8
    title_max_length: int = 60
    description_max_length: int = 160
    enable_trend_analysis: bool = True

@dataclass
class APIConfig:
    """Configurazione per l'API Flask"""
    host: str = "localhost"
    port: int = 5000
    debug: bool = True
    cors_enabled: bool = True
    max_content_length: int = 16 * 1024 * 1024  # 16MB
    rate_limit: str = "100 per hour"

@dataclass
class CacheConfig:
    """Configurazione per il caching"""
    enabled: bool = True
    ttl_seconds: int = 3600  # 1 ora
    max_size: int = 1000
    cache_type: str = "memory"  # "memory" o "redis"
    redis_url: Optional[str] = None

class Config:
    """Configurazione principale del sistema"""
    
    def __init__(self):
        self.model = ModelConfig()
        self.seo = SEOConfig()
        self.api = APIConfig()
        self.cache = CacheConfig()
        
        # Carica configurazioni da variabili d'ambiente
        self._load_from_env()
        
        # Configurazioni specifiche per automotive
        self.automotive_config = self._get_automotive_config()
        
        # Configurazioni multilingua
        self.language_config = self._get_language_config()
    
    def _load_from_env(self):
        """Carica configurazioni da variabili d'ambiente"""
        # API Config
        self.api.host = os.getenv("API_HOST", self.api.host)
        self.api.port = int(os.getenv("API_PORT", self.api.port))
        self.api.debug = os.getenv("API_DEBUG", "true").lower() == "true"
        
        # Model Config
        self.model.embedding_model = os.getenv("EMBEDDING_MODEL", self.model.embedding_model)
        self.model.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", self.model.similarity_threshold))
        
        # SEO Config
        self.seo.max_keywords_per_category = int(os.getenv("MAX_KEYWORDS", self.seo.max_keywords_per_category))
        self.seo.min_search_volume = int(os.getenv("MIN_SEARCH_VOLUME", self.seo.min_search_volume))
        
        # Cache Config
        self.cache.enabled = os.getenv("CACHE_ENABLED", "true").lower() == "true"
        self.cache.redis_url = os.getenv("REDIS_URL")
        if self.cache.redis_url:
            self.cache.cache_type = "redis"
    
    def _get_automotive_config(self) -> Dict:
        """Configurazioni specifiche per il settore automotive"""
        return {
            "main_categories": [
                "Ricambi Auto",
                "Accessori Auto",
                "Pneumatici",
                "Oli e Lubrificanti",
                "Batterie",
                "Elettronica Auto",
                "Tuning e Performance",
                "Manutenzione"
            ],
            "brand_keywords": [
                "bmw", "mercedes", "audi", "volkswagen", "fiat", "alfa romeo",
                "ferrari", "lamborghini", "maserati", "lancia", "jeep",
                "ford", "opel", "peugeot", "renault", "citroen", "toyota",
                "honda", "nissan", "mazda", "hyundai", "kia", "volvo",
                "skoda", "seat", "mini", "smart", "porsche", "bentley"
            ],
            "product_types": {
                "motore": ["pistoni", "valvole", "cinghie", "catene", "guarnizioni"],
                "freni": ["pastiglie", "dischi", "tamburi", "pinze", "tubi"],
                "sospensioni": ["ammortizzatori", "molle", "barre", "silent block"],
                "trasmissione": ["frizione", "cambio", "differenziale", "semiassi"],
                "elettrico": ["alternatore", "motorino", "candele", "bobine", "sensori"],
                "carrozzeria": ["paraurti", "cofano", "portiere", "specchietti", "fari"],
                "interni": ["sedili", "volante", "cruscotto", "tappetini", "rivestimenti"]
            },
            "compatibility_keywords": [
                "compatibile", "originale", "aftermarket", "oem", "universale",
                "specifico", "adatto", "ricambio", "sostituzione", "equivalente"
            ],
            "quality_indicators": [
                "premium", "originale", "certificato", "garantito", "testato",
                "professionale", "racing", "performance", "economico", "standard"
            ]
        }
    
    def _get_language_config(self) -> Dict:
        """Configurazioni per il supporto multilingua"""
        return {
            "supported_languages": ["it", "en", "de", "fr", "es"],
            "default_language": "it",
            "language_models": {
                "it": "it_core_news_sm",
                "en": "en_core_web_sm",
                "de": "de_core_news_sm",
                "fr": "fr_core_news_sm",
                "es": "es_core_news_sm"
            },
            "translation_fallback": True,
            "auto_detect_language": True
        }
    
    def get_category_templates(self) -> Dict[str, List[str]]:
        """Template per la generazione automatica di categorie"""
        return {
            "ricambi_motore": [
                "Ricambi Auto > Motore > {component}",
                "Ricambi Auto > Sistema Motore > {component}",
                "Motore > Componenti > {component}"
            ],
            "ricambi_freni": [
                "Ricambi Auto > Freni > {component}",
                "Ricambi Auto > Sistema Frenante > {component}",
                "Freni > Componenti > {component}"
            ],
            "accessori": [
                "Accessori Auto > {category} > {subcategory}",
                "Accessori > {category} > {subcategory}"
            ],
            "elettronica": [
                "Elettronica Auto > {system} > {component}",
                "Ricambi Auto > Elettronica > {system} > {component}"
            ]
        }
    
    def get_seo_templates(self) -> Dict[str, str]:
        """Template per la generazione di contenuti SEO"""
        return {
            "title": "{category} | {keywords} | Ricambi Auto Online",
            "description": "Scopri {category} di qualità. {keywords} per {brands}. Spedizione rapida, prezzi competitivi e garanzia.",
            "h1": "{category} - {keywords}",
            "breadcrumb": "Home > {path} > {category}",
            "alt_text": "{product_name} - {category} per {brand}"
        }
    
    def get_validation_rules(self) -> Dict:
        """Regole di validazione per categorie e prodotti"""
        return {
            "category_name": {
                "min_length": 3,
                "max_length": 50,
                "allowed_chars": r"[a-zA-Z0-9\s\-_àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]",
                "forbidden_words": ["test", "prova", "temp", "xxx"]
            },
            "product_title": {
                "min_length": 10,
                "max_length": 200,
                "required_elements": ["brand_or_category", "product_type"]
            },
            "description": {
                "min_length": 50,
                "max_length": 2000,
                "min_words": 10
            },
            "keywords": {
                "max_count": 20,
                "min_length": 2,
                "max_length": 30
            }
        }
    
    def get_performance_settings(self) -> Dict:
        """Impostazioni per le performance del sistema"""
        return {
            "batch_size": 100,
            "max_concurrent_requests": 10,
            "timeout_seconds": 30,
            "retry_attempts": 3,
            "memory_limit_mb": 512,
            "enable_profiling": self.api.debug,
            "log_level": "DEBUG" if self.api.debug else "INFO"
        }
    
    def validate(self) -> List[str]:
        """Valida la configurazione e restituisce eventuali errori"""
        errors = []
        
        # Valida soglie
        if not 0.0 <= self.model.similarity_threshold <= 1.0:
            errors.append("similarity_threshold deve essere tra 0.0 e 1.0")
        
        if self.model.max_category_depth < 1 or self.model.max_category_depth > 10:
            errors.append("max_category_depth deve essere tra 1 e 10")
        
        if self.seo.min_search_volume < 0:
            errors.append("min_search_volume deve essere >= 0")
        
        if not 0.0 <= self.seo.max_competition_threshold <= 1.0:
            errors.append("max_competition_threshold deve essere tra 0.0 e 1.0")
        
        # Valida porte
        if not 1024 <= self.api.port <= 65535:
            errors.append("port deve essere tra 1024 e 65535")
        
        return errors
    
    def to_dict(self) -> Dict:
        """Converte la configurazione in dizionario"""
        return {
            "model": {
                "embedding_model": self.model.embedding_model,
                "similarity_threshold": self.model.similarity_threshold,
                "max_category_depth": self.model.max_category_depth,
                "min_similarity_for_merge": self.model.min_similarity_for_merge,
                "language_detection_confidence": self.model.language_detection_confidence
            },
            "seo": {
                "max_keywords_per_category": self.seo.max_keywords_per_category,
                "min_search_volume": self.seo.min_search_volume,
                "max_competition_threshold": self.seo.max_competition_threshold,
                "title_max_length": self.seo.title_max_length,
                "description_max_length": self.seo.description_max_length,
                "enable_trend_analysis": self.seo.enable_trend_analysis
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug,
                "cors_enabled": self.api.cors_enabled,
                "max_content_length": self.api.max_content_length,
                "rate_limit": self.api.rate_limit
            },
            "cache": {
                "enabled": self.cache.enabled,
                "ttl_seconds": self.cache.ttl_seconds,
                "max_size": self.cache.max_size,
                "cache_type": self.cache.cache_type,
                "redis_url": self.cache.redis_url
            }
        }

# Istanza globale della configurazione
config = Config()

# Valida la configurazione all'avvio
validation_errors = config.validate()
if validation_errors:
    print("⚠️ Errori di configurazione:")
    for error in validation_errors:
        print(f"  - {error}")
    print("Il sistema potrebbe non funzionare correttamente.")
else:
    print("✅ Configurazione validata con successo")