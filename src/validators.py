"""Modulo per validazione input con Pydantic"""

from pydantic import BaseModel, validator, Field
from typing import List, Optional, Dict, Any
from enum import Enum
import re

class LanguageCode(str, Enum):
    """Codici lingua supportati"""
    ITALIAN = "it"
    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
    AUTO = "auto"  # Rilevamento automatico

class CategoryDepth(int, Enum):
    """Livelli di profondità categoria"""
    MAIN = 1
    SUB = 2
    DETAIL = 3
    SPECIFIC = 4

class ProductInput(BaseModel):
    """Modello per validazione input prodotto"""
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200,
        description="Titolo del prodotto"
    )
    description: str = Field(
        ..., 
        min_length=10, 
        max_length=2000,
        description="Descrizione dettagliata del prodotto"
    )
    seo_keywords: Optional[List[str]] = Field(
        default=[], 
        max_items=20,
        description="Keywords SEO opzionali"
    )
    language: Optional[LanguageCode] = Field(
        default=LanguageCode.AUTO,
        description="Lingua del contenuto"
    )
    brand: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Brand del prodotto"
    )
    model: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Modello del prodotto"
    )
    price: Optional[float] = Field(
        default=None,
        ge=0,
        description="Prezzo del prodotto"
    )
    
    @validator('title')
    def validate_title(cls, v):
        """Valida e pulisce il titolo"""
        if not v.strip():
            raise ValueError('Titolo non può essere vuoto')
        
        # Rimuovi caratteri speciali pericolosi
        cleaned = re.sub(r'[<>"\'\/\\]', '', v.strip())
        if len(cleaned) < 1:
            raise ValueError('Titolo deve contenere almeno un carattere valido')
        
        return cleaned
    
    @validator('description')
    def validate_description(cls, v):
        """Valida e pulisce la descrizione"""
        if not v.strip():
            raise ValueError('Descrizione non può essere vuota')
        
        # Rimuovi caratteri speciali pericolosi
        cleaned = re.sub(r'[<>"\'\/\\]', '', v.strip())
        if len(cleaned) < 10:
            raise ValueError('Descrizione deve contenere almeno 10 caratteri validi')
        
        return cleaned
    
    @validator('seo_keywords')
    def validate_keywords(cls, v):
        """Valida e pulisce le keywords SEO"""
        if not v:
            return []
        
        cleaned_keywords = []
        for keyword in v:
            if isinstance(keyword, str) and keyword.strip():
                # Pulisci e normalizza
                clean_kw = re.sub(r'[^a-zA-Z0-9\s\-_]', '', keyword.strip().lower())
                if len(clean_kw) >= 2:
                    cleaned_keywords.append(clean_kw)
        
        return list(set(cleaned_keywords))  # Rimuovi duplicati
    
    @validator('brand')
    def validate_brand(cls, v):
        """Valida il brand"""
        if v is None:
            return None
        
        cleaned = re.sub(r'[^a-zA-Z0-9\s\-_]', '', v.strip())
        return cleaned if cleaned else None
    
    @validator('model')
    def validate_model(cls, v):
        """Valida il modello"""
        if v is None:
            return None
        
        cleaned = re.sub(r'[^a-zA-Z0-9\s\-_.]', '', v.strip())
        return cleaned if cleaned else None

