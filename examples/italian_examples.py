"""Esempi di utilizzo del sistema di categorizzazione prodotti in italiano"""

import sys
import os
import json
from typing import Dict, Any, List

# Aggiungi la directory principale al path per l'importazione dei moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa i moduli necessari
from src.italian_categorizer import ItalianProductCategorizer
from src.validators import ProductInput
from src.italian_support import analyze_italian_product_title, generate_italian_seo_keywords

def print_json(data: Any) -> None:
    """Stampa i dati in formato JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def example_categorize_product() -> None:
    """Esempio di categorizzazione di un prodotto"""
    print("\n=== ESEMPIO DI CATEGORIZZAZIONE PRODOTTO ===")
    
    # Inizializza il categorizzatore
    categorizer = ItalianProductCategorizer()
    
    # Crea un input di prodotto
    product = ProductInput(
        product_id="12345",
        title="Kit Frizione Completo per Fiat Punto 1.2 Benzina 2003-2010 con Volano e Cuscinetto Reggispinta",
        description="Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina prodotta dal 2003 al 2010. "
                    "Il kit include disco frizione, spingidisco, volano e cuscinetto reggispinta. "
                    "Prodotto da un fornitore affidabile di ricambi aftermarket con qualità equivalente all'originale.",
        brand="Valeo",
        language="it"
    )
    
    # Categorizza il prodotto
    result = categorizer.categorize_product(product)
    
    # Stampa i risultati
    print("\nRisultato della categorizzazione:")
    print_json({
        "product_id": result.product_id,
        "title": result.title,
        "categories": result.categories,
        "keywords": result.keywords,
        "confidence": result.confidence,
        "seo_suggestions": result.seo_suggestions
    })

def example_multiple_products() -> None:
    """Esempio di categorizzazione di più prodotti"""
    print("\n=== ESEMPIO DI CATEGORIZZAZIONE MULTIPLA ===")
    
    # Inizializza il categorizzatore
    categorizer = ItalianProductCategorizer()
    
    # Lista di prodotti di esempio
    products = [
        ProductInput(
            product_id="12345",
            title="Kit Frizione Completo per Fiat Punto 1.2 Benzina 2003-2010",
            description="Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina.",
            brand="Valeo",
            language="it"
        ),
        ProductInput(
            product_id="67890",
            title="Pastiglie Freno Anteriori per Alfa Romeo Giulietta 2.0 JTDM 2010-2020",
            description="Pastiglie freno anteriori di alta qualità per Alfa Romeo Giulietta 2.0 JTDM.",
            brand="Brembo",
            language="it"
        ),
        ProductInput(
            product_id="24680",
            title="Kit Distribuzione con Pompa Acqua per Fiat 500 1.3 Multijet Diesel 2007-2015",
            description="Kit distribuzione completo con pompa acqua per Fiat 500 1.3 Multijet Diesel.",
            brand="SKF",
            language="it"
        ),
        ProductInput(
            product_id="13579",
            title="Ammortizzatori Posteriori per Lancia Ypsilon 1.2 2011-2021 Coppia",
            description="Coppia di ammortizzatori posteriori per Lancia Ypsilon 1.2 dal 2011 al 2021.",
            brand="Magneti Marelli",
            language="it"
        ),
        ProductInput(
            product_id="97531",
            title="Filtro Abitacolo ai Carboni Attivi per Fiat 500X 1.6 Multijet 2014-2022",
            description="Filtro abitacolo ai carboni attivi per Fiat 500X 1.6 Multijet dal 2014 al 2022.",
            brand="Bosch",
            language="it"
        )
    ]
    
    # Categorizza ogni prodotto
    for i, product in enumerate(products, 1):
        print(f"\nProdotto {i}: {product.title}")
        result = categorizer.categorize_product(product)
        
        # Stampa i risultati principali
        print(f"Categoria principale: {result.categories[0]['name'] if result.categories else 'N/A'}")
        print(f"Confidenza: {result.confidence:.2f}")
        print(f"Parole chiave: {', '.join(result.keywords[:5])}...")

def example_analyze_title() -> None:
    """Esempio di analisi di un titolo di prodotto"""
    print("\n=== ESEMPIO DI ANALISI TITOLO ===")
    
    # Titolo di esempio
    title = "Kit Frizione Originale per Fiat Punto 1.2 Benzina dal 2003 al 2010"
    
    # Analizza il titolo
    analysis = analyze_italian_product_title(title)
    
    # Stampa i risultati
    print("\nAnalisi del titolo:")
    print_json({
        "original": analysis["original"],
        "cleaned": analysis["cleaned"],
        "normalized": analysis["normalized"],
        "filtered": analysis["filtered"],
        "stemmed": analysis["stemmed"],
        "automotive_terms": analysis["automotive_terms"],
        "compound_words": analysis["compound_words"]
    })

def example_generate_seo_keywords() -> None:
    """Esempio di generazione di parole chiave SEO"""
    print("\n=== ESEMPIO DI GENERAZIONE PAROLE CHIAVE SEO ===")
    
    # Parametri di esempio
    category = "Auto"
    subcategory = "Trasmissione"
    product_terms = ["kit frizione", "disco frizione", "spingidisco"]
    
    # Genera parole chiave SEO
    keywords = generate_italian_seo_keywords(category, subcategory, product_terms)
    
    # Stampa i risultati
    print("\nParole chiave SEO generate:")
    print_json(keywords[:20])  # Mostra solo le prime 20 parole chiave

def example_seo_suggestions() -> None:
    """Esempio di suggerimenti SEO"""
    print("\n=== ESEMPIO DI SUGGERIMENTI SEO ===")
    
    # Inizializza il categorizzatore
    categorizer = ItalianProductCategorizer()
    
    # Esempi di prodotti con titoli e descrizioni di diverse lunghezze
    products = [
        # Titolo troppo corto
        ProductInput(
            product_id="12345",
            title="Kit Frizione Fiat",  # Titolo troppo corto
            description="Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina prodotta dal 2003 al 2010.",
            brand="Valeo",
            language="it"
        ),
        # Titolo buono
        ProductInput(
            product_id="67890",
            title="Pastiglie Freno Anteriori per Alfa Romeo Giulietta 2.0 JTDM 2010-2020 con Sensore Usura",  # Titolo buono
            description="Pastiglie freno anteriori di alta qualità per Alfa Romeo Giulietta 2.0 JTDM dal 2010 al 2020.",
            brand="Brembo",
            language="it"
        ),
        # Titolo troppo lungo
        ProductInput(
            product_id="24680",
            title="Kit Distribuzione con Pompa Acqua per Fiat 500 1.3 Multijet Diesel 2007-2015 Completo di Cinghia Distribuzione Tendicinghia Rullo e Pompa Acqua di Alta Qualità Compatibile con Tutti i Modelli",  # Titolo troppo lungo
            description="Kit distribuzione completo con pompa acqua per Fiat 500 1.3 Multijet Diesel.",
            brand="SKF",
            language="it"
        ),
        # Senza descrizione
        ProductInput(
            product_id="13579",
            title="Ammortizzatori Posteriori per Lancia Ypsilon 1.2 2011-2021 Coppia",
            description=None,  # Senza descrizione
            brand="Magneti Marelli",
            language="it"
        )
    ]
    
    # Analizza ogni prodotto
    for i, product in enumerate(products, 1):
        print(f"\nProdotto {i}: {product.title}")
        result = categorizer.categorize_product(product)
        
        # Stampa i suggerimenti SEO
        print("Suggerimenti SEO:")
        for key, suggestion in result.seo_suggestions.items():
            print(f"- {key}: {suggestion}")

def run_all_examples() -> None:
    """Esegue tutti gli esempi"""
    example_categorize_product()
    example_multiple_products()
    example_analyze_title()
    example_generate_seo_keywords()
    example_seo_suggestions()

if __name__ == "__main__":
    run_all_examples()