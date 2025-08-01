"""Modulo per gestione centralizzata delle eccezioni"""

class ProductCategorizerError(Exception):
    """Eccezione base per errori di categorizzazione"""
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GENERAL_ERROR"
        self.details = details or {}

class InvalidInputError(ProductCategorizerError):
    """Errore per input non validi"""
    def __init__(self, message: str, field: str = None, value: str = None):
        super().__init__(message, "INVALID_INPUT")
        self.field = field
        self.value = value
        self.details = {"field": field, "value": value}

class CategoryNotFoundError(ProductCategorizerError):
    """Errore quando non si trova una categoria adatta"""
    def __init__(self, message: str, confidence_score: float = None):
        super().__init__(message, "CATEGORY_NOT_FOUND")
        self.confidence_score = confidence_score
        self.details = {"confidence_score": confidence_score}

class ModelLoadError(ProductCategorizerError):
    """Errore nel caricamento dei modelli ML/NLP"""
    def __init__(self, message: str, model_name: str = None):
        super().__init__(message, "MODEL_LOAD_ERROR")
        self.model_name = model_name
        self.details = {"model_name": model_name}

class SEOAnalysisError(ProductCategorizerError):
    """Errore nell'analisi SEO"""
    def __init__(self, message: str, seo_operation: str = None):
        super().__init__(message, "SEO_ANALYSIS_ERROR")
        self.seo_operation = seo_operation
        self.details = {"seo_operation": seo_operation}

class ValidationError(ProductCategorizerError):
    """Errore di validazione dati"""
    def __init__(self, message: str, validation_errors: list = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.validation_errors = validation_errors or []
        self.details = {"validation_errors": self.validation_errors}

class RateLimitError(ProductCategorizerError):
    """Errore per superamento rate limit"""
    def __init__(self, message: str, retry_after: int = None):
        super().__init__(message, "RATE_LIMIT_EXCEEDED")
        self.retry_after = retry_after
        self.details = {"retry_after": retry_after}

class CacheError(ProductCategorizerError):
    """Errore nelle operazioni di cache"""
    def __init__(self, message: str, cache_operation: str = None):
        super().__init__(message, "CACHE_ERROR")
        self.cache_operation = cache_operation
        self.details = {"cache_operation": cache_operation}

class ConfigurationError(ProductCategorizerError):
    """Errore di configurazione"""
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, "CONFIGURATION_ERROR")
        self.config_key = config_key
        self.details = {"config_key": config_key}