"""Modulo principale per la categorizzazione dei prodotti in italiano"""

import os
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

# Importa i moduli di supporto per l'italiano
from src.italian_support import ItalianNLPSupport, analyze_italian_product_title, generate_italian_seo_keywords
from src.italian_config import get_italian_config, ITALIAN_CATEGORY_CONFIG
from src.exceptions import ProductCategorizerError, InvalidInputError, CategoryNotFoundError
from src.validators import ProductInput
from src.monitoring import MetricsCollector

# Configura il logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ItalianProductAnalysis:
    """Risultato dell'analisi di un prodotto in italiano"""
    product_id: str
    title: str
    description: Optional[str] = None
    brand: Optional[str] = None
    language: str = "it"
    categories: List[Dict[str, Any]] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    confidence: float = 0.0
    technical_terms: Dict[str, List[str]] = field(default_factory=dict)
    automotive_terms: Dict[str, List[str]] = field(default_factory=dict)
    compound_words: List[str] = field(default_factory=list)
    title_analysis: Dict[str, Any] = field(default_factory=dict)
    seo_suggestions: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ItalianCategoryResult:
    """Risultato della categorizzazione in italiano"""
    category_id: str
    category_name: str
    category_path: List[str]
    confidence: float
    subcategories: List[Dict[str, Any]] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)

