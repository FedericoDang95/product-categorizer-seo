from typing import Dict, List

# Struttura ad albero delle categorie di esempio per ricambi auto
SAMPLE_CATEGORY_TREE = {
    "Ricambi Auto": {
        "Motore": {
            "Pistoni e Bielle": {},
            "Valvole e Distribuzione": {
                "Cinghie Distribuzione": {},
                "Catene Distribuzione": {},
                "Valvole": {},
                "Punterie": {}
            },
            "Guarnizioni": {
                "Guarnizione Testata": {},
                "Guarnizioni Varie": {}
            },
            "Filtri": {
                "Filtro Olio": {},
                "Filtro Aria": {},
                "Filtro Carburante": {}
            }
        },
        "Freni": {
            "Pastiglie Freno": {
                "Pastiglie Anteriori": {},
                "Pastiglie Posteriori": {}
            },
            "Dischi Freno": {
                "Dischi Anteriori": {},
                "Dischi Posteriori": {}
            },
            "Tamburi Freno": {},
            "Pinze Freno": {},
            "Tubi Freno": {}
        },
        "Sospensioni": {
            "Ammortizzatori": {
                "Ammortizzatori Anteriori": {},
                "Ammortizzatori Posteriori": {}
            },
            "Molle": {
                "Molle Anteriori": {},
                "Molle Posteriori": {}
            },
            "Barre Stabilizzatrici": {},
            "Silent Block": {}
        },
        "Trasmissione": {
            "Frizione": {
                "Kit Frizione": {},
                "Spingidisco": {},
                "Disco Frizione": {},
                "Cuscinetto Reggispinta": {}
            },
            "Cambio": {
                "Olio Cambio": {},
                "Filtro Cambio": {}
            },
            "Differenziale": {},
            "Semiassi": {}
        },
        "Elettrico": {
            "Alternatore": {},
            "Motorino Avviamento": {},
            "Candele": {
                "Candele Accensione": {},
                "Candelette": {}
            },
            "Bobine Accensione": {},
            "Sensori": {
                "Sensore ABS": {},
                "Sensore Temperatura": {},
                "Sensore Pressione": {}
            }
        },
        "Carrozzeria": {
            "Paraurti": {
                "Paraurti Anteriori": {},
                "Paraurti Posteriori": {}
            },
            "Cofano": {},
            "Portiere": {},
            "Specchietti": {
                "Specchietti Esterni": {},
                "Specchietti Interni": {}
            },
            "Fari": {
                "Fari Anteriori": {},
                "Fari Posteriori": {},
                "Fari Fendinebbia": {}
            }
        }
    },
    "Accessori Auto": {
        "Interni": {
            "Sedili": {},
            "Volante": {},
            "Cruscotto": {},
            "Tappetini": {},
            "Rivestimenti": {}
        },
        "Esterni": {
            "Deflettori": {},
            "Spoiler": {},
            "Protezioni": {}
        },
        "Comfort": {
            "Climatizzazione": {},
            "Audio": {},
            "Navigazione": {}
        }
    },
    "Pneumatici": {
        "Estivi": {
            "185/65 R15": {},
            "195/65 R15": {},
            "205/55 R16": {},
            "225/45 R17": {}
        },
        "Invernali": {
            "185/65 R15": {},
            "195/65 R15": {},
            "205/55 R16": {},
            "225/45 R17": {}
        },
        "All Season": {},
        "Cerchi": {
            "Cerchi in Lega": {},
            "Cerchi in Acciaio": {}
        }
    },
    "Oli e Lubrificanti": {
        "Olio Motore": {
            "5W-30": {},
            "5W-40": {},
            "10W-40": {},
            "15W-40": {}
        },
        "Olio Cambio": {},
        "Olio Differenziale": {},
        "Liquido Freni": {},
        "Liquido Raffreddamento": {},
        "Additivi": {}
    },
    "Batterie": {
        "Batterie Auto": {
            "60Ah": {},
            "70Ah": {},
            "80Ah": {},
            "100Ah": {}
        },
        "Batterie Moto": {},
        "Caricabatterie": {}
    }
}