class CategoryInput(BaseModel):
    """Modello per validazione categoria"""
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50,
        description="Nome della categoria"
    )
    parent_path: Optional[List[str]] = Field(
        default=[],
        max_items=3,
        description="Percorso categoria padre"
    )
    seo_priority: int = Field(
        default=1, 
        ge=1, 
        le=10,
        description="Priorità SEO (1-10)"
    )
    keywords: Optional[List[str]] = Field(
        default=[],
        max_items=15,
        description="Keywords associate alla categoria"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Descrizione della categoria"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """Valida il nome categoria"""
        if not v.strip():
            raise ValueError('Nome categoria non può essere vuoto')
        
        # Solo caratteri alfanumerici, spazi, trattini
        if not re.match(r'^[a-zA-Z0-9\s\-_àèéìíîòóùúç]+$', v):
            raise ValueError('Nome categoria contiene caratteri non validi')
        
        return v.strip().title()  # Capitalizza
    
    @validator('parent_path')
    def validate_parent_path(cls, v):
        """Valida il percorso padre"""
        if not v:
            return []
        
        # Verifica che ogni elemento sia valido
        cleaned_path = []
        for item in v:
            if isinstance(item, str) and item.strip():
                cleaned_item = re.sub(r'[^a-zA-Z0-9\s\-_àèéìíîòóùúç]', '', item.strip())
                if cleaned_item:
                    cleaned_path.append(cleaned_item.title())
        
        return cleaned_path

class BatchProductInput(BaseModel):
    """Modello per validazione batch di prodotti"""
    products: List[ProductInput] = Field(
        ...,
        min_items=1,
        max_items=100,
        description="Lista di prodotti da categorizzare"
    )
    batch_id: Optional[str] = Field(
        default=None,
        max_length=50,
        description="ID del batch per tracking"
    )
    priority: Optional[int] = Field(
        default=1,
        ge=1,
        le=5,
        description="Priorità elaborazione (1=alta, 5=bassa)"
    )
    
    @validator('batch_id')
    def validate_batch_id(cls, v):
        """Valida l'ID del batch"""
        if v is None:
            return None
        
        # Solo caratteri alfanumerici e trattini
        if not re.match(r'^[a-zA-Z0-9\-_]+$', v):
            raise ValueError('Batch ID può contenere solo caratteri alfanumerici e trattini')
        
        return v

class SEOAnalysisInput(BaseModel):
    """Modello per validazione analisi SEO"""
    text: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Testo da analizzare"
    )
    target_keywords: Optional[List[str]] = Field(
        default=[],
        max_items=10,
        description="Keywords target per l'analisi"
    )
    language: Optional[LanguageCode] = Field(
        default=LanguageCode.AUTO,
        description="Lingua del testo"
    )
    include_trends: bool = Field(
        default=True,
        description="Includi analisi trend"
    )
    
    @validator('text')
    def validate_text(cls, v):
        """Valida il testo per analisi SEO"""
        if not v.strip():
            raise ValueError('Testo non può essere vuoto')
        
        # Rimuovi caratteri di controllo
        cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', v.strip())
        if len(cleaned) < 10:
            raise ValueError('Testo deve contenere almeno 10 caratteri validi')
        
        return cleaned

class CategoryTreeInput(BaseModel):
    """Modello per validazione albero categorie"""
    tree: Dict[str, Any] = Field(
        ...,
        description="Struttura ad albero delle categorie"
    )
    max_depth: Optional[int] = Field(
        default=4,
        ge=1,
        le=6,
        description="Profondità massima dell'albero"
    )
    validate_structure: bool = Field(
        default=True,
        description="Valida la struttura dell'albero"
    )
    
    @validator('tree')
    def validate_tree_structure(cls, v, values):
        """Valida la struttura dell'albero categorie"""
        if not isinstance(v, dict):
            raise ValueError('Tree deve essere un dizionario')
        
        if not v:
            raise ValueError('Tree non può essere vuoto')
        
        # Valida ricorsivamente la struttura
        max_depth = values.get('max_depth', 4)
        
        def validate_node(node, current_depth=1):
            if current_depth > max_depth:
                raise ValueError(f'Profondità albero supera il massimo ({max_depth})')
            
            if isinstance(node, dict):
                for key, value in node.items():
                    if not isinstance(key, str) or not key.strip():
                        raise ValueError('Chiavi categoria devono essere stringhe non vuote')
                    
                    if isinstance(value, dict):
                        validate_node(value, current_depth + 1)
                    elif value is not None:
                        raise ValueError('Valori foglia devono essere None o dizionari')
        
        if values.get('validate_structure', True):
            validate_node(v)
        
        return v

# Funzioni di utilità per validazione
def validate_product_input(data: dict) -> ProductInput:
    """Valida input prodotto e restituisce modello validato"""
    try:
        return ProductInput(**data)
    except Exception as e:
        from .exceptions import ValidationError
        raise ValidationError(f"Errore validazione prodotto: {str(e)}")

def validate_batch_input(data: dict) -> BatchProductInput:
    """Valida input batch e restituisce modello validato"""
    try:
        return BatchProductInput(**data)
    except Exception as e:
        from .exceptions import ValidationError
        raise ValidationError(f"Errore validazione batch: {str(e)}")

def validate_category_input(data: dict) -> CategoryInput:
    """Valida input categoria e restituisce modello validato"""
    try:
        return CategoryInput(**data)
    except Exception as e:
        from .exceptions import ValidationError
        raise ValidationError(f"Errore validazione categoria: {str(e)}")