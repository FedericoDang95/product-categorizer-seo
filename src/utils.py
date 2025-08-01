import re
import json
import hashlib
import unicodedata
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
import logging
from functools import wraps
import time

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessor:
    """Utilità per il processamento del testo"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Pulisce e normalizza il testo"""
        if not text:
            return ""
        
        # Rimuovi caratteri di controllo
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C')
        
        # Normalizza unicode
        text = unicodedata.normalize('NFKD', text)
        
        # Rimuovi spazi multipli
        text = re.sub(r'\s+', ' ', text)
        
        # Trim
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3, max_keywords: int = 20) -> List[str]:
        """Estrae keywords dal testo"""
        if not text:
            return []
        
        # Converti in minuscolo e pulisci
        text = TextProcessor.clean_text(text.lower())
        
        # Estrai parole alfanumeriche
        words = re.findall(r'\b[a-zA-Z0-9àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]+\b', text)
        
        # Filtra per lunghezza
        keywords = [word for word in words if len(word) >= min_length]
        
        # Rimuovi duplicati mantenendo l'ordine
        seen = set()
        unique_keywords = []
        for keyword in keywords:
            if keyword not in seen:
                seen.add(keyword)
                unique_keywords.append(keyword)
        
        return unique_keywords[:max_keywords]
    
    @staticmethod
    def extract_brands(text: str, brand_list: List[str]) -> List[str]:
        """Estrae brand dal testo"""
        if not text or not brand_list:
            return []
        
        text_lower = text.lower()
        found_brands = []
        
        for brand in brand_list:
            if brand.lower() in text_lower:
                found_brands.append(brand)
        
        return found_brands
    
    @staticmethod
    def extract_model_year(text: str) -> Optional[int]:
        """Estrae l'anno del modello dal testo"""
        # Cerca pattern di anni (1900-2030)
        year_pattern = r'\b(19[0-9]{2}|20[0-3][0-9])\b'
        matches = re.findall(year_pattern, text)
        
        if matches:
            # Restituisci l'anno più recente
            years = [int(year) for year in matches]
            return max(years)
        
        return None
    
    @staticmethod
    def similarity_score(text1: str, text2: str) -> float:
        """Calcola similarità tra due testi usando Jaccard"""
        if not text1 or not text2:
            return 0.0
        
        # Estrai keywords
        keywords1 = set(TextProcessor.extract_keywords(text1))
        keywords2 = set(TextProcessor.extract_keywords(text2))
        
        if not keywords1 or not keywords2:
            return 0.0
        
        # Calcola Jaccard similarity
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))
        
        return intersection / union if union > 0 else 0.0