class ItalianProductCategorizer:
    """Categorizzatore di prodotti ottimizzato per la lingua italiana"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Inizializza il categorizzatore di prodotti in italiano"""
        self.nlp_support = ItalianNLPSupport()
        self.config = self._load_config(config_path)
        self.category_tree = ITALIAN_CATEGORY_CONFIG
        self.metrics = MetricsCollector()
        self.seo_keywords = self._load_seo_keywords()
        self.brand_database = self._load_brand_database()
        logger.info("Inizializzato categorizzatore prodotti in italiano")
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Carica la configurazione da file o utilizza quella predefinita"""
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                logger.info(f"Configurazione caricata da {config_path}")
                return config
            except Exception as e:
                logger.error(f"Errore nel caricamento della configurazione: {str(e)}")
                logger.info("Utilizzo della configurazione predefinita")
        
        # Utilizza la configurazione predefinita
        return get_italian_config()
    
    def _load_seo_keywords(self) -> Dict[str, List[str]]:
        """Carica le parole chiave SEO per le categorie"""
        seo_keywords = {}
        
        # Esempio di database di parole chiave SEO per categorie
        seo_keywords["ricambi_auto"] = [
            "ricambi auto online", "ricambi auto originali", "ricambi auto usati",
            "ricambi auto economici", "ricambi auto compatibili", "autoricambi",
            "pezzi di ricambio auto", "componenti auto", "parti di ricambio auto"
        ]
        
        seo_keywords["freni"] = [
            "pastiglie freno", "dischi freno", "kit freni", "freni a tamburo",
            "pinze freno", "liquido freni", "cavi freno", "freni auto",
            "impianto frenante", "freni sportivi", "freni ad alte prestazioni"
        ]
        
        seo_keywords["motore"] = [
            "parti motore", "ricambi motore", "guarnizioni motore", "testata motore",
            "pistoni", "albero motore", "cinghia distribuzione", "pompa acqua",
            "pompa olio", "filtro olio", "filtro aria", "turbocompressore"
        ]
        
        seo_keywords["trasmissione"] = [
            "frizione", "kit frizione", "volano", "cambio", "differenziale",
            "semiassi", "giunti omocinetici", "cuffie", "olio cambio",
            "sincronizzatori", "cuscinetti cambio", "leva cambio"
        ]
        
        seo_keywords["elettrico"] = [
            "batteria auto", "alternatore", "motorino avviamento", "centralina",
            "sensori auto", "fari auto", "fanali", "lampadine auto", "fusibili",
            "relè", "cablaggio auto", "impianto elettrico auto"
        ]
        
        seo_keywords["carrozzeria"] = [
            "paraurti", "cofano", "parafanghi", "portiere", "specchietti",
            "parabrezza", "lunotto", "vetri auto", "maniglie", "serrature",
            "modanature", "griglie", "emblemi", "spoiler", "minigonne"
        ]
        
        seo_keywords["filtri"] = [
            "filtro olio", "filtro aria", "filtro abitacolo", "filtro carburante",
            "filtro antipolline", "filtro gasolio", "kit filtri", "cartuccia filtro",
            "filtri auto", "manutenzione filtri", "cambio filtri"
        ]
        
        seo_keywords["pneumatici"] = [
            "pneumatici auto", "gomme auto", "pneumatici estivi", "pneumatici invernali",
            "pneumatici 4 stagioni", "cerchi in lega", "cerchi in acciaio", "TPMS",
            "pressione pneumatici", "battistrada", "equilibratura", "convergenza"
        ]
        
        return seo_keywords
    
    def _load_brand_database(self) -> Dict[str, List[str]]:
        """Carica il database dei brand automobilistici"""
        return self.config["brands"]
    
    def categorize_product(self, product_input: ProductInput) -> ItalianProductAnalysis:
        """Categorizza un prodotto in italiano"""
        self.metrics.increment_requests()
        
        try:
            # Valida l'input
            if product_input.language != "it":
                raise InvalidInputError("La lingua deve essere impostata su 'it' per l'italiano")
            
            # Analizza il titolo del prodotto
            title_analysis = analyze_italian_product_title(product_input.title)
            
            # Identifica le categorie
            categories, confidence = self._identify_categories(title_analysis, product_input.description)
            
            # Genera parole chiave SEO
            keywords = self._generate_seo_keywords(categories, title_analysis)
            
            # Crea l'analisi del prodotto
            product_analysis = ItalianProductAnalysis(
                product_id=product_input.product_id or "unknown",
                title=product_input.title,
                description=product_input.description,
                brand=product_input.brand,
                language=product_input.language,
                categories=categories,
                keywords=keywords,
                confidence=confidence,
                technical_terms=self._extract_technical_terms(title_analysis, product_input.description),
                automotive_terms=title_analysis.get("automotive_terms", {}),
                compound_words=title_analysis.get("compound_words", []),
                title_analysis=title_analysis,
                seo_suggestions=self._generate_seo_suggestions(title_analysis, product_input.description, categories)
            )
            
            self.metrics.increment_categorizations()
            return product_analysis
            
        except Exception as e:
            self.metrics.increment_errors()
            logger.error(f"Errore nella categorizzazione del prodotto: {str(e)}")
            raise ProductCategorizerError(f"Errore nella categorizzazione del prodotto: {str(e)}")
    
    def _identify_categories(self, title_analysis: Dict[str, Any], description: Optional[str] = None) -> Tuple[List[Dict[str, Any]], float]:
        """Identifica le categorie del prodotto in base all'analisi del titolo e alla descrizione"""
        categories = []
        max_confidence = 0.0
        
        # Estrai termini automotive dall'analisi del titolo
        automotive_terms = title_analysis.get("automotive_terms", {})
        
        # Analizza la descrizione se disponibile
        description_terms = {}
        if description:
            description_analysis = analyze_italian_product_title(description)
            description_terms = description_analysis.get("automotive_terms", {})
        
        # Combina i termini dal titolo e dalla descrizione
        all_terms = {}
        for category, terms in automotive_terms.items():
            all_terms[category] = terms.copy()
        
        for category, terms in description_terms.items():
            if category in all_terms:
                all_terms[category].extend(terms)
                all_terms[category] = list(set(all_terms[category]))  # Rimuovi duplicati
            else:
                all_terms[category] = terms
        
        # Calcola il punteggio per ogni categoria principale
        category_scores = {}
        for main_category, data in self.category_tree.items():
            category_scores[main_category] = 0
            
            # Controlla ogni sottocategoria
            for subcategory_key, subcategory_data in data.get("subcategories", {}).items():
                subcategory_score = 0
                subcategory_keywords = subcategory_data.get("keywords", [])
                
                # Controlla se i termini automotive corrispondono alle parole chiave della sottocategoria
                for category, terms in all_terms.items():
                    for term in terms:
                        if term in subcategory_keywords:
                            subcategory_score += 1
                
                # Aggiorna il punteggio della categoria principale
                category_scores[main_category] += subcategory_score
        
        # Ordina le categorie per punteggio
        sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Prendi le prime N categorie con punteggio > 0
        max_categories = self.config["model"].get("max_categories", 3)
        for category_id, score in sorted_categories:
            if score > 0 and len(categories) < max_categories:
                category_data = self.category_tree.get(category_id, {})
                main_category_name = category_data.get("main_category", category_id)
                
                # Calcola la confidenza (normalizzata tra 0 e 1)
                confidence = min(score / 10.0, 1.0)  # Normalizza il punteggio
                max_confidence = max(max_confidence, confidence)
                
                # Trova le sottocategorie più rilevanti
                subcategories = []
                for subcategory_key, subcategory_data in category_data.get("subcategories", {}).items():
                    subcategory_score = 0
                    subcategory_keywords = subcategory_data.get("keywords", [])
                    
                    # Controlla se i termini automotive corrispondono alle parole chiave della sottocategoria
                    for category, terms in all_terms.items():
                        for term in terms:
                            if term in subcategory_keywords:
                                subcategory_score += 1
                    
                    if subcategory_score > 0:
                        subcategory_confidence = min(subcategory_score / 5.0, 1.0)  # Normalizza il punteggio
                        subcategories.append({
                            "id": subcategory_key,
                            "name": subcategory_data.get("name", subcategory_key),
                            "confidence": subcategory_confidence
                        })
                
                # Ordina le sottocategorie per confidenza
                subcategories = sorted(subcategories, key=lambda x: x["confidence"], reverse=True)
                
                # Crea il risultato della categoria
                category_result = {
                    "id": category_id,
                    "name": main_category_name,
                    "confidence": confidence,
                    "subcategories": subcategories[:3]  # Prendi le prime 3 sottocategorie
                }
                
                categories.append(category_result)
        
        # Se non sono state trovate categorie, restituisci una categoria generica
        if not categories:
            categories.append({
                "id": "ricambi_auto",
                "name": "Ricambi Auto",
                "confidence": 0.5,
                "subcategories": []
            })
            max_confidence = 0.5
        
        return categories, max_confidence
    
    def _generate_seo_keywords(self, categories: List[Dict[str, Any]], title_analysis: Dict[str, Any]) -> List[str]:
        """Genera parole chiave SEO in base alle categorie identificate"""
        keywords = []
        
        # Aggiungi parole chiave SEO per ogni categoria
        for category in categories:
            category_id = category.get("id")
            if category_id in self.seo_keywords:
                keywords.extend(self.seo_keywords[category_id])
            
            # Aggiungi parole chiave SEO per le sottocategorie
            for subcategory in category.get("subcategories", []):
                subcategory_id = subcategory.get("id")
                if subcategory_id in self.seo_keywords:
                    keywords.extend(self.seo_keywords[subcategory_id])
        
        # Aggiungi parole chiave basate sui termini automotive identificati
        automotive_terms = title_analysis.get("automotive_terms", {})
        for category, terms in automotive_terms.items():
            if category == "parti_motore":
                keywords.append("ricambi motore")
                keywords.append("parti motore auto")
            elif category == "parti_freni":
                keywords.append("ricambi freni auto")
                keywords.append("sistema frenante")
            elif category == "parti_sospensioni":
                keywords.append("ricambi sospensioni")
                keywords.append("ammortizzatori auto")
            elif category == "parti_elettriche":
                keywords.append("componenti elettrici auto")
                keywords.append("impianto elettrico auto")
            elif category == "parti_carrozzeria":
                keywords.append("ricambi carrozzeria auto")
                keywords.append("parti carrozzeria")
            elif category == "fluidi_e_filtri":
                keywords.append("filtri auto")
                keywords.append("olio motore")
            elif category == "pneumatici_e_ruote":
                keywords.append("pneumatici auto")
                keywords.append("cerchi in lega")
        
        # Rimuovi duplicati e limita il numero di parole chiave
        keywords = list(set(keywords))
        max_keywords = self.config["seo"].get("max_keywords", 10)
        
        return keywords[:max_keywords]
    
    def _extract_technical_terms(self, title_analysis: Dict[str, Any], description: Optional[str] = None) -> Dict[str, List[str]]:
        """Estrae termini tecnici dal titolo e dalla descrizione"""
        technical_terms = {}
        
        # Estrai termini tecnici dal titolo
        title_text = title_analysis.get("cleaned", "")
        
        # Aggiungi termini dalla descrizione se disponibile
        if description:
            description_text = self.nlp_support.clean_text(description)
            text_to_analyze = f"{title_text} {description_text}"
        else:
            text_to_analyze = title_text
        
        # Cerca termini tecnici nel testo
        for category, terms in self.config["technical_terms"].items():
            found_terms = []
            for term in terms:
                if term in text_to_analyze:
                    found_terms.append(term)
            
            if found_terms:
                technical_terms[category] = found_terms
        
        return technical_terms
    
    def _generate_seo_suggestions(self, title_analysis: Dict[str, Any], description: Optional[str] = None, categories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Genera suggerimenti SEO per il prodotto"""
        suggestions = {}
        
        # Analizza il titolo
        title = title_analysis.get("original", "")
        title_length = len(title)
        title_min = self.config["seo"]["title_length"]["min"]
        title_max = self.config["seo"]["title_length"]["max"]
        title_optimal = self.config["seo"]["title_length"]["optimal"]
        
        # Suggerimenti per il titolo
        if title_length < title_min:
            suggestions["title"] = f"Il titolo è troppo corto ({title_length} caratteri). Dovrebbe essere almeno {title_min} caratteri."
        elif title_length > title_max:
            suggestions["title"] = f"Il titolo è troppo lungo ({title_length} caratteri). Dovrebbe essere al massimo {title_max} caratteri."
        else:
            suggestions["title"] = f"La lunghezza del titolo è buona ({title_length} caratteri)."
        
        # Analizza la descrizione
        if description:
            description_length = len(description)
            description_min = self.config["seo"]["description_length"]["min"]
            description_max = self.config["seo"]["description_length"]["max"]
            description_optimal = self.config["seo"]["description_length"]["optimal"]
            
            # Suggerimenti per la descrizione
            if description_length < description_min:
                suggestions["description"] = f"La descrizione è troppo corta ({description_length} caratteri). Dovrebbe essere almeno {description_min} caratteri."
            elif description_length > description_max:
                suggestions["description"] = f"La descrizione è troppo lunga ({description_length} caratteri). Dovrebbe essere al massimo {description_max} caratteri."
            else:
                suggestions["description"] = f"La lunghezza della descrizione è buona ({description_length} caratteri)."
        else:
            suggestions["description"] = "Manca la descrizione. Aggiungere una descrizione dettagliata del prodotto."
        
        # Suggerimenti per le parole chiave
        if categories:
            main_category = categories[0]
            category_name = main_category.get("name")
            subcategories = main_category.get("subcategories", [])
            
            if subcategories:
                subcategory_name = subcategories[0].get("name")
                suggestions["keywords"] = f"Includere parole chiave relative a '{category_name}' e '{subcategory_name}'."
            else:
                suggestions["keywords"] = f"Includere parole chiave relative a '{category_name}'."
        else:
            suggestions["keywords"] = "Includere parole chiave specifiche per la categoria del prodotto."
        
        # Suggerimenti per i marketplace
        suggestions["marketplace"] = f"Ottimizzare per i seguenti marketplace italiani: {', '.join(self.config['seo']['popular_italian_marketplaces'][:3])}"
        
        return suggestions

# Funzione di utilità per testare il categorizzatore
def test_italian_categorizer():
    """Funzione di test per il categorizzatore di prodotti in italiano"""
    categorizer = ItalianProductCategorizer()
    
    # Esempio di prodotto
    product = ProductInput(
        product_id="12345",
        title="Kit Frizione Completo per Fiat Punto 1.2 Benzina 2003-2010 con Volano e Cuscinetto Reggispinta",
        description="Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina prodotta dal 2003 al 2010. Il kit include disco frizione, spingidisco, volano e cuscinetto reggispinta. Prodotto da un fornitore affidabile di ricambi aftermarket con qualità equivalente all'originale.",
        brand="Valeo",
        language="it"
    )
    
    # Categorizza il prodotto
    result = categorizer.categorize_product(product)
    
    # Stampa il risultato
    print(json.dumps({
        "product_id": result.product_id,
        "title": result.title,
        "categories": result.categories,
        "keywords": result.keywords,
        "confidence": result.confidence,
        "seo_suggestions": result.seo_suggestions
    }, indent=2, ensure_ascii=False))

# Esegui il test se il modulo viene eseguito direttamente
if __name__ == "__main__":
    test_italian_categorizer()