# Prodotti di esempio per testare il sistema
SAMPLE_PRODUCTS = [
    {
        "title": "Pastiglie Freno Anteriori Brembo per BMW Serie 3 E90 2005-2012",
        "description": "Pastiglie freno anteriori originali Brembo specifiche per BMW Serie 3 E90 dal 2005 al 2012. Realizzate con materiali di alta qualità per garantire prestazioni ottimali e durata nel tempo. Compatibili con dischi freno ventilati da 300mm. Include kit di montaggio con clips e grasso per pastiglie. Certificazione ECE R90 per la massima sicurezza.",
        "keywords": ["pastiglie freno", "brembo", "bmw serie 3", "e90", "freni anteriori"]
    },
    {
        "title": "Kit Frizione Completo LuK per Volkswagen Golf VII 1.6 TDI",
        "description": "Kit frizione completo LuK per Volkswagen Golf VII 1.6 TDI 105CV. Il kit include disco frizione, spingidisco e cuscinetto reggispinta. Progettato per garantire cambi marcia fluidi e durata superiore. Compatibile con motori CAYC, CLHA. Facile installazione con attrezzi standard. Garanzia 24 mesi.",
        "keywords": ["kit frizione", "luk", "volkswagen golf", "1.6 tdi", "frizione"]
    },
    {
        "title": "Ammortizzatori Posteriori Bilstein B4 per Mercedes Classe C W204",
        "description": "Coppia di ammortizzatori posteriori Bilstein B4 per Mercedes Classe C W204 2007-2014. Tecnologia monotubo per prestazioni superiori e comfort di guida ottimale. Resistenti alla corrosione grazie al rivestimento speciale. Compatibili con sospensioni standard e sportive. Installazione plug&play senza modifiche.",
        "keywords": ["ammortizzatori", "bilstein", "mercedes classe c", "w204", "sospensioni"]
    },
    {
        "title": "Filtro Olio Mann W712/75 per Audi A4 B8 2.0 TDI",
        "description": "Filtro olio motore Mann Filter W712/75 per Audi A4 B8 2.0 TDI. Filtrazione superiore per proteggere il motore da impurità e particelle. Materiale filtrante di alta qualità per massima efficienza. Compatibile con oli sintetici e semi-sintetici. Facile sostituzione durante il tagliando.",
        "keywords": ["filtro olio", "mann filter", "audi a4", "b8", "2.0 tdi"]
    },
    {
        "title": "Cinghia Distribuzione Gates per Fiat Punto 1.3 Multijet",
        "description": "Cinghia distribuzione Gates PowerGrip per Fiat Punto 1.3 Multijet 75CV. Realizzata in gomma HNBR per resistenza estrema alle alte temperature. Denti rinforzati per trasmissione precisa. Compatibile con motori 188A9.000. Sostituzione raccomandata ogni 120.000 km.",
        "keywords": ["cinghia distribuzione", "gates", "fiat punto", "1.3 multijet", "distribuzione"]
    },
    {
        "title": "Candele NGK Iridium per Honda Civic Type R FK8 2.0 VTEC Turbo",
        "description": "Set 4 candele NGK Iridium IX per Honda Civic Type R FK8 2.0 VTEC Turbo 320CV. Elettrodo centrale in iridio per accensione ottimale e durata superiore. Migliori prestazioni e consumi ridotti. Resistenza alle alte temperature del motore turbo. Compatibili con centralina originale.",
        "keywords": ["candele", "ngk iridium", "honda civic type r", "fk8", "vtec turbo"]
    },
    {
        "title": "Dischi Freno Zimmermann Sport per Alfa Romeo Giulia Quadrifoglio",
        "description": "Coppia dischi freno anteriori Zimmermann Sport per Alfa Romeo Giulia Quadrifoglio 2.9 V6 Bi-Turbo. Dischi forati e baffati per massimo raffreddamento. Trattamento geomet per resistenza alla corrosione. Diametro 350mm, spessore 32mm. Prestazioni racing per uso stradale.",
        "keywords": ["dischi freno", "zimmermann sport", "alfa romeo giulia", "quadrifoglio", "freni sportivi"]
    },
    {
        "title": "Olio Motore Castrol Edge 5W-30 C3 Longlife 5 Litri",
        "description": "Olio motore sintetico Castrol Edge 5W-30 C3 in confezione da 5 litri. Formula Fluid Titanium per protezione estrema del motore. Compatibile con filtri antiparticolato DPF. Specifiche ACEA C3, API SN/CF. Adatto per motori benzina e diesel Euro 5 e Euro 6. Intervalli di sostituzione estesi.",
        "keywords": ["olio motore", "castrol edge", "5w-30", "sintetico", "longlife"]
    },
    {
        "title": "Batteria Auto Bosch S5 AGM 95Ah 850A per BMW X5 F15",
        "description": "Batteria auto Bosch S5 AGM 95Ah 850A per BMW X5 F15 con sistema Start&Stop. Tecnologia AGM per cicli di carica/scarica frequenti. Resistente alle vibrazioni e alle temperature estreme. Manutenzione zero, completamente sigillata. Dimensioni: 353x175x190mm. Garanzia 4 anni.",
        "keywords": ["batteria auto", "bosch s5 agm", "95ah", "bmw x5", "start stop"]
    },
    {
        "title": "Pneumatici Michelin Pilot Sport 4 225/45 R17 94Y XL",
        "description": "Set 4 pneumatici estivi Michelin Pilot Sport 4 225/45 R17 94Y XL. Tecnologia Dynamic Response per handling preciso e frenata ridotta. Mescola bi-compound per grip ottimale su asciutto e bagnato. Struttura rinforzata XL per carichi elevati. Ideali per auto sportive e berline premium.",
        "keywords": ["pneumatici", "michelin pilot sport 4", "225/45 r17", "estivi", "sportivi"]
    }
]

