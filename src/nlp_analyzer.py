import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter
import unicodedata

@dataclass
class EntityRecognitionResult:
    """Risultato del riconoscimento delle entità"""
    brands: List[str]
    models: List[str]
    product_categories: List[str]
    technical_specs: Dict[str, str]
    years: List[int]
    languages_detected: List[str]
    confidence_score: float

class MultilingualNLPAnalyzer:
    """Analizzatore NLP multilingua per il riconoscimento di entità automotive"""
    
    def __init__(self):
        self.brand_database = self._load_brand_database()
        self.category_keywords = self._load_category_keywords()
        self.technical_patterns = self._load_technical_patterns()
        self.language_patterns = self._load_language_patterns()
        self.stopwords = self._load_stopwords()
        
    def _load_brand_database(self) -> Dict[str, Dict[str, List[str]]]:
        """Database completo di brand automobilistici con varianti e modelli"""
        return {
            "luxury": {
                "BMW": ["bmw", "bayerische motoren werke"],
                "Mercedes-Benz": ["mercedes", "benz", "mercedes-benz", "mb"],
                "Audi": ["audi", "quattro"],
                "Porsche": ["porsche"],
                "Ferrari": ["ferrari"],
                "Lamborghini": ["lamborghini", "lambo"],
                "Bentley": ["bentley"],
                "Rolls-Royce": ["rolls royce", "rolls-royce"]
            },
            "mainstream": {
                "Volkswagen": ["volkswagen", "vw", "volks"],
                "Ford": ["ford"],
                "Toyota": ["toyota"],
                "Honda": ["honda"],
                "Nissan": ["nissan"],
                "Hyundai": ["hyundai"],
                "Kia": ["kia"],
                "Mazda": ["mazda"],
                "Subaru": ["subaru"]
            },
            "european": {
                "Fiat": ["fiat"],
                "Alfa Romeo": ["alfa romeo", "alfa", "ar"],
                "Lancia": ["lancia"],
                "Peugeot": ["peugeot"],
                "Citroën": ["citroen", "citroën"],
                "Renault": ["renault"],
                "Opel": ["opel"],
                "Seat": ["seat"],
                "Skoda": ["skoda", "škoda"],
                "Volvo": ["volvo"]
            }
        }
    
    def _load_category_keywords(self) -> Dict[str, Dict[str, List[str]]]:
        """Keywords per categorie di prodotti in multiple lingue"""
        return {
            "freni": {
                "it": ["freno", "freni", "frenata", "frenante", "pastiglie", "dischi", "tamburi"],
                "en": ["brake", "brakes", "braking", "pads", "discs", "rotors", "drums"],
                "de": ["bremse", "bremsen", "bremsscheibe", "bremsbelag"],
                "fr": ["frein", "freins", "freinage", "plaquettes", "disques"],
                "es": ["freno", "frenos", "frenado", "pastillas", "discos"]
            },
            "motore": {
                "it": ["motore", "cilindro", "pistoni", "valvole", "albero", "distribuzione"],
                "en": ["engine", "motor", "cylinder", "pistons", "valves", "camshaft", "timing"],
                "de": ["motor", "zylinder", "kolben", "ventile", "nockenwelle"],
                "fr": ["moteur", "cylindre", "pistons", "soupapes", "arbre à cames"],
                "es": ["motor", "cilindro", "pistones", "válvulas", "árbol de levas"]
            },
            "filtri": {
                "it": ["filtro", "filtri", "filtraggio", "aria", "olio", "carburante"],
                "en": ["filter", "filters", "filtration", "air", "oil", "fuel"],
                "de": ["filter", "luftfilter", "ölfilter", "kraftstofffilter"],
                "fr": ["filtre", "filtres", "filtration", "air", "huile", "carburant"],
                "es": ["filtro", "filtros", "filtración", "aire", "aceite", "combustible"]
            },
            "sospensioni": {
                "it": ["sospensione", "sospensioni", "ammortizzatore", "molla", "barra"],
                "en": ["suspension", "shock", "absorber", "spring", "strut", "damper"],
                "de": ["federung", "stoßdämpfer", "feder", "federbein"],
                "fr": ["suspension", "amortisseur", "ressort", "jambe"],
                "es": ["suspensión", "amortiguador", "muelle", "resorte"]
            },
            "elettronica": {
                "it": ["elettronica", "sensore", "centralina", "ecu", "abs", "esp"],
                "en": ["electronic", "sensor", "ecu", "control unit", "abs", "esp"],
                "de": ["elektronik", "sensor", "steuergerät", "abs", "esp"],
                "fr": ["électronique", "capteur", "calculateur", "abs", "esp"],
                "es": ["electrónica", "sensor", "centralita", "abs", "esp"]
            }
        }
    
    def _load_technical_patterns(self) -> Dict[str, str]:
        """Pattern regex per specifiche tecniche"""
        return {
            "displacement": r'\b(\d+\.\d+)\s?[lL]\b|\b(\d{3,4})\s?cc\b',
            "power": r'\b(\d+)\s?(hp|cv|kw|bhp)\b',
            "year": r'\b(19[5-9]\d|20[0-4]\d)\b',
            "model_code": r'\b([A-Z]\d{2,4}[A-Z]?|\d{3}[A-Z]{1,3})\b',
            "part_number": r'\b([A-Z0-9]{6,15})\b',
            "dimensions": r'\b(\d+)\s?x\s?(\d+)\s?x?\s?(\d+)?\s?(mm|cm)\b'
        }
    
    def _load_language_patterns(self) -> Dict[str, List[str]]:
        """Pattern per il riconoscimento della lingua"""
        return {
            "it": ["per", "con", "auto", "ricambi", "compatibile", "originale"],
            "en": ["for", "with", "car", "parts", "compatible", "original"],
            "de": ["für", "mit", "auto", "teile", "kompatibel", "original"],
            "fr": ["pour", "avec", "auto", "pièces", "compatible", "original"],
            "es": ["para", "con", "auto", "piezas", "compatible", "original"]
        }
    
    def _load_stopwords(self) -> Dict[str, Set[str]]:
        """Stopwords per diverse lingue"""
        return {
            "it": {"il", "la", "di", "da", "in", "con", "per", "su", "come", "più", "anche", "molto"},
            "en": {"the", "of", "to", "and", "a", "in", "is", "it", "you", "that", "he", "was", "for"},
            "de": {"der", "die", "das", "und", "in", "den", "von", "zu", "mit", "sich", "auf", "für"},
            "fr": {"le", "de", "et", "à", "un", "il", "être", "et", "en", "avoir", "que", "pour"},
            "es": {"el", "la", "de", "que", "y", "a", "en", "un", "ser", "se", "no", "te"}
        }
    
    def analyze_entities(self, text: str) -> EntityRecognitionResult:
        """Analizza il testo per estrarre entità automotive"""
        # Normalizza il testo
        normalized_text = self._normalize_text(text)
        
        # Rileva lingue
        languages = self._detect_languages(normalized_text)
        
        # Estrai entità
        brands = self._extract_brands(normalized_text)
        models = self._extract_models(normalized_text)
        categories = self._extract_product_categories(normalized_text, languages)
        technical_specs = self._extract_technical_specs(normalized_text)
        years = self._extract_years(normalized_text)
        
        # Calcola confidence score
        confidence = self._calculate_entity_confidence(
            brands, models, categories, technical_specs, years
        )
        
        return EntityRecognitionResult(
            brands=brands,
            models=models,
            product_categories=categories,
            technical_specs=technical_specs,
            years=years,
            languages_detected=languages,
            confidence_score=confidence
        )
    
    def _normalize_text(self, text: str) -> str:
        """Normalizza il testo per l'analisi"""
        # Converti in lowercase
        text = text.lower()
        
        # Rimuovi accenti ma mantieni caratteri speciali per il riconoscimento lingua
        text = unicodedata.normalize('NFD', text)
        
        # Sostituisci caratteri speciali comuni
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
            'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
            'é': 'e', 'ç': 'c', 'ñ': 'n'
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
        
        return text
    
    def _detect_languages(self, text: str) -> List[str]:
        """Rileva le lingue presenti nel testo"""
        detected_languages = []
        
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for pattern in patterns if pattern in text)
            if score >= 2:  # Soglia minima per considerare una lingua
                detected_languages.append(lang)
        
        # Se nessuna lingua rilevata, assume italiano come default
        if not detected_languages:
            detected_languages = ["it"]
        
        return detected_languages
    
    def _extract_brands(self, text: str) -> List[str]:
        """Estrae brand automobilistici dal testo"""
        found_brands = []
        
        for category, brands in self.brand_database.items():
            for brand, variants in brands.items():
                for variant in variants:
                    if variant in text:
                        if brand not in found_brands:
                            found_brands.append(brand)
                        break
        
        return found_brands
    
    def _extract_models(self, text: str) -> List[str]:
        """Estrae modelli di veicoli dal testo"""
        models = []
        
        # Pattern per modelli comuni
        model_patterns = [
            r'\b([a-z]\d{1,3}[a-z]?)\b',  # Es: a4, x5, 320i
            r'\b(\d{3,4}[a-z]{0,3})\b',   # Es: 320i, 500l
            r'\b([a-z]{2,}\s?\d+)\b',     # Es: golf 7, punto evo
            r'\b([a-z]+\s[a-z]+)\b'       # Es: serie 3, classe a
        ]
        
        for pattern in model_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) > 1 and match not in models:
                    models.append(match)
        
        return models[:5]  # Limita a 5 modelli per evitare rumore
    
    def _extract_product_categories(self, text: str, languages: List[str]) -> List[str]:
        """Estrae categorie di prodotto basate sulle lingue rilevate"""
        categories = []
        
        for category, lang_keywords in self.category_keywords.items():
            for lang in languages:
                if lang in lang_keywords:
                    keywords = lang_keywords[lang]
                    if any(keyword in text for keyword in keywords):
                        if category not in categories:
                            categories.append(category)
        
        return categories
    
    def _extract_technical_specs(self, text: str) -> Dict[str, str]:
        """Estrae specifiche tecniche dal testo"""
        specs = {}
        
        for spec_type, pattern in self.technical_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                if spec_type == "displacement":
                    # Gestisce sia litri che cc
                    for match in matches:
                        if isinstance(match, tuple):
                            value = match[0] if match[0] else match[1]
                        else:
                            value = match
                        if value:
                            specs[spec_type] = value
                            break
                else:
                    specs[spec_type] = matches[0] if isinstance(matches[0], str) else str(matches[0])
        
        return specs
    
    def _extract_years(self, text: str) -> List[int]:
        """Estrae anni dal testo"""
        year_pattern = r'\b(19[5-9]\d|20[0-4]\d)\b'
        matches = re.findall(year_pattern, text)
        return [int(year) for year in matches]
    
    def _calculate_entity_confidence(self, brands: List[str], models: List[str],
                                   categories: List[str], specs: Dict[str, str],
                                   years: List[int]) -> float:
        """Calcola il punteggio di confidenza per le entità estratte"""
        score = 0.0
        
        # Punteggio per brand (peso alto)
        if brands:
            score += 0.3
        
        # Punteggio per categorie (peso alto)
        if categories:
            score += 0.3
        
        # Punteggio per specifiche tecniche
        if specs:
            score += 0.2 * min(len(specs) / 3, 1.0)
        
        # Punteggio per modelli
        if models:
            score += 0.1
        
        # Punteggio per anni
        if years:
            score += 0.1
        
        return min(score, 1.0)
    
    def get_seo_keywords(self, entities: EntityRecognitionResult, 
                        target_language: str = "it") -> List[str]:
        """Genera keywords SEO basate sulle entità estratte"""
        keywords = set()
        
        # Aggiungi brand
        for brand in entities.brands:
            keywords.add(brand.lower())
            keywords.add(f"ricambi {brand.lower()}")
            keywords.add(f"{brand.lower()} parts")
        
        # Aggiungi categorie con traduzione
        for category in entities.product_categories:
            if category in self.category_keywords:
                lang_keywords = self.category_keywords[category]
                if target_language in lang_keywords:
                    keywords.update(lang_keywords[target_language])
        
        # Aggiungi specifiche tecniche
        for spec_type, value in entities.technical_specs.items():
            if spec_type == "displacement":
                keywords.add(f"{value}l")
                keywords.add(f"motore {value}")
            elif spec_type == "year":
                keywords.add(f"anno {value}")
                keywords.add(f"{value} model")
        
        # Aggiungi combinazioni
        if entities.brands and entities.product_categories:
            for brand in entities.brands:
                for category in entities.product_categories:
                    keywords.add(f"{brand.lower()} {category}")
        
        return sorted(list(keywords))
    
    def suggest_category_improvements(self, current_category: str, 
                                    entities: EntityRecognitionResult) -> List[str]:
        """Suggerisce miglioramenti per la categoria corrente"""
        suggestions = []
        
        # Suggerimenti basati su brand
        if entities.brands:
            for brand in entities.brands:
                suggestions.append(f"{current_category} > {brand}")
        
        # Suggerimenti basati su specifiche tecniche
        if "displacement" in entities.technical_specs:
            displacement = entities.technical_specs["displacement"]
            suggestions.append(f"{current_category} > {displacement}L")
        
        # Suggerimenti basati su anni
        if entities.years:
            year_ranges = self._group_years(entities.years)
            for year_range in year_ranges:
                suggestions.append(f"{current_category} > {year_range}")
        
        return suggestions[:3]  # Limita a 3 suggerimenti
    
    def _group_years(self, years: List[int]) -> List[str]:
        """Raggruppa anni in range logici"""
        if not years:
            return []
        
        years = sorted(set(years))
        ranges = []
        
        if len(years) == 1:
            return [str(years[0])]
        
        # Crea range per decenni
        decades = {}
        for year in years:
            decade = (year // 10) * 10
            if decade not in decades:
                decades[decade] = []
            decades[decade].append(year)
        
        for decade, decade_years in decades.items():
            if len(decade_years) > 1:
                ranges.append(f"{min(decade_years)}-{max(decade_years)}")
            else:
                ranges.append(str(decade_years[0]))
        
        return ranges