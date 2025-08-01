"""Configurazione specifica per la lingua italiana"""

from typing import Dict, List, Any

# Configurazione del modello per l'italiano
ITALIAN_MODEL_CONFIG = {
    "embedding_model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    "similarity_threshold": 0.75,  # Soglia di similarità per la corrispondenza delle categorie
    "confidence_threshold": 0.65,  # Soglia di confidenza per l'accettazione delle categorie
    "language_detection_confidence": 0.8,  # Soglia di confidenza per il rilevamento della lingua
    "max_categories": 3,  # Numero massimo di categorie da restituire
    "enable_stemming": True,  # Abilita lo stemming per l'italiano
    "enable_lemmatization": True,  # Abilita la lemmatizzazione per l'italiano
    "enable_compound_detection": True,  # Abilita il rilevamento di parole composte
    "enable_regional_normalization": True,  # Abilita la normalizzazione delle varianti regionali
}

# Configurazione SEO per l'italiano
ITALIAN_SEO_CONFIG = {
    "max_keywords": 10,  # Numero massimo di parole chiave da generare
    "min_search_volume": 100,  # Volume di ricerca minimo per considerare una parola chiave
    "max_competition": 0.7,  # Competizione massima per considerare una parola chiave
    "title_length": {
        "min": 50,  # Lunghezza minima del titolo in caratteri
        "max": 70,  # Lunghezza massima del titolo in caratteri
        "optimal": 60  # Lunghezza ottimale del titolo in caratteri
    },
    "description_length": {
        "min": 120,  # Lunghezza minima della descrizione in caratteri
        "max": 160,  # Lunghezza massima della descrizione in caratteri
        "optimal": 150  # Lunghezza ottimale della descrizione in caratteri
    },
    "keyword_density": {
        "min": 0.01,  # Densità minima delle parole chiave (1%)
        "max": 0.03,  # Densità massima delle parole chiave (3%)
        "optimal": 0.02  # Densità ottimale delle parole chiave (2%)
    },
    "popular_italian_marketplaces": [
        "Amazon.it",
        "eBay.it",
        "ePrice",
        "Subito.it",
        "IBS",
        "Zalando",
        "ManoMano",
        "Trovaprezzi",
        "Idealo"
    ]
}

