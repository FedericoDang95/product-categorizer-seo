import re
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import unicodedata

@dataclass
class ProductAnalysis:
    """Risultato dell'analisi semantica di un prodotto"""
    product_type: str
    brand: Optional[str]
    model: Optional[str]
    main_function: str
    compatibility: List[str]
    seo_keywords: List[str]
    confidence_score: float

@dataclass
class CategoryResult:
    """Risultato della categorizzazione"""
    categoria_principale: str
    sottocategoria: str
    tags_seo: List[str]
    nuovo_albero: Dict[str, Any]
    confidence_score: float
    is_new_category: bool

class ProductCategorizer:
    """Sistema di categorizzazione automatica dei prodotti con ottimizzazione SEO"""
    
    def __init__(self):
        self.category_tree = {}
        self.seo_keywords_db = self._load_seo_keywords()
        self.brand_patterns = self._load_brand_patterns()
        self.product_type_patterns = self._load_product_type_patterns()
        
    def _load_seo_keywords(self) -> Dict[str, List[str]]:
        """Carica database di parole chiave SEO per categoria"""
        return {
            "ricambi_auto": ["ricambi", "auto", "automobile", "veicolo", "macchina", "car", "parts"],
            "freni": ["freno", "freni", "brake", "brakes", "frenata", "frenante"],
            "motore": ["motore", "engine", "motor", "cilindro", "pistoni", "valvole"],
            "elettronica": ["elettronica", "electronic", "sensore", "centralina", "ecu"],
            "carrozzeria": ["carrozzeria", "body", "paraurti", "cofano", "portiera"],
            "pneumatici": ["pneumatico", "gomma", "tire", "ruota", "cerchio"]
        }
    
    def _load_brand_patterns(self) -> List[str]:
        """Pattern per riconoscimento brand automobilistici"""
        return [
            r'\b(BMW|Mercedes|Audi|Volkswagen|Ford|Fiat|Alfa Romeo|Ferrari|Lamborghini)\b',
            r'\b(Toyota|Honda|Nissan|Mazda|Subaru|Mitsubishi)\b',
            r'\b(Peugeot|Citroën|Renault|Opel|Seat|Skoda)\b',
            r'\b(Volvo|Saab|Porsche|Bentley|Rolls Royce)\b'
        ]
    
    def _load_product_type_patterns(self) -> Dict[str, List[str]]:
        """Pattern per riconoscimento tipologie di prodotto"""
        return {
            "pastiglie_freno": [r'pastigli[ae]', r'brake pad', r'pad freno'],
            "dischi_freno": [r'dischi? freno', r'brake disc', r'rotore'],
            "filtri": [r'filtro', r'filter', r'filtrante'],
            "olio": [r'olio', r'oil', r'lubrificante'],
            "candele": [r'candel[ae]', r'spark plug', r'accensione'],
            "ammortizzatori": [r'ammortizzator[ei]', r'shock absorber', r'sospension[ei]']
        }
    
    def analyze_product(self, title: str, description: str) -> ProductAnalysis:
        """Analizza semanticamente titolo e descrizione del prodotto"""
        text = f"{title} {description}".lower()
        
        # Normalizza il testo
        text = self._normalize_text(text)
        
        # Estrai informazioni
        product_type = self._extract_product_type(text)
        brand = self._extract_brand(text)
        model = self._extract_model(text)
        main_function = self._extract_main_function(text)
        compatibility = self._extract_compatibility(text)
        seo_keywords = self._extract_seo_keywords(text)
        
        # Calcola confidence score
        confidence = self._calculate_confidence(product_type, brand, main_function)
        
        return ProductAnalysis(
            product_type=product_type,
            brand=brand,
            model=model,
            main_function=main_function,
            compatibility=compatibility,
            seo_keywords=seo_keywords,
            confidence_score=confidence
        )
    
    def categorize_product(self, title: str, description: str, 
                          current_tree: Dict[str, Any] = None,
                          target_seo_keywords: List[str] = None) -> CategoryResult:
        """Categorizza automaticamente il prodotto"""
        if current_tree:
            self.category_tree = current_tree
        
        # Analizza il prodotto
        analysis = self.analyze_product(title, description)
        
        # Trova o crea categoria appropriata
        category_path = self._find_or_create_category(analysis, target_seo_keywords)
        
        # Aggiorna albero categorie
        updated_tree = self._update_category_tree(category_path)
        
        # Genera tags SEO
        seo_tags = self._generate_seo_tags(analysis, target_seo_keywords)
        
        return CategoryResult(
            categoria_principale=category_path[0],
            sottocategoria=" > ".join(category_path[1:]) if len(category_path) > 1 else "",
            tags_seo=seo_tags,
            nuovo_albero=updated_tree,
            confidence_score=analysis.confidence_score,
            is_new_category=self._is_new_category(category_path)
        )
    
    def _normalize_text(self, text: str) -> str:
        """Normalizza il testo rimuovendo accenti e caratteri speciali"""
        # Rimuovi accenti
        text = unicodedata.normalize('NFD', text)
        text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
        
        # Rimuovi caratteri speciali
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Normalizza spazi
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _extract_product_type(self, text: str) -> str:
        """Estrae la tipologia di prodotto dal testo"""
        for product_type, patterns in self.product_type_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return product_type.replace('_', ' ').title()
        
        # Fallback: cerca parole chiave generiche
        if any(word in text for word in ['ricambi', 'parts', 'componenti']):
            return "Ricambi Generici"
        
        return "Prodotto Generico"
    
    def _extract_brand(self, text: str) -> Optional[str]:
        """Estrae il brand dal testo"""
        for pattern in self.brand_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        return None
    
    def _extract_model(self, text: str) -> Optional[str]:
        """Estrae il modello dal testo"""
        # Pattern per modelli comuni
        model_patterns = [
            r'\b([A-Z]\d{2,4}[A-Z]?)\b',  # Es: A4, X5, 320i
            r'\b(\d{3,4}[A-Z]{0,2})\b',   # Es: 320i, 500L
            r'\b([A-Z]{2,}\s?\d+)\b'      # Es: Golf 7, Punto Evo
        ]
        
        for pattern in model_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None
    
    def _extract_main_function(self, text: str) -> str:
        """Estrae la funzione principale del prodotto"""
        function_keywords = {
            "frenata": ["freno", "frenata", "brake", "stop"],
            "filtrazione": ["filtro", "filter", "filtraggio"],
            "lubrificazione": ["olio", "oil", "lubrificante"],
            "accensione": ["candela", "spark", "accensione"],
            "sospensione": ["ammortizzatore", "shock", "sospensione"]
        }
        
        for function, keywords in function_keywords.items():
            if any(keyword in text for keyword in keywords):
                return function.title()
        
        return "Funzione Generica"
    
    def _extract_compatibility(self, text: str) -> List[str]:
        """Estrae informazioni di compatibilità"""
        compatibility = []
        
        # Pattern per anni
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        if years:
            compatibility.extend([f"Anno {year}" for year in years])
        
        # Pattern per cilindrata
        engine_pattern = r'\b(\d+\.\d+)\s?(l|litri?)\b'
        engines = re.findall(engine_pattern, text, re.IGNORECASE)
        if engines:
            compatibility.extend([f"{engine[0]}L" for engine in engines])
        
        return compatibility
    
    def _extract_seo_keywords(self, text: str) -> List[str]:
        """Estrae parole chiave SEO rilevanti"""
        keywords = set()
        
        for category, category_keywords in self.seo_keywords_db.items():
            for keyword in category_keywords:
                if keyword in text:
                    keywords.add(keyword)
        
        return list(keywords)
    
    def _calculate_confidence(self, product_type: str, brand: Optional[str], 
                            main_function: str) -> float:
        """Calcola il punteggio di confidenza dell'analisi"""
        score = 0.0
        
        if product_type != "Prodotto Generico":
            score += 0.4
        
        if brand:
            score += 0.3
        
        if main_function != "Funzione Generica":
            score += 0.3
        
        return min(score, 1.0)
    
    def _find_or_create_category(self, analysis: ProductAnalysis, 
                               target_seo_keywords: List[str] = None) -> List[str]:
        """Trova o crea la categoria appropriata"""
        # Logica di categorizzazione basata sull'analisi
        if "freno" in analysis.main_function.lower() or "brake" in analysis.seo_keywords:
            if "pastiglie" in analysis.product_type.lower():
                return ["Ricambi Auto", "Freni", "Pastiglie"]
            elif "dischi" in analysis.product_type.lower():
                return ["Ricambi Auto", "Freni", "Dischi"]
            else:
                return ["Ricambi Auto", "Freni"]
        
        elif "filtro" in analysis.product_type.lower():
            return ["Ricambi Auto", "Filtri"]
        
        elif "olio" in analysis.product_type.lower():
            return ["Ricambi Auto", "Lubrificanti", "Oli Motore"]
        
        elif "candela" in analysis.product_type.lower():
            return ["Ricambi Auto", "Motore", "Accensione"]
        
        elif "ammortizzatore" in analysis.product_type.lower():
            return ["Ricambi Auto", "Sospensioni"]
        
        # Categoria di fallback
        return ["Ricambi Auto", "Altri Componenti"]
    
    def _update_category_tree(self, category_path: List[str]) -> Dict[str, Any]:
        """Aggiorna l'albero delle categorie"""
        current = self.category_tree
        
        for category in category_path:
            if category not in current:
                current[category] = {}
            current = current[category]
        
        return self.category_tree
    
    def _generate_seo_tags(self, analysis: ProductAnalysis, 
                          target_seo_keywords: List[str] = None) -> List[str]:
        """Genera tag SEO ottimizzati"""
        tags = set()
        
        # Aggiungi keywords dall'analisi
        tags.update(analysis.seo_keywords)
        
        # Aggiungi tipo prodotto
        if analysis.product_type:
            tags.add(analysis.product_type.lower())
        
        # Aggiungi brand se presente
        if analysis.brand:
            tags.add(analysis.brand.lower())
        
        # Aggiungi funzione principale
        if analysis.main_function:
            tags.add(analysis.main_function.lower())
        
        # Aggiungi target keywords se fornite
        if target_seo_keywords:
            tags.update([kw.lower() for kw in target_seo_keywords])
        
        # Rimuovi duplicati e ordina per rilevanza
        return sorted(list(tags))
    
    def _is_new_category(self, category_path: List[str]) -> bool:
        """Verifica se la categoria è stata creata ex novo"""
        current = self.category_tree
        
        for category in category_path:
            if category not in current:
                return True
            current = current[category]
        
        return False
    
    def get_category_suggestions(self, partial_analysis: ProductAnalysis, 
                               max_suggestions: int = 5) -> List[Tuple[List[str], float]]:
        """Suggerisce categorie alternative con punteggi di confidenza"""
        suggestions = []
        
        # Implementa logica per suggerimenti alternativi
        # Questo è un esempio semplificato
        base_categories = [
            ["Ricambi Auto", "Freni"],
            ["Ricambi Auto", "Motore"],
            ["Ricambi Auto", "Elettronica"],
            ["Ricambi Auto", "Carrozzeria"],
            ["Ricambi Auto", "Pneumatici"]
        ]
        
        for category in base_categories:
            score = self._calculate_category_score(partial_analysis, category)
            suggestions.append((category, score))
        
        # Ordina per punteggio e restituisci i migliori
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:max_suggestions]
    
    def _calculate_category_score(self, analysis: ProductAnalysis, 
                                category_path: List[str]) -> float:
        """Calcola il punteggio di affinità tra prodotto e categoria"""
        score = 0.0
        
        # Logica semplificata per il calcolo del punteggio
        category_text = " ".join(category_path).lower()
        
        if analysis.main_function.lower() in category_text:
            score += 0.5
        
        if analysis.product_type.lower() in category_text:
            score += 0.3
        
        # Aggiungi altri fattori di scoring
        
        return min(score, 1.0)