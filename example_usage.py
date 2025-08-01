#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esempio di utilizzo del Product Categorizer SEO

Questo script dimostra come utilizzare il sistema di categorizzazione
automatica dei prodotti con ottimizzazione SEO.
"""

import sys
import os
import json
from pprint import pprint

# Aggiungi il path src per importare i moduli
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples'))

from product_categorizer import ProductCategorizer
from nlp_analyzer import MultilingualNLPAnalyzer
from seo_optimizer import SEOOptimizer
from sample_data import SAMPLE_CATEGORY_TREE, SAMPLE_PRODUCTS

def print_separator(title):
    """Stampa un separatore con titolo"""
    print("\n" + "="*60)
    print(f" {title} ")
    print("="*60)

def example_basic_categorization():
    """Esempio di categorizzazione base"""
    print_separator("ESEMPIO 1: Categorizzazione Base")
    
    # Inizializza il categorizzatore
    categorizer = ProductCategorizer()
    
    # Prodotto di esempio
    title = "Pastiglie Freno Brembo per BMW Serie 3 E90 2008-2012"
    description = """
    Pastiglie freno anteriori di alta qualità Brembo per BMW Serie 3 E90.
    Materiale ceramico per prestazioni ottimali e durata superiore.
    Compatibili con modelli dal 2008 al 2012.
    Certificazione ECE R90 per sicurezza garantita.
    """
    
    print(f"📦 Prodotto da categorizzare:")
    print(f"   Titolo: {title}")
    print(f"   Descrizione: {description.strip()}")
    
    # Esegui categorizzazione
    result = categorizer.categorize_product(
        title=title,
        description=description,
        current_tree=SAMPLE_CATEGORY_TREE.copy()
    )
    
    print(f"\n🎯 Risultato Categorizzazione:")
    print(f"   Categoria Principale: {result.main_category}")
    print(f"   Percorso Sottocategoria: {result.subcategory_path}")
    print(f"   Confidence Score: {result.confidence_score:.2f}")
    print(f"   SEO Tags: {', '.join(result.seo_tags)}")
    
    return result

def example_multilingual_analysis():
    """Esempio di analisi multilingua"""
    print_separator("ESEMPIO 2: Analisi Multilingua")
    
    analyzer = MultilingualNLPAnalyzer()
    
    # Prodotti in diverse lingue
    products = [
        {
            "lang": "Italiano",
            "title": "Olio Motore Castrol GTX 5W30 4 Litri",
            "description": "Olio motore sintetico Castrol GTX 5W30 per auto benzina e diesel. Protezione avanzata del motore."
        },
        {
            "lang": "Inglese",
            "title": "Brake Pads Front BMW 3 Series E90",
            "description": "Front brake pads for BMW 3 Series E90. High performance ceramic compound for optimal braking."
        },
        {
            "lang": "Francese",
            "title": "Filtre à Air Mann BMW Série 3",
            "description": "Filtre à air de haute qualité Mann pour BMW Série 3. Améliore les performances du moteur."
        }
    ]
    
    for product in products:
        print(f"\n🌍 Analisi prodotto in {product['lang']}:")
        print(f"   Titolo: {product['title']}")
        
        # Rileva lingua
        detected_lang = analyzer.detect_language(product['title'] + " " + product['description'])
        print(f"   Lingua rilevata: {detected_lang}")
        
        # Estrai entità
        entities = analyzer.extract_entities(product['title'] + " " + product['description'])
        print(f"   Brand rilevati: {', '.join(entities.get('brands', []))}")
        print(f"   Categorie prodotto: {', '.join(entities.get('product_categories', []))}")
        
        # Genera keywords SEO
        keywords = analyzer.generate_seo_keywords(product['title'] + " " + product['description'])
        print(f"   Keywords SEO: {', '.join(keywords[:5])}")

def example_seo_optimization():
    """Esempio di ottimizzazione SEO"""
    print_separator("ESEMPIO 3: Ottimizzazione SEO")
    
    optimizer = SEOOptimizer()
    
    # Keywords di esempio
    keywords = ["pastiglie freno", "bmw serie 3", "ricambi auto", "brembo"]
    
    print(f"🔍 Analisi SEO per keywords: {', '.join(keywords)}")
    
    # Analizza keywords
    keyword_analysis = optimizer.analyze_keywords(keywords)
    
    print(f"\n📊 Metriche Keywords:")
    for keyword, metrics in keyword_analysis.items():
        print(f"   {keyword}:")
        print(f"     - Volume ricerca: {metrics['search_volume']}")
        print(f"     - Competizione: {metrics['competition']}")
        print(f"     - Difficoltà: {metrics['difficulty']}")
        print(f"     - Rilevanza: {metrics['relevance']:.2f}")
    
    # Genera meta tags
    meta_tags = optimizer.generate_meta_tags("Pastiglie Freno BMW", keywords)
    
    print(f"\n🏷️ Meta Tags Generati:")
    print(f"   Title: {meta_tags['title']}")
    print(f"   Description: {meta_tags['description']}")
    print(f"   Keywords: {meta_tags['keywords']}")
    
    # Analisi SEO categoria
    category_path = ["Ricambi Auto", "Freni", "Pastiglie Freno"]
    seo_analysis = optimizer.analyze_category_seo(category_path, keywords)
    
    print(f"\n📈 Analisi SEO Categoria:")
    print(f"   Keywords primarie: {', '.join(seo_analysis.primary_keywords)}")
    print(f"   Keywords long-tail: {', '.join(seo_analysis.long_tail_keywords[:3])}")
    print(f"   Score SEO: {seo_analysis.seo_score:.2f}")

def example_dynamic_category_creation():
    """Esempio di creazione dinamica categorie"""
    print_separator("ESEMPIO 4: Creazione Dinamica Categorie")
    
    categorizer = ProductCategorizer()
    
    # Prodotto che richiede nuova categoria
    title = "Casco Moto AGV K6 Integrale Nero Opaco Taglia L"
    description = """
    Casco integrale per motociclismo AGV K6 in fibra di carbonio.
    Protezione massima per motociclisti sportivi.
    Visiera antigraffio e sistema di ventilazione avanzato.
    Omologazione ECE 22.06 per sicurezza certificata.
    """
    
    print(f"🏍️ Prodotto che richiede nuova categoria:")
    print(f"   Titolo: {title}")
    print(f"   Descrizione: {description.strip()}")
    
    # Albero categorie originale (senza categoria moto)
    original_tree = SAMPLE_CATEGORY_TREE.copy()
    print(f"\n🌳 Categorie esistenti: {list(original_tree.keys())}")
    
    # Esegui categorizzazione
    result = categorizer.categorize_product(
        title=title,
        description=description,
        current_tree=original_tree
    )
    
    print(f"\n🆕 Nuova categorizzazione:")
    print(f"   Categoria Principale: {result.main_category}")
    print(f"   Percorso: {result.subcategory_path}")
    print(f"   Confidence: {result.confidence_score:.2f}")
    
    # Mostra l'albero aggiornato
    new_categories = list(result.updated_tree.keys())
    print(f"\n🌳 Categorie dopo aggiornamento: {new_categories}")
    
    if result.main_category not in original_tree:
        print(f"✨ Creata nuova categoria principale: {result.main_category}")

def example_batch_processing():
    """Esempio di elaborazione batch"""
    print_separator("ESEMPIO 5: Elaborazione Batch")
    
    categorizer = ProductCategorizer()
    
    # Usa prodotti di esempio
    products = SAMPLE_PRODUCTS[:5]  # Primi 5 prodotti
    
    print(f"📦 Elaborazione batch di {len(products)} prodotti...")
    
    results = []
    for i, product in enumerate(products, 1):
        print(f"\n🔄 Elaborazione prodotto {i}/{len(products)}:")
        print(f"   {product['title'][:50]}...")
        
        result = categorizer.categorize_product(
            title=product['title'],
            description=product['description'],
            current_tree=SAMPLE_CATEGORY_TREE.copy(),
            seo_keywords=product.get('keywords', [])
        )
        
        results.append({
            'product': product['title'],
            'category': result.main_category,
            'subcategory': result.subcategory_path,
            'confidence': result.confidence_score,
            'seo_tags': len(result.seo_tags)
        })
        
        print(f"   ✅ Categorizzato in: {result.main_category} > {result.subcategory_path}")
    
    # Statistiche finali
    print(f"\n📊 Statistiche Elaborazione:")
    categories = {}
    total_confidence = 0
    
    for result in results:
        cat = result['category']
        categories[cat] = categories.get(cat, 0) + 1
        total_confidence += result['confidence']
    
    print(f"   Prodotti elaborati: {len(results)}")
    print(f"   Confidence media: {total_confidence/len(results):.2f}")
    print(f"   Categorie utilizzate: {len(categories)}")
    
    for cat, count in categories.items():
        print(f"     - {cat}: {count} prodotti")

def example_api_simulation():
    """Simula l'utilizzo dell'API"""
    print_separator("ESEMPIO 6: Simulazione API")
    
    # Simula una richiesta API
    api_request = {
        "title": "Filtro Olio Mann W712/75 per Volkswagen Golf",
        "description": "Filtro olio di ricambio Mann W712/75 per Volkswagen Golf, Passat e Audi A3. Filtrazione superiore per protezione motore.",
        "seo_keywords": ["filtro olio", "mann", "volkswagen", "golf"],
        "language": "it"
    }
    
    print(f"📡 Richiesta API simulata:")
    print(json.dumps(api_request, indent=2, ensure_ascii=False))
    
    # Elabora con il categorizzatore
    categorizer = ProductCategorizer()
    
    result = categorizer.categorize_product(
        title=api_request['title'],
        description=api_request['description'],
        current_tree=SAMPLE_CATEGORY_TREE.copy(),
        seo_keywords=api_request['seo_keywords']
    )
    
    # Simula risposta API
    api_response = {
        "success": True,
        "data": {
            "categoria_principale": result.main_category,
            "sottocategoria": result.subcategory_path,
            "tags_seo": result.seo_tags,
            "confidence_score": result.confidence_score,
            "language_detected": "it",
            "processing_time_ms": 245
        },
        "metadata": {
            "version": "1.0.0",
            "timestamp": "2024-01-15T10:30:00Z"
        }
    }
    
    print(f"\n📤 Risposta API simulata:")
    print(json.dumps(api_response, indent=2, ensure_ascii=False))

def main():
    """Funzione principale che esegue tutti gli esempi"""
    print("🚀 DEMO: Product Categorizer SEO")
    print("Sistema intelligente per categorizzazione automatica prodotti")
    
    try:
        # Esegui tutti gli esempi
        example_basic_categorization()
        example_multilingual_analysis()
        example_seo_optimization()
        example_dynamic_category_creation()
        example_batch_processing()
        example_api_simulation()
        
        print_separator("DEMO COMPLETATA")
        print("✅ Tutti gli esempi sono stati eseguiti con successo!")
        print("\n💡 Suggerimenti:")
        print("   - Modifica i prodotti di esempio in examples/sample_data.py")
        print("   - Personalizza le configurazioni in src/config.py")
        print("   - Avvia l'API con: python src/api.py")
        print("   - Esegui i test con: python tests/test_categorizer.py")
        
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione: {e}")
        print("\n⚠️ Note:")
        print("   - Assicurati di aver installato tutte le dipendenze")
        print("   - Alcuni modelli NLP potrebbero non essere disponibili")
        print("   - Per installare: pip install -r requirements.txt")
        
        import traceback
        print(f"\n🔍 Dettagli errore:")
        traceback.print_exc()

if __name__ == "__main__":
    main()