# Configurazione delle categorie di prodotti in italiano
ITALIAN_CATEGORY_CONFIG = {
    "automotive": {
        "main_category": "Ricambi Auto",
        "subcategories": {
            "motore": {
                "name": "Motore",
                "keywords": [
                    "pistone", "biella", "albero motore", "testata", "valvola", "distribuzione",
                    "cinghia", "catena", "punteria", "guarnizione", "cilindro", "carter",
                    "basamento", "monoblocco", "bronzina", "cuscinetto", "pompa olio", "pompa acqua"
                ],
                "subcategories": {
                    "distribuzione": {
                        "name": "Distribuzione",
                        "keywords": ["cinghia distribuzione", "catena distribuzione", "tendicinghia", "puleggia", "albero a camme"]
                    },
                    "raffreddamento": {
                        "name": "Raffreddamento",
                        "keywords": ["radiatore", "termostato", "ventola", "pompa acqua", "liquido raffreddamento"]
                    },
                    "lubrificazione": {
                        "name": "Lubrificazione",
                        "keywords": ["pompa olio", "filtro olio", "olio motore", "coppa olio", "sensore pressione olio"]
                    }
                }
            },
            "freni": {
                "name": "Freni",
                "keywords": [
                    "pastiglie", "disco", "tamburo", "pinza", "pistoncino", "cilindretti", "pompa freno",
                    "servofreno", "abs", "liquido freni", "tubo freno", "cavo freno", "leva freno"
                ],
                "subcategories": {
                    "pastiglie": {
                        "name": "Pastiglie Freno",
                        "keywords": ["pastiglie freno anteriori", "pastiglie freno posteriori", "sensore usura"]
                    },
                    "dischi": {
                        "name": "Dischi Freno",
                        "keywords": ["disco freno anteriore", "disco freno posteriore", "disco ventilato", "disco forato"]
                    },
                    "idraulica": {
                        "name": "Idraulica Freni",
                        "keywords": ["pompa freno", "cilindretti", "pinza", "liquido freni", "tubo freno"]
                    }
                }
            },
            "sospensioni": {
                "name": "Sospensioni",
                "keywords": [
                    "ammortizzatore", "molla", "braccio oscillante", "barra stabilizzatrice",
                    "silent block", "boccola", "testina sterzo", "scatola sterzo", "cremagliera"
                ],
                "subcategories": {
                    "ammortizzatori": {
                        "name": "Ammortizzatori",
                        "keywords": ["ammortizzatore anteriore", "ammortizzatore posteriore", "kit ammortizzatori"]
                    },
                    "molle": {
                        "name": "Molle",
                        "keywords": ["molla anteriore", "molla posteriore", "kit molle", "molla ribassata"]
                    },
                    "bracci": {
                        "name": "Bracci e Articolazioni",
                        "keywords": ["braccio oscillante", "testina sterzo", "giunto sferico", "silent block"]
                    }
                }
            },
            "trasmissione": {
                "name": "Trasmissione",
                "keywords": [
                    "frizione", "volano", "cambio", "differenziale", "semiasse", "giunto", "crociera",
                    "cuscinetto", "sincronizzatore", "selettore", "leva cambio", "cavo frizione"
                ],
                "subcategories": {
                    "frizione": {
                        "name": "Frizione",
                        "keywords": ["kit frizione", "disco frizione", "spingidisco", "cuscinetto reggispinta", "volano"]
                    },
                    "cambio": {
                        "name": "Cambio",
                        "keywords": ["ingranaggio", "sincronizzatore", "selettore", "forcella", "olio cambio"]
                    },
                    "semiassi": {
                        "name": "Semiassi e Giunti",
                        "keywords": ["semiasse", "giunto omocinetico", "cuffia", "crociera", "differenziale"]
                    }
                }
            },
            "elettrico": {
                "name": "Elettrico",
                "keywords": [
                    "batteria", "alternatore", "motorino avviamento", "centralina", "fusibile",
                    "relè", "interruttore", "sensore", "attuatore", "cablaggio", "faro", "fanale"
                ],
                "subcategories": {
                    "illuminazione": {
                        "name": "Illuminazione",
                        "keywords": ["faro", "fanale", "lampadina", "led", "xenon", "freccia", "luce targa"]
                    },
                    "avviamento": {
                        "name": "Avviamento e Ricarica",
                        "keywords": ["batteria", "alternatore", "motorino avviamento", "regolatore tensione"]
                    },
                    "sensori": {
                        "name": "Sensori e Attuatori",
                        "keywords": ["sensore temperatura", "sensore pressione", "sensore giri", "attuatore"]
                    }
                }
            },
            "carrozzeria": {
                "name": "Carrozzeria",
                "keywords": [
                    "paraurti", "cofano", "parafango", "portiera", "maniglia", "serratura",
                    "vetro", "parabrezza", "lunotto", "specchietto", "retrovisore", "tetto"
                ],
                "subcategories": {
                    "esterni": {
                        "name": "Esterni",
                        "keywords": ["paraurti", "cofano", "parafango", "portiera", "specchietto", "griglia"]
                    },
                    "vetri": {
                        "name": "Vetri e Cristalli",
                        "keywords": ["parabrezza", "lunotto", "vetro laterale", "alzacristalli", "guarnizione vetro"]
                    },
                    "serrature": {
                        "name": "Serrature e Chiusure",
                        "keywords": ["serratura", "maniglia", "chiusura centralizzata", "telecomando", "cilindretto"]
                    }
                }
            },
            "filtri": {
                "name": "Filtri",
                "keywords": [
                    "filtro olio", "filtro aria", "filtro abitacolo", "filtro carburante", "filtro gasolio"
                ],
                "subcategories": {
                    "filtro_aria": {
                        "name": "Filtri Aria",
                        "keywords": ["filtro aria motore", "filtro sportivo", "scatola filtro", "manicotto"]
                    },
                    "filtro_olio": {
                        "name": "Filtri Olio",
                        "keywords": ["filtro olio motore", "cartuccia filtro", "chiave filtro", "guarnizione"]
                    },
                    "filtro_carburante": {
                        "name": "Filtri Carburante",
                        "keywords": ["filtro benzina", "filtro gasolio", "prefiltro", "sensore acqua"]
                    }
                }
            },
            "pneumatici": {
                "name": "Pneumatici e Ruote",
                "keywords": [
                    "pneumatico", "gomma", "copertone", "cerchio", "cerchione", "ruota",
                    "bullone", "dado", "coprimozzo", "copricerchio", "valvola", "camera d'aria"
                ],
                "subcategories": {
                    "pneumatici": {
                        "name": "Pneumatici",
                        "keywords": ["pneumatico estivo", "pneumatico invernale", "pneumatico 4 stagioni", "battistrada"]
                    },
                    "cerchi": {
                        "name": "Cerchi",
                        "keywords": ["cerchio in lega", "cerchio in acciaio", "cerchio originale", "canale"]
                    },
                    "accessori": {
                        "name": "Accessori Ruote",
                        "keywords": ["bullone", "dado", "antifurto", "distanziale", "coprimozzo", "copricerchio"]
                    }
                }
            }
        }
    }
}