class CategoryUtils:
    """Utilità per la gestione delle categorie"""
    
    @staticmethod
    def normalize_category_name(name: str) -> str:
        """Normalizza il nome di una categoria"""
        if not name:
            return ""
        
        # Pulisci il testo
        name = TextProcessor.clean_text(name)
        
        # Capitalizza ogni parola
        name = ' '.join(word.capitalize() for word in name.split())
        
        # Rimuovi caratteri speciali eccetto spazi e trattini
        name = re.sub(r'[^a-zA-Z0-9\s\-àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]', '', name)
        
        return name.strip()
    
    @staticmethod
    def build_category_path(categories: List[str]) -> str:
        """Costruisce il path di una categoria"""
        if not categories:
            return ""
        
        normalized = [CategoryUtils.normalize_category_name(cat) for cat in categories]
        return " > ".join(normalized)
    
    @staticmethod
    def parse_category_path(path: str) -> List[str]:
        """Parsifica un path di categoria"""
        if not path:
            return []
        
        categories = [cat.strip() for cat in path.split('>')]
        return [cat for cat in categories if cat]
    
    @staticmethod
    def get_category_depth(category_tree: Dict, path: List[str]) -> int:
        """Calcola la profondità di una categoria nell'albero"""
        if not path:
            return 0
        
        current = category_tree
        depth = 0
        
        for category in path:
            if category in current:
                current = current[category]
                depth += 1
            else:
                break
        
        return depth
    
    @staticmethod
    def find_similar_categories(target_category: str, category_tree: Dict, 
                              threshold: float = 0.7) -> List[Tuple[List[str], float]]:
        """Trova categorie simili nell'albero"""
        similar_categories = []
        
        def traverse_tree(tree: Dict, path: List[str] = []):
            for category, subtree in tree.items():
                current_path = path + [category]
                
                # Calcola similarità
                similarity = TextProcessor.similarity_score(target_category, category)
                
                if similarity >= threshold:
                    similar_categories.append((current_path, similarity))
                
                # Continua la ricerca nei sottoalberi
                if isinstance(subtree, dict):
                    traverse_tree(subtree, current_path)
        
        traverse_tree(category_tree)
        
        # Ordina per similarità decrescente
        similar_categories.sort(key=lambda x: x[1], reverse=True)
        
        return similar_categories
    
    @staticmethod
    def merge_category_trees(tree1: Dict, tree2: Dict) -> Dict:
        """Unisce due alberi di categorie"""
        merged = tree1.copy()
        
        def merge_recursive(target: Dict, source: Dict):
            for key, value in source.items():
                if key in target:
                    if isinstance(target[key], dict) and isinstance(value, dict):
                        merge_recursive(target[key], value)
                else:
                    target[key] = value
        
        merge_recursive(merged, tree2)
        return merged

class ValidationUtils:
    """Utilità per la validazione"""
    
    @staticmethod
    def validate_product_data(data: Dict) -> Tuple[bool, List[str]]:
        """Valida i dati di un prodotto"""
        errors = []
        
        # Campi obbligatori
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Campo obbligatorio mancante: {field}")
        
        # Validazione titolo
        if 'title' in data:
            title = data['title']
            if len(title) < 10:
                errors.append("Il titolo deve essere di almeno 10 caratteri")
            elif len(title) > 200:
                errors.append("Il titolo non può superare i 200 caratteri")
        
        # Validazione descrizione
        if 'description' in data:
            description = data['description']
            if len(description) < 50:
                errors.append("La descrizione deve essere di almeno 50 caratteri")
            elif len(description) > 2000:
                errors.append("La descrizione non può superare i 2000 caratteri")
        
        # Validazione keywords
        if 'keywords' in data and data['keywords']:
            keywords = data['keywords']
            if not isinstance(keywords, list):
                errors.append("Le keywords devono essere una lista")
            elif len(keywords) > 20:
                errors.append("Non più di 20 keywords sono consentite")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_category_tree(tree: Dict, max_depth: int = 4) -> Tuple[bool, List[str]]:
        """Valida un albero di categorie"""
        errors = []
        
        def validate_recursive(subtree: Dict, current_depth: int = 0, path: List[str] = []):
            if current_depth > max_depth:
                errors.append(f"Profondità massima superata nel path: {' > '.join(path)}")
                return
            
            for category, subcategories in subtree.items():
                # Valida nome categoria
                if not category or not isinstance(category, str):
                    errors.append(f"Nome categoria non valido: {category}")
                    continue
                
                if len(category) < 3 or len(category) > 50:
                    errors.append(f"Nome categoria deve essere tra 3 e 50 caratteri: {category}")
                
                # Valida caratteri
                if not re.match(r'^[a-zA-Z0-9\s\-_àèéìíîòóùúÀÈÉÌÍÎÒÓÙÚ]+$', category):
                    errors.append(f"Nome categoria contiene caratteri non validi: {category}")
                
                # Continua validazione ricorsiva
                if isinstance(subcategories, dict):
                    validate_recursive(subcategories, current_depth + 1, path + [category])
        
        validate_recursive(tree)
        return len(errors) == 0, errors