# Keywords SEO di esempio per il settore automotive
SAMPLE_SEO_KEYWORDS = {
    "ricambi_auto": [
        "ricambi auto", "ricambi originali", "ricambi aftermarket", "ricambi auto online",
        "pezzi di ricambio", "ricambi economici", "ricambi garantiti", "ricambi auto usati"
    ],
    "freni": [
        "pastiglie freno", "dischi freno", "freni auto", "sistema frenante",
        "freni anteriori", "freni posteriori", "freni sportivi", "kit freni"
    ],
    "motore": [
        "ricambi motore", "filtri motore", "cinghia distribuzione", "guarnizioni motore",
        "pistoni", "valvole", "candele", "bobine accensione"
    ],
    "sospensioni": [
        "ammortizzatori", "molle sospensioni", "sospensioni auto", "kit sospensioni",
        "barre stabilizzatrici", "silent block", "sospensioni sportive"
    ],
    "pneumatici": [
        "pneumatici auto", "gomme auto", "pneumatici estivi", "pneumatici invernali",
        "pneumatici all season", "cerchi auto", "cerchi in lega"
    ],
    "oli_lubrificanti": [
        "olio motore", "olio cambio", "liquido freni", "liquido raffreddamento",
        "olio sintetico", "additivi auto", "lubrificanti auto"
    ]
}

# Brand automotive più comuni
AUTOMOTIVE_BRANDS = [
    # Marchi italiani
    "Alfa Romeo", "Ferrari", "Fiat", "Lancia", "Maserati", "Lamborghini",
    
    # Marchi tedeschi
    "Audi", "BMW", "Mercedes", "Mercedes-Benz", "Volkswagen", "Porsche",
    "Opel", "Smart", "Mini",
    
    # Marchi francesi
    "Peugeot", "Renault", "Citroen", "DS",
    
    # Marchi giapponesi
    "Toyota", "Honda", "Nissan", "Mazda", "Subaru", "Mitsubishi", "Lexus", "Infiniti",
    
    # Marchi coreani
    "Hyundai", "Kia", "Genesis",
    
    # Marchi americani
    "Ford", "Chevrolet", "Jeep", "Chrysler", "Dodge", "Cadillac",
    
    # Marchi svedesi
    "Volvo", "Saab",
    
    # Marchi cechi
    "Skoda",
    
    # Marchi spagnoli
    "Seat",
    
    # Marchi britannici
    "Land Rover", "Range Rover", "Jaguar", "Bentley", "Rolls-Royce", "Aston Martin"
]

