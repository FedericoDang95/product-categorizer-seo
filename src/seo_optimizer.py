import re
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from collections import Counter, defaultdict
import math

@dataclass
class SEOMetrics:
    """Metriche SEO per una categoria o keyword"""
    keyword: str
    search_volume: int
    competition: float  # 0.0 - 1.0
    difficulty: float   # 0.0 - 1.0
    relevance_score: float
    trend: str  # 'rising', 'stable', 'declining'
    
@dataclass
class CategorySEOAnalysis:
    """Analisi SEO completa per una categoria"""
    category_path: List[str]
    primary_keywords: List[SEOMetrics]
    long_tail_keywords: List[SEOMetrics]
    seo_score: float
    optimization_suggestions: List[str]
    competitor_analysis: Dict[str, float]

class SEOOptimizer:
    """Ottimizzatore SEO per categorie di prodotti automotive"""
    
    def __init__(self):
        self.keyword_database = self._load_keyword_database()
        self.search_volume_data = self._load_search_volume_data()
        self.competition_data = self._load_competition_data()
        self.trend_data = self._load_trend_data()
        self.stop_words = self._load_seo_stop_words()
        
    def _load_keyword_database(self) -> Dict[str, Dict[str, any]]:
        """Database di keywords automotive con metriche SEO"""
        return {
            # Categorie principali
            "ricambi auto": {
                "volume": 50000,
                "competition": 0.8,
                "difficulty": 0.7,
                "trend": "stable",
                "related": ["parti auto", "componenti auto", "accessori auto"]
            },
            "freni auto": {
                "volume": 15000,
                "competition": 0.6,
                "difficulty": 0.5,
                "trend": "stable",
                "related": ["brake parts", "sistema frenante", "componenti freno"]
            },
            "pastiglie freno": {
                "volume": 8000,
                "competition": 0.5,
                "difficulty": 0.4,
                "trend": "rising",
                "related": ["brake pads", "ferodo", "pastiglie anteriori"]
            },
            "dischi freno": {
                "volume": 6000,
                "competition": 0.5,
                "difficulty": 0.4,
                "trend": "stable",
                "related": ["brake discs", "rotori", "dischi ventilati"]
            },
            "filtri auto": {
                "volume": 12000,
                "competition": 0.4,
                "difficulty": 0.3,
                "trend": "stable",
                "related": ["filtro aria", "filtro olio", "filtro carburante"]
            },
            "olio motore": {
                "volume": 25000,
                "competition": 0.7,
                "difficulty": 0.6,
                "trend": "stable",
                "related": ["lubrificanti", "olio sintetico", "cambio olio"]
            },
            "ammortizzatori": {
                "volume": 10000,
                "competition": 0.5,
                "difficulty": 0.4,
                "trend": "stable",
                "related": ["shock absorber", "sospensioni", "molle"]
            },
            # Keywords long-tail
            "pastiglie freno anteriori": {
                "volume": 3000,
                "competition": 0.3,
                "difficulty": 0.2,
                "trend": "rising",
                "related": ["front brake pads", "pastiglie davanti"]
            },
            "filtro aria motore": {
                "volume": 4000,
                "competition": 0.3,
                "difficulty": 0.2,
                "trend": "stable",
                "related": ["air filter", "filtro aspirazione"]
            },
            "olio motore 5w30": {
                "volume": 8000,
                "competition": 0.4,
                "difficulty": 0.3,
                "trend": "stable",
                "related": ["5w30 oil", "olio sintetico 5w30"]
            }
        }
    
    def _load_search_volume_data(self) -> Dict[str, int]:
        """Dati di volume di ricerca per keywords automotive"""
        return {
            "auto": 100000,
            "ricambi": 30000,
            "freni": 20000,
            "motore": 40000,
            "filtro": 15000,
            "olio": 35000,
            "pneumatici": 25000,
            "batteria": 18000,
            "candele": 12000,
            "cinghia": 8000,
            "radiatore": 7000,
            "alternatore": 6000,
            "starter": 5000,
            "frizione": 9000,
            "cambio": 11000
        }
    
    def _load_competition_data(self) -> Dict[str, float]:
        """Dati di competizione per keywords (0.0 = bassa, 1.0 = alta)"""
        return {
            "auto": 0.9,
            "ricambi": 0.7,
            "freni": 0.5,
            "motore": 0.8,
            "filtro": 0.4,
            "olio": 0.6,
            "pneumatici": 0.8,
            "batteria": 0.6,
            "candele": 0.4,
            "cinghia": 0.3,
            "radiatore": 0.4,
            "alternatore": 0.3,
            "starter": 0.3,
            "frizione": 0.5,
            "cambio": 0.6
        }
    
    def _load_trend_data(self) -> Dict[str, str]:
        """Dati di trend per keywords"""
        return {
            "elettrico": "rising",
            "ibrido": "rising",
            "sostenibile": "rising",
            "originale": "stable",
            "aftermarket": "stable",
            "performance": "rising",
            "tuning": "stable",
            "racing": "stable",
            "economico": "declining",
            "premium": "rising"
        }
    
    def _load_seo_stop_words(self) -> Set[str]:
        """Stop words da evitare nelle keywords SEO"""
        return {
            "il", "la", "di", "da", "in", "con", "per", "su", "come", "più",
            "the", "of", "to", "and", "a", "in", "is", "it", "you", "that",
            "molto", "tanto", "poco", "alcuni", "tutti", "ogni", "qualche"
        }
    
    def analyze_category_seo(self, category_path: List[str], 
                           product_keywords: List[str] = None) -> CategorySEOAnalysis:
        """Analizza le performance SEO di una categoria"""
        # Genera keywords per la categoria
        primary_keywords = self._generate_primary_keywords(category_path)
        long_tail_keywords = self._generate_long_tail_keywords(category_path, product_keywords)
        
        # Calcola metriche SEO
        primary_metrics = [self._calculate_keyword_metrics(kw) for kw in primary_keywords]
        long_tail_metrics = [self._calculate_keyword_metrics(kw) for kw in long_tail_keywords]
        
        # Calcola punteggio SEO complessivo
        seo_score = self._calculate_category_seo_score(primary_metrics, long_tail_metrics)
        
        # Genera suggerimenti di ottimizzazione
        suggestions = self._generate_optimization_suggestions(
            category_path, primary_metrics, long_tail_metrics
        )
        
        # Analisi competitor (simulata)
        competitor_analysis = self._analyze_competitors(category_path)
        
        return CategorySEOAnalysis(
            category_path=category_path,
            primary_keywords=primary_metrics,
            long_tail_keywords=long_tail_metrics,
            seo_score=seo_score,
            optimization_suggestions=suggestions,
            competitor_analysis=competitor_analysis
        )
    
    def _generate_primary_keywords(self, category_path: List[str]) -> List[str]:
        """Genera keywords primarie per una categoria"""
        keywords = []
        
        # Keyword basate sul path della categoria
        category_text = " ".join(category_path).lower()
        keywords.append(category_text)
        
        # Combinazioni di categorie
        if len(category_path) >= 2:
            keywords.append(f"{category_path[0].lower()} {category_path[-1].lower()}")
        
        # Varianti comuni
        for category in category_path:
            category_lower = category.lower()
            if category_lower in self.keyword_database:
                related = self.keyword_database[category_lower].get("related", [])
                keywords.extend(related[:2])  # Limita a 2 varianti per categoria
        
        return list(set(keywords))[:5]  # Massimo 5 keywords primarie
    
    def _generate_long_tail_keywords(self, category_path: List[str], 
                                   product_keywords: List[str] = None) -> List[str]:
        """Genera keywords long-tail per una categoria"""
        long_tail = []
        
        # Combinazioni con modificatori
        modifiers = [
            "originale", "aftermarket", "compatibile", "universale",
            "anteriore", "posteriore", "destro", "sinistro",
            "economico", "premium", "performance", "racing"
        ]
        
        base_category = category_path[-1].lower() if category_path else ""
        
        for modifier in modifiers[:4]:  # Limita a 4 modificatori
            long_tail.append(f"{base_category} {modifier}")
            long_tail.append(f"{modifier} {base_category}")
        
        # Combinazioni con keywords del prodotto
        if product_keywords:
            for keyword in product_keywords[:3]:  # Limita a 3 keywords prodotto
                if keyword not in self.stop_words:
                    long_tail.append(f"{base_category} {keyword}")
                    long_tail.append(f"{keyword} {base_category}")
        
        # Combinazioni con brand comuni
        common_brands = ["bmw", "mercedes", "audi", "volkswagen", "fiat"]
        for brand in common_brands[:3]:
            long_tail.append(f"{base_category} {brand}")
        
        return list(set(long_tail))[:10]  # Massimo 10 keywords long-tail
    
    def _calculate_keyword_metrics(self, keyword: str) -> SEOMetrics:
        """Calcola metriche SEO per una keyword"""
        # Cerca nei dati esistenti
        if keyword in self.keyword_database:
            data = self.keyword_database[keyword]
            return SEOMetrics(
                keyword=keyword,
                search_volume=data["volume"],
                competition=data["competition"],
                difficulty=data["difficulty"],
                relevance_score=1.0,
                trend=data["trend"]
            )
        
        # Calcola metriche stimate
        estimated_volume = self._estimate_search_volume(keyword)
        estimated_competition = self._estimate_competition(keyword)
        estimated_difficulty = self._estimate_difficulty(keyword)
        relevance = self._calculate_relevance_score(keyword)
        trend = self._estimate_trend(keyword)
        
        return SEOMetrics(
            keyword=keyword,
            search_volume=estimated_volume,
            competition=estimated_competition,
            difficulty=estimated_difficulty,
            relevance_score=relevance,
            trend=trend
        )
    
    def _estimate_search_volume(self, keyword: str) -> int:
        """Stima il volume di ricerca per una keyword"""
        words = keyword.lower().split()
        total_volume = 0
        
        for word in words:
            if word in self.search_volume_data:
                total_volume += self.search_volume_data[word]
        
        # Applica fattore di riduzione per keywords composte
        if len(words) > 1:
            reduction_factor = 0.3 ** (len(words) - 1)
            total_volume = int(total_volume * reduction_factor)
        
        return max(total_volume, 100)  # Volume minimo di 100
    
    def _estimate_competition(self, keyword: str) -> float:
        """Stima la competizione per una keyword"""
        words = keyword.lower().split()
        competition_scores = []
        
        for word in words:
            if word in self.competition_data:
                competition_scores.append(self.competition_data[word])
        
        if competition_scores:
            # Media pesata (keywords più lunghe = meno competizione)
            weight = 1.0 / len(words)
            return min(sum(competition_scores) / len(competition_scores) * weight, 1.0)
        
        return 0.3  # Competizione di default per keywords sconosciute
    
    def _estimate_difficulty(self, keyword: str) -> float:
        """Stima la difficoltà SEO per una keyword"""
        # La difficoltà è correlata alla competizione ma considera anche la lunghezza
        competition = self._estimate_competition(keyword)
        length_factor = max(0.1, 1.0 - (len(keyword.split()) - 1) * 0.2)
        
        return min(competition * length_factor, 1.0)
    
    def _calculate_relevance_score(self, keyword: str) -> float:
        """Calcola il punteggio di rilevanza per una keyword automotive"""
        automotive_terms = {
            "auto", "car", "ricambi", "parts", "componenti", "accessori",
            "motore", "engine", "freni", "brake", "filtro", "filter",
            "olio", "oil", "pneumatici", "tire", "batteria", "battery"
        }
        
        words = set(keyword.lower().split())
        automotive_words = words.intersection(automotive_terms)
        
        if not automotive_words:
            return 0.3
        
        return min(len(automotive_words) / len(words), 1.0)
    
    def _estimate_trend(self, keyword: str) -> str:
        """Stima il trend per una keyword"""
        words = keyword.lower().split()
        
        for word in words:
            if word in self.trend_data:
                return self.trend_data[word]
        
        return "stable"  # Trend di default
    
    def _calculate_category_seo_score(self, primary_metrics: List[SEOMetrics],
                                    long_tail_metrics: List[SEOMetrics]) -> float:
        """Calcola il punteggio SEO complessivo per una categoria"""
        if not primary_metrics and not long_tail_metrics:
            return 0.0
        
        # Punteggio basato su volume, competizione e rilevanza
        total_score = 0.0
        total_weight = 0.0
        
        # Keywords primarie (peso maggiore)
        for metric in primary_metrics:
            volume_score = min(metric.search_volume / 10000, 1.0)  # Normalizza a 10k
            competition_score = 1.0 - metric.competition  # Meno competizione = meglio
            relevance_score = metric.relevance_score
            
            keyword_score = (volume_score * 0.4 + competition_score * 0.3 + relevance_score * 0.3)
            total_score += keyword_score * 0.7  # Peso 70% per keywords primarie
            total_weight += 0.7
        
        # Keywords long-tail (peso minore)
        for metric in long_tail_metrics:
            volume_score = min(metric.search_volume / 5000, 1.0)  # Normalizza a 5k
            competition_score = 1.0 - metric.competition
            relevance_score = metric.relevance_score
            
            keyword_score = (volume_score * 0.4 + competition_score * 0.3 + relevance_score * 0.3)
            total_score += keyword_score * 0.3  # Peso 30% per keywords long-tail
            total_weight += 0.3
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _generate_optimization_suggestions(self, category_path: List[str],
                                         primary_metrics: List[SEOMetrics],
                                         long_tail_metrics: List[SEOMetrics]) -> List[str]:
        """Genera suggerimenti per l'ottimizzazione SEO"""
        suggestions = []
        
        # Analizza keywords primarie
        high_competition_keywords = [
            m for m in primary_metrics if m.competition > 0.7
        ]
        
        if high_competition_keywords:
            suggestions.append(
                f"Considera keywords meno competitive per '{high_competition_keywords[0].keyword}'"
            )
        
        # Analizza volume di ricerca
        low_volume_keywords = [
            m for m in primary_metrics if m.search_volume < 1000
        ]
        
        if low_volume_keywords:
            suggestions.append(
                "Aggiungi keywords con volume di ricerca più alto"
            )
        
        # Suggerimenti per long-tail
        if len(long_tail_metrics) < 5:
            suggestions.append(
                "Espandi le keywords long-tail per catturare traffico più specifico"
            )
        
        # Suggerimenti basati su trend
        rising_trends = [m for m in primary_metrics + long_tail_metrics if m.trend == "rising"]
        if not rising_trends:
            suggestions.append(
                "Considera l'aggiunta di keywords con trend in crescita (es. 'elettrico', 'ibrido')"
            )
        
        # Suggerimenti per struttura categoria
        if len(category_path) > 4:
            suggestions.append(
                "Considera di semplificare la struttura della categoria (max 4 livelli)"
            )
        
        return suggestions[:5]  # Massimo 5 suggerimenti
    
    def _analyze_competitors(self, category_path: List[str]) -> Dict[str, float]:
        """Analizza i competitor per una categoria (simulato)"""
        # Simulazione di analisi competitor
        competitors = {
            "euroricambi.it": 0.8,
            "ricambiauto24.it": 0.7,
            "autodoc.it": 0.9,
            "tuttoautoricambi.it": 0.6,
            "ricambieuropa.com": 0.5
        }
        
        return competitors
    
    def rank_categories_by_seo(self, categories: List[List[str]], 
                             product_keywords: List[str] = None) -> List[Tuple[List[str], float]]:
        """Classifica le categorie in base al potenziale SEO"""
        category_scores = []
        
        for category_path in categories:
            analysis = self.analyze_category_seo(category_path, product_keywords)
            category_scores.append((category_path, analysis.seo_score))
        
        # Ordina per punteggio SEO decrescente
        category_scores.sort(key=lambda x: x[1], reverse=True)
        
        return category_scores
    
    def optimize_category_name(self, category_name: str, 
                             target_keywords: List[str] = None) -> str:
        """Ottimizza il nome di una categoria per la SEO"""
        # Rimuovi stop words
        words = [w for w in category_name.lower().split() if w not in self.stop_words]
        
        # Aggiungi target keywords se fornite
        if target_keywords:
            for keyword in target_keywords[:2]:  # Massimo 2 keywords aggiuntive
                if keyword.lower() not in words:
                    words.append(keyword.lower())
        
        # Riordina per importanza SEO
        word_scores = []
        for word in words:
            score = self._estimate_search_volume(word) / 1000  # Normalizza
            word_scores.append((word, score))
        
        # Ordina per punteggio e ricostruisci
        word_scores.sort(key=lambda x: x[1], reverse=True)
        optimized_words = [word for word, score in word_scores]
        
        # Capitalizza appropriatamente
        optimized_name = " ".join(word.title() for word in optimized_words)
        
        return optimized_name
    
    def generate_meta_tags(self, category_path: List[str], 
                          product_keywords: List[str] = None) -> Dict[str, str]:
        """Genera meta tags ottimizzati per una categoria"""
        analysis = self.analyze_category_seo(category_path, product_keywords)
        
        # Title tag
        primary_keyword = analysis.primary_keywords[0].keyword if analysis.primary_keywords else ""
        title = f"{' > '.join(category_path)} | {primary_keyword.title()} | Ricambi Auto"
        
        # Meta description
        top_keywords = [m.keyword for m in analysis.primary_keywords[:3]]
        description = f"Scopri la nostra selezione di {', '.join(top_keywords)}. " \
                     f"Ricambi auto di qualità per {category_path[-1].lower()}. " \
                     f"Spedizione rapida e prezzi competitivi."
        
        # Keywords meta tag
        all_keywords = [m.keyword for m in analysis.primary_keywords + analysis.long_tail_keywords]
        keywords = ", ".join(all_keywords[:10])  # Massimo 10 keywords
        
        return {
            "title": title[:60],  # Limita a 60 caratteri
            "description": description[:160],  # Limita a 160 caratteri
            "keywords": keywords
        }