class CacheUtils:
    """Utilità per il caching"""
    
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        self.cache = {}
        self.timestamps = {}
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Genera una chiave di cache"""
        key_data = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, key: str) -> bool:
        """Verifica se una chiave è scaduta"""
        if key not in self.timestamps:
            return True
        
        age = datetime.now() - self.timestamps[key]
        return age.total_seconds() > self.ttl_seconds
    
    def _cleanup_expired(self):
        """Rimuove le chiavi scadute"""
        expired_keys = [key for key in self.cache.keys() if self._is_expired(key)]
        for key in expired_keys:
            del self.cache[key]
            del self.timestamps[key]
    
    def _enforce_size_limit(self):
        """Applica il limite di dimensione della cache"""
        if len(self.cache) <= self.max_size:
            return
        
        # Rimuovi le chiavi più vecchie
        sorted_keys = sorted(self.timestamps.items(), key=lambda x: x[1])
        keys_to_remove = sorted_keys[:len(self.cache) - self.max_size]
        
        for key, _ in keys_to_remove:
            del self.cache[key]
            del self.timestamps[key]
    
    def get(self, key: str) -> Optional[Any]:
        """Recupera un valore dalla cache"""
        if key in self.cache and not self._is_expired(key):
            return self.cache[key]
        return None
    
    def set(self, key: str, value: Any):
        """Imposta un valore nella cache"""
        self._cleanup_expired()
        self._enforce_size_limit()
        
        self.cache[key] = value
        self.timestamps[key] = datetime.now()
    
    def clear(self):
        """Svuota la cache"""
        self.cache.clear()
        self.timestamps.clear()
    
    def cached(self, ttl: Optional[int] = None):
        """Decorator per il caching automatico"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Genera chiave di cache
                cache_key = self._generate_key(func.__name__, *args, **kwargs)
                
                # Controlla se il risultato è in cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Esegui la funzione e salva il risultato
                result = func(*args, **kwargs)
                self.set(cache_key, result)
                
                return result
            return wrapper
        return decorator

class PerformanceUtils:
    """Utilità per il monitoraggio delle performance"""
    
    @staticmethod
    def timing_decorator(func):
        """Decorator per misurare il tempo di esecuzione"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
            
            return result
        return wrapper
    
    @staticmethod
    def memory_usage():
        """Restituisce l'uso della memoria (se psutil è disponibile)"""
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            return {
                'rss': memory_info.rss / 1024 / 1024,  # MB
                'vms': memory_info.vms / 1024 / 1024   # MB
            }
        except ImportError:
            return {'rss': 0, 'vms': 0}

class JSONUtils:
    """Utilità per la gestione JSON"""
    
    @staticmethod
    def safe_json_loads(json_str: str, default: Any = None) -> Any:
        """Carica JSON in modo sicuro"""
        try:
            return json.loads(json_str)
        except (json.JSONDecodeError, TypeError):
            return default
    
    @staticmethod
    def safe_json_dumps(obj: Any, default: str = "{}") -> str:
        """Serializza JSON in modo sicuro"""
        try:
            return json.dumps(obj, ensure_ascii=False, indent=2)
        except (TypeError, ValueError):
            return default
    
    @staticmethod
    def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
        """Unisce due dizionari in profondità"""
        result = dict1.copy()
        
        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JSONUtils.deep_merge(result[key], value)
            else:
                result[key] = value
        
        return result

# Istanze globali per utilità comuni
text_processor = TextProcessor()
category_utils = CategoryUtils()
validation_utils = ValidationUtils()
cache_utils = CacheUtils()
performance_utils = PerformanceUtils()
json_utils = JSONUtils()

# Funzioni di convenienza
def clean_text(text: str) -> str:
    return text_processor.clean_text(text)

def extract_keywords(text: str, **kwargs) -> List[str]:
    return text_processor.extract_keywords(text, **kwargs)

def normalize_category_name(name: str) -> str:
    return category_utils.normalize_category_name(name)

def validate_product_data(data: Dict) -> Tuple[bool, List[str]]:
    return validation_utils.validate_product_data(data)

def timed(func):
    return performance_utils.timing_decorator(func)