# Fornitori di ricambi più comuni
PARTS_SUPPLIERS = [
    # Freni
    "Brembo", "ATE", "TRW", "Ferodo", "Textar", "Pagid", "Zimmermann",
    
    # Filtri
    "Mann Filter", "Mahle", "Bosch", "Fram", "Purflux", "UFI", "Hengst",
    
    # Sospensioni
    "Bilstein", "Sachs", "Monroe", "KYB", "Koni", "Eibach", "H&R",
    
    # Frizione
    "LuK", "Sachs", "Valeo", "Exedy", "Clutch Pro",
    
    # Distribuzione
    "Gates", "Dayco", "Contitech", "INA", "SKF", "Febi",
    
    # Candele
    "NGK", "Bosch", "Champion", "Denso", "Beru",
    
    # Oli
    "Castrol", "Mobil", "Shell", "Total", "Eni", "Motul", "Liqui Moly",
    
    # Batterie
    "Bosch", "Varta", "Exide", "Yuasa", "Banner",
    
    # Pneumatici
    "Michelin", "Continental", "Pirelli", "Bridgestone", "Goodyear", "Dunlop", "Yokohama"
]

# Configurazioni di test per diversi scenari
TEST_SCENARIOS = {
    "new_product_existing_category": {
        "product": {
            "title": "Pastiglie Freno Posteriori Ferodo per Toyota Yaris 2020",
            "description": "Pastiglie freno posteriori Ferodo per Toyota Yaris 2020. Materiale organico per frenata silenziosa."
        },
        "expected_category": ["Ricambi Auto", "Freni", "Pastiglie Freno", "Pastiglie Posteriori"]
    },
    "new_product_new_subcategory": {
        "product": {
            "title": "Sensore Parcheggio Ultrasonico per Audi Q7 2018",
            "description": "Sensore di parcheggio ultrasonico originale per Audi Q7 2018. Frequenza 40kHz, range 0.3-2.5m."
        },
        "expected_category": ["Ricambi Auto", "Elettrico", "Sensori", "Sensori Parcheggio"]
    },
    "new_main_category": {
        "product": {
            "title": "Casco Integrale AGV K6 per Motociclismo",
            "description": "Casco integrale AGV K6 per motociclismo. Calotta in fibra di carbonio, visiera antigraffio."
        },
        "expected_category": ["Accessori Moto", "Caschi", "Caschi Integrali"]
    },
    "multilingual_product": {
        "product": {
            "title": "Brake Pads Front Brembo BMW 3 Series E90 320d",
            "description": "Front brake pads Brembo for BMW 3 Series E90 320d. High performance ceramic compound for optimal braking."
        },
        "expected_category": ["Ricambi Auto", "Freni", "Pastiglie Freno", "Pastiglie Anteriori"]
    }
}

# Metriche SEO di esempio
SAMPLE_SEO_METRICS = {
    "pastiglie freno": {
        "search_volume": 8100,
        "competition": 0.65,
        "difficulty": 45,
        "cpc": 1.20
    },
    "ricambi auto": {
        "search_volume": 22200,
        "competition": 0.78,
        "difficulty": 62,
        "cpc": 0.95
    },
    "ammortizzatori": {
        "search_volume": 5400,
        "competition": 0.58,
        "difficulty": 38,
        "cpc": 1.45
    },
    "filtro olio": {
        "search_volume": 12100,
        "competition": 0.52,
        "difficulty": 35,
        "cpc": 0.85
    },
    "pneumatici auto": {
        "search_volume": 18300,
        "competition": 0.82,
        "difficulty": 58,
        "cpc": 2.10
    }
}

def get_sample_data():
    """Restituisce tutti i dati di esempio"""
    return {
        "category_tree": SAMPLE_CATEGORY_TREE,
        "products": SAMPLE_PRODUCTS,
        "seo_keywords": SAMPLE_SEO_KEYWORDS,
        "brands": AUTOMOTIVE_BRANDS,
        "suppliers": PARTS_SUPPLIERS,
        "test_scenarios": TEST_SCENARIOS,
        "seo_metrics": SAMPLE_SEO_METRICS
    }

def get_random_product():
    """Restituisce un prodotto casuale per i test"""
    import random
    return random.choice(SAMPLE_PRODUCTS)

def get_category_by_path(path: List[str]) -> Dict:
    """Naviga nell'albero delle categorie seguendo il path"""
    current = SAMPLE_CATEGORY_TREE
    for category in path:
        if category in current:
            current = current[category]
        else:
            return {}
    return current