# Configurazione dei brand automobilistici italiani
ITALIAN_AUTOMOTIVE_BRANDS = {
    "italiani": [
        "Fiat", "Alfa Romeo", "Lancia", "Ferrari", "Lamborghini", "Maserati", 
        "Pagani", "Abarth", "Autobianchi", "Innocenti", "De Tomaso", "Piaggio", 
        "Ducati", "MV Agusta", "Aprilia", "Benelli", "Moto Guzzi", "Cagiva", "Iveco"
    ],
    "europei": [
        "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Opel", "Renault", "Peugeot", 
        "Citroën", "Seat", "Škoda", "Volvo", "Porsche", "Land Rover", "Jaguar", 
        "Mini", "Smart", "Dacia", "Bugatti", "Bentley", "Rolls-Royce", "Aston Martin"
    ],
    "asiatici": [
        "Toyota", "Honda", "Nissan", "Mazda", "Mitsubishi", "Suzuki", "Subaru", 
        "Daihatsu", "Lexus", "Infiniti", "Hyundai", "Kia", "Daewoo", "SsangYong"
    ],
    "americani": [
        "Ford", "Chevrolet", "Jeep", "Chrysler", "Dodge", "Cadillac", "GMC", 
        "Buick", "Lincoln", "Tesla", "Hummer", "Pontiac", "Oldsmobile"
    ]
}

# Configurazione dei termini tecnici in italiano
ITALIAN_TECHNICAL_TERMS = {
    "specifiche_motore": [
        "cilindrata", "potenza", "coppia", "cavalli", "kW", "CV", "Nm", "cc", 
        "aspirato", "turbo", "sovralimentato", "iniezione", "carburatore", "valvole", 
        "distribuzione", "DOHC", "SOHC", "VVT", "common rail", "multijet", "multiair"
    ],
    "specifiche_trasmissione": [
        "manuale", "automatico", "sequenziale", "CVT", "doppia frizione", "DSG", 
        "marce", "rapporti", "trazione anteriore", "trazione posteriore", "trazione integrale", 
        "4x4", "AWD", "FWD", "RWD", "differenziale", "bloccaggio", "autobloccante"
    ],
    "specifiche_dimensioni": [
        "lunghezza", "larghezza", "altezza", "passo", "carreggiata", "peso", 
        "massa", "portata", "capacità bagagliaio", "volume", "litri", "kg", "mm"
    ],
    "specifiche_prestazioni": [
        "velocità massima", "accelerazione", "0-100", "consumo", "emissioni", 
        "CO2", "g/km", "l/100km", "km/l", "autonomia", "classe emissioni", "Euro 6"
    ],
    "specifiche_pneumatici": [
        "misura", "pollici", "indice carico", "indice velocità", "pressione", 
        "bar", "PSI", "battistrada", "profondità", "mm", "DOT", "M+S", "3PMSF"
    ]
}

# Configurazione delle frasi comuni in italiano per la descrizione dei prodotti
ITALIAN_PRODUCT_PHRASES = {
    "qualità": [
        "alta qualità", "qualità premium", "qualità OEM", "qualità originale", 
        "qualità aftermarket", "qualità superiore", "materiali di prima scelta", 
        "costruzione robusta", "fabbricazione precisa", "standard elevati"
    ],
    "compatibilità": [
        "compatibile con", "adatto per", "specifico per", "dedicato a", 
        "si adatta a", "progettato per", "per i modelli", "per le versioni", 
        "per i motori", "universale", "intercambiabile con"
    ],
    "vantaggi": [
        "facile installazione", "lunga durata", "prestazioni migliorate", 
        "risparmio di carburante", "maggiore affidabilità", "minore usura", 
        "funzionamento silenzioso", "manutenzione ridotta", "resistente alla corrosione", 
        "resistente alle alte temperature", "miglior rapporto qualità-prezzo"
    ],
    "garanzia": [
        "garanzia di 2 anni", "garanzia del produttore", "soddisfatti o rimborsati", 
        "testato in laboratorio", "certificato TÜV", "conforme agli standard", 
        "approvato da", "omologato", "certificato di qualità", "100% testato"
    ]
}

# Funzione per ottenere la configurazione completa per l'italiano
def get_italian_config() -> Dict[str, Any]:
    """Restituisce la configurazione completa per l'italiano"""
    return {
        "model": ITALIAN_MODEL_CONFIG,
        "seo": ITALIAN_SEO_CONFIG,
        "categories": ITALIAN_CATEGORY_CONFIG,
        "brands": ITALIAN_AUTOMOTIVE_BRANDS,
        "technical_terms": ITALIAN_TECHNICAL_TERMS,
        "product_phrases": ITALIAN_PRODUCT_PHRASES
    }