"""Modulo di supporto specifico per la lingua italiana"""

from typing import Dict, List, Set, Tuple, Optional
import re
import json
from dataclasses import dataclass

@dataclass
class ItalianNLPConfig:
    """Configurazione NLP specifica per l'italiano"""
    stopwords: List[str]
    stemming_rules: Dict[str, str]
    compound_words: List[Tuple[str, str]]
    accent_normalization: bool = True
    enable_lemmatization: bool = True

class ItalianNLPSupport:
    """Classe di supporto per l'elaborazione del linguaggio naturale in italiano"""
    
    def __init__(self):
        self.stopwords = self._load_stopwords()
        self.stemming_rules = self._load_stemming_rules()
        self.compound_words = self._load_compound_words()
        self.automotive_terms = self._load_automotive_terms()
        self.regional_variants = self._load_regional_variants()
        
    def _load_stopwords(self) -> Set[str]:
        """Carica le stopwords italiane"""
        return {
            "il", "lo", "la", "i", "gli", "le", "un", "uno", "una", 
            "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
            "e", "ed", "o", "ma", "se", "perché", "come", "dove", "quando",
            "chi", "che", "cui", "quale", "quali", "del", "dello", "della", "dei", "degli", "delle",
            "al", "allo", "alla", "ai", "agli", "alle", "dal", "dallo", "dalla", "dai", "dagli", "dalle",
            "nel", "nello", "nella", "nei", "negli", "nelle", "sul", "sullo", "sulla", "sui", "sugli", "sulle",
            "questo", "questa", "questi", "queste", "quello", "quella", "quelli", "quelle",
            "mio", "mia", "miei", "mie", "tuo", "tua", "tuoi", "tue", "suo", "sua", "suoi", "sue",
            "nostro", "nostra", "nostri", "nostre", "vostro", "vostra", "vostri", "vostre",
            "loro", "sì", "no", "non", "più", "meno", "molto", "poco", "troppo", "tanto",
            "essere", "avere", "fare", "dire", "vedere", "sapere", "potere", "dovere", "volere"
        }
    
    def _load_stemming_rules(self) -> Dict[str, str]:
        """Regole di stemming per l'italiano"""
        return {
            # Plurali
            r'i$': 'o',  # es. ricambi -> ricambo
            r'e$': 'a',  # es. cinghie -> cinghia
            r'oni$': 'one',  # es. pistoni -> pistone
            r'ini$': 'ino',  # es. cuscinettini -> cuscinettino
            r'etti$': 'etto',  # es. cuscinetti -> cuscinetto
            r'elli$': 'ello',  # es. pistoncelli -> pistoncello
            r'ori$': 'ore',  # es. ammortizzatori -> ammortizzatore
            
            # Suffissi
            r'mente$': '',  # es. facilmente -> facil
            r'abile$': 'are',  # es. regolabile -> regolare
            r'ibile$': 'ire',  # es. sostituibile -> sostituire
            r'anza$': 'are',  # es. resistanza -> resistare
            r'enza$': 'ere',  # es. efficienza -> efficere
            r'aggio$': 'are',  # es. montaggio -> montare
            r'atore$': 'are',  # es. regolatore -> regolare
            r'zione$': 'to',  # es. regolazione -> regolato
            r'mento$': 're',  # es. funzionamento -> funzionare
        }
    
    def _load_compound_words(self) -> List[Tuple[str, str]]:
        """Parole composte comuni nel settore automotive"""
        return [
            ("auto", "ricambi"),
            ("ricambi", "auto"),
            ("kit", "frizione"),
            ("cinghia", "distribuzione"),
            ("filtro", "olio"),
            ("filtro", "aria"),
            ("filtro", "abitacolo"),
            ("pastiglie", "freno"),
            ("dischi", "freno"),
            ("pompa", "acqua"),
            ("pompa", "olio"),
            ("ammortizzatore", "anteriore"),
            ("ammortizzatore", "posteriore"),
            ("faro", "anteriore"),
            ("faro", "posteriore"),
            ("sensore", "temperatura"),
            ("sensore", "pressione"),
            ("olio", "motore"),
            ("candela", "accensione"),
            ("testina", "sterzo"),
            ("braccio", "oscillante"),
            ("albero", "motore"),
            ("albero", "trasmissione"),
            ("guarnizione", "testata"),
            ("cuscinetto", "ruota"),
        ]
    
    def _load_automotive_terms(self) -> Dict[str, List[str]]:
        """Termini specifici del settore automotive in italiano"""
        return {
            "parti_motore": [
                "pistone", "biella", "albero motore", "testata", "valvola", "distribuzione",
                "cinghia", "catena", "punteria", "guarnizione", "cilindro", "carter",
                "basamento", "monoblocco", "bronzina", "cuscinetto", "pompa olio", "pompa acqua",
                "termostato", "radiatore", "ventola", "intercooler", "turbocompressore", "aspirazione",
                "scarico", "collettore", "marmitta", "catalizzatore", "sonda lambda", "iniettore",
                "carburatore", "candela", "candeletta", "bobina", "spinterogeno", "alternatore",
                "motorino avviamento", "volano", "frizione", "cambio", "differenziale", "semiasse"
            ],
            "parti_freni": [
                "pastiglie", "disco", "tamburo", "pinza", "pistoncino", "cilindretti", "pompa freno",
                "servofreno", "abs", "liquido freni", "tubo freno", "cavo freno", "leva freno",
                "pedale freno", "freno a mano", "freno di stazionamento", "freno di servizio"
            ],
            "parti_sospensioni": [
                "ammortizzatore", "molla", "braccio oscillante", "barra stabilizzatrice",
                "silent block", "boccola", "testina sterzo", "scatola sterzo", "cremagliera",
                "idroguida", "servosterzo", "culla", "traversa", "montante", "mozzo", "cuscinetto ruota"
            ],
            "parti_elettriche": [
                "batteria", "alternatore", "motorino avviamento", "centralina", "fusibile",
                "relè", "interruttore", "sensore", "attuatore", "cablaggio", "faro", "fanale",
                "lampadina", "led", "xenon", "clacson", "tergicristallo", "motorino tergicristallo",
                "pompa lavavetri", "alzacristalli", "chiusura centralizzata", "antenna", "autoradio"
            ],
            "parti_carrozzeria": [
                "paraurti", "cofano", "parafango", "portiera", "maniglia", "serratura",
                "vetro", "parabrezza", "lunotto", "specchietto", "retrovisore", "tetto",
                "baule", "portellone", "spoiler", "minigonna", "modanatura", "griglia",
                "mascherina", "emblema", "logo", "stemma", "antenna", "tergicristallo"
            ],
            "parti_interni": [
                "sedile", "poggiatesta", "cintura", "airbag", "volante", "cruscotto",
                "quadro strumenti", "contachilometri", "contagiri", "tachimetro", "indicatore",
                "spia", "leva cambio", "pomello", "pedale", "freno a mano", "tappetino",
                "rivestimento", "pannello porta", "consolle", "climatizzatore", "riscaldamento"
            ],
            "fluidi_e_filtri": [
                "olio motore", "olio cambio", "olio differenziale", "liquido freni",
                "liquido raffreddamento", "antigelo", "liquido servosterzo", "liquido lavavetri",
                "filtro olio", "filtro aria", "filtro abitacolo", "filtro carburante", "filtro gasolio"
            ],
            "pneumatici_e_ruote": [
                "pneumatico", "gomma", "copertone", "cerchio", "cerchione", "ruota",
                "bullone", "dado", "coprimozzo", "copricerchio", "valvola", "camera d'aria"
            ]
        }
    
    def _load_regional_variants(self) -> Dict[str, List[str]]:
        """Varianti regionali italiane per termini automotive"""
        return {
            "gomma": ["copertone", "pneumatico"],
            "cerchio": ["cerchione", "ruota"],
            "cofano": ["cappotta", "bonnet"],
            "portiera": ["sportello"],
            "parabrezza": ["vetro anteriore", "cristallo"],
            "lunotto": ["vetro posteriore"],
            "baule": ["portabagagli", "bagagliaio", "vano bagagli"],
            "paraurti": ["parafango", "bumper"],
            "clacson": ["tromba", "avvisatore acustico"],
            "fanale": ["faro", "luce"],
            "freccia": ["indicatore di direzione", "lampeggiante"],
            "marmitta": ["silenziatore", "scarico"],
            "motorino d'avviamento": ["starter", "avviamento"],
            "freno a mano": ["freno di stazionamento", "freno di emergenza"],
            "cruscotto": ["plancia", "dashboard"],
            "volante": ["sterzo", "guida"],
            "benzina": ["carburante", "combustibile"],
            "gasolio": ["diesel", "nafta"],
            "tergicristallo": ["spazzola", "pulitore", "wiper"],
            "specchietto": ["retrovisore", "specchio"],
            "cintura": ["cintura di sicurezza", "safety belt"],
            "sedile": ["poltrona", "seat"],
            "cambio": ["trasmissione", "scatola del cambio"],
            "frizione": ["clutch", "innesto"],
            "acceleratore": ["gas", "pedale dell'acceleratore"],
            "batteria": ["accumulatore", "pila"]
        }
    
    def clean_text(self, text: str) -> str:
        """Pulisce e normalizza il testo in italiano"""
        # Converti in minuscolo
        text = text.lower()
        
        # Normalizza accenti
        text = self._normalize_accents(text)
        
        # Rimuovi caratteri speciali mantenendo lettere, numeri e spazi
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Sostituisci numeri con spazi
        text = re.sub(r'\d+', ' ', text)
        
        # Rimuovi spazi multipli
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _normalize_accents(self, text: str) -> str:
        """Normalizza i caratteri accentati in italiano"""
        replacements = {
            'à': 'a', 'è': 'e', 'é': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
            'À': 'A', 'È': 'E', 'É': 'E', 'Ì': 'I', 'Ò': 'O', 'Ù': 'U'
        }
        
        for accented, normal in replacements.items():
            text = text.replace(accented, normal)
        
        return text
    
    def remove_stopwords(self, text: str) -> str:
        """Rimuove le stopwords italiane dal testo"""
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in self.stopwords]
        return ' '.join(filtered_words)
    
    def stem_word(self, word: str) -> str:
        """Applica lo stemming a una parola italiana"""
        for pattern, replacement in self.stemming_rules.items():
            if re.search(pattern, word):
                return re.sub(pattern, replacement, word)
        return word
    
    def stem_text(self, text: str) -> str:
        """Applica lo stemming a un testo italiano"""
        words = text.split()
        stemmed_words = [self.stem_word(word) for word in words]
        return ' '.join(stemmed_words)
    
    def identify_compound_words(self, text: str) -> List[str]:
        """Identifica parole composte nel testo"""
        words = text.split()
        compounds = []
        
        for i in range(len(words) - 1):
            for first, second in self.compound_words:
                if words[i] == first and words[i+1] == second:
                    compounds.append(f"{first} {second}")
        
        return compounds
    
    def extract_automotive_terms(self, text: str) -> Dict[str, List[str]]:
        """Estrae termini automotive dal testo"""
        clean_text = self.clean_text(text)
        words = clean_text.split()
        
        results = {category: [] for category in self.automotive_terms.keys()}
        
        # Cerca termini singoli
        for word in words:
            for category, terms in self.automotive_terms.items():
                for term in terms:
                    if term == word or term in word:
                        results[category].append(term)
        
        # Cerca termini composti
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            for category, terms in self.automotive_terms.items():
                for term in terms:
                    if len(term.split()) > 1 and term == bigram:
                        results[category].append(term)
        
        # Rimuovi duplicati
        for category in results:
            results[category] = list(set(results[category]))
        
        return results
    
    def normalize_regional_variants(self, text: str) -> str:
        """Normalizza varianti regionali a termini standard"""
        words = text.split()
        normalized = []
        
        for word in words:
            normalized_word = word
            for standard, variants in self.regional_variants.items():
                if word in variants:
                    normalized_word = standard
                    break
            normalized.append(normalized_word)
        
        return ' '.join(normalized)

# Funzioni di utilità per l'italiano
def generate_italian_seo_keywords(category: str, subcategory: str, product_terms: List[str]) -> List[str]:
    """Genera keywords SEO ottimizzate per l'italiano"""
    base_templates = [
        "{product} per {brand}",
        "migliori {product} {category}",
        "{product} {category} online",
        "{product} {category} prezzo",
        "{product} {subcategory} economici",
        "{product} {subcategory} professionali",
        "vendita {product} {category}",
        "{product} {category} offerta",
        "{product} {category} originali",
        "{product} {category} compatibili",
        "{brand} {product} {subcategory}",
        "{product} {category} {year}",
        "ricambi {category} {subcategory}",
        "componenti {category} {product}",
        "accessori {category} {product}",
        "{product} {category} recensioni",
        "{product} {category} qualità",
        "{product} {category} confronto",
        "{product} {category} caratteristiche",
        "{product} {category} specifiche"
    ]
    
    # Genera keywords di base
    keywords = []
    for template in base_templates:
        for term in product_terms:
            keyword = template.format(
                product=term,
                category=category.lower(),
                subcategory=subcategory.lower(),
                brand="{brand}",  # Placeholder per brand specifici
                year="{year}"  # Placeholder per anni specifici
            )
            keywords.append(keyword)
    
    # Aggiungi varianti con preposizioni italiane
    preposition_variants = [
        "per", "di", "da", "con", "senza", "a"
    ]
    
    preposition_templates = [
        "{product} {preposition} {category}",
        "{product} {preposition} {subcategory}",
        "{category} {preposition} {product}",
        "{subcategory} {preposition} {product}"
    ]
    
    for template in preposition_templates:
        for preposition in preposition_variants:
            for term in product_terms:
                keyword = template.format(
                    product=term,
                    category=category.lower(),
                    subcategory=subcategory.lower(),
                    preposition=preposition
                )
                keywords.append(keyword)
    
    # Rimuovi duplicati e restituisci
    return list(set(keywords))

def analyze_italian_product_title(title: str) -> Dict[str, Any]:
    """Analizza un titolo di prodotto in italiano"""
    nlp_support = ItalianNLPSupport()
    clean_title = nlp_support.clean_text(title)
    
    # Estrai termini automotive
    automotive_terms = nlp_support.extract_automotive_terms(clean_title)
    
    # Identifica parole composte
    compound_words = nlp_support.identify_compound_words(clean_title)
    
    # Normalizza varianti regionali
    normalized_title = nlp_support.normalize_regional_variants(clean_title)
    
    # Rimuovi stopwords
    filtered_title = nlp_support.remove_stopwords(normalized_title)
    
    # Applica stemming
    stemmed_title = nlp_support.stem_text(filtered_title)
    
    return {
        "original": title,
        "cleaned": clean_title,
        "normalized": normalized_title,
        "filtered": filtered_title,
        "stemmed": stemmed_title,
        "automotive_terms": automotive_terms,
        "compound_words": compound_words
    }

# Esempi di utilizzo
if __name__ == "__main__":
    # Test di analisi titolo
    test_title = "Kit Frizione Originale per Fiat Punto 1.2 Benzina dal 2003 al 2010"
    analysis = analyze_italian_product_title(test_title)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    
    # Test generazione keywords SEO
    keywords = generate_italian_seo_keywords(
        "Auto", 
        "Trasmissione", 
        ["kit frizione", "disco frizione", "spingidisco"]
    )
    print(json.dumps(keywords[:10], indent=2, ensure_ascii=False))