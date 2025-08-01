"""Test di integrazione completo per il sistema di categorizzazione italiano"""

import unittest
import json
import os
import sys
from pathlib import Path

# Aggiungi il percorso src al PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from italian_categorizer import ItalianProductCategorizer, ItalianProductAnalysis
from italian_support import (
    load_italian_stopwords,
    load_italian_stemming_rules,
    load_italian_compound_words,
    load_italian_automotive_terms,
    load_italian_regional_variants,
    analyze_italian_product_title,
    generate_italian_seo_keywords
)


class TestItalianIntegration(unittest.TestCase):
    """Test di integrazione per tutti i componenti del sistema italiano"""
    
    @classmethod
    def setUpClass(cls):
        """Setup iniziale per tutti i test"""
        cls.categorizer = ItalianProductCategorizer()
        cls.test_data_dir = Path(__file__).parent.parent / 'data'
        
    def test_data_files_exist(self):
        """Verifica che tutti i file di dati esistano"""
        required_files = [
            'italian_stopwords.txt',
            'italian_stemming_rules.txt',
            'italian_compound_words.txt',
            'italian_automotive_terms.txt',
            'italian_regional_variants.txt',
            'italian_categories.json',
            'italian_seo_keywords.json',
            'italian_analysis_rules.json'
        ]
        
        for filename in required_files:
            file_path = self.test_data_dir / filename
            self.assertTrue(file_path.exists(), f"File mancante: {filename}")
            self.assertGreater(file_path.stat().st_size, 0, f"File vuoto: {filename}")
    
    def test_config_file_exists(self):
        """Verifica che il file di configurazione esista"""
        config_path = Path(__file__).parent.parent / 'config' / 'italian_config.json'
        self.assertTrue(config_path.exists(), "File di configurazione mancante")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        self.assertEqual(config['language'], 'it')
        self.assertIn('data_files', config)
        self.assertIn('nlp_settings', config)
        self.assertIn('categorization', config)
    
    def test_stopwords_loading(self):
        """Test caricamento stopwords italiane"""
        stopwords = load_italian_stopwords()
        self.assertIsInstance(stopwords, set)
        self.assertGreater(len(stopwords), 100)
        self.assertIn('il', stopwords)
        self.assertIn('la', stopwords)
        self.assertIn('di', stopwords)
    
    def test_stemming_rules_loading(self):
        """Test caricamento regole di stemming"""
        rules = load_italian_stemming_rules()
        self.assertIsInstance(rules, dict)
        self.assertGreater(len(rules), 50)
        # Verifica alcune regole comuni
        self.assertIn('plurali_maschili', rules)
        self.assertIn('plurali_femminili', rules)
    
    def test_compound_words_loading(self):
        """Test caricamento parole composte"""
        compounds = load_italian_compound_words()
        self.assertIsInstance(compounds, dict)
        self.assertGreater(len(compounds), 100)
        # Verifica alcune parole composte comuni
        automotive_terms = [term for term in compounds.keys() if 'auto' in term.lower()]
        self.assertGreater(len(automotive_terms), 10)
    
    def test_automotive_terms_loading(self):
        """Test caricamento termini automobilistici"""
        terms = load_italian_automotive_terms()
        self.assertIsInstance(terms, dict)
        self.assertGreater(len(terms), 200)
        # Verifica categorie principali
        self.assertIn('motore', terms)
        self.assertIn('freni', terms)
        self.assertIn('trasmissione', terms)
    
    def test_regional_variants_loading(self):
        """Test caricamento varianti regionali"""
        variants = load_italian_regional_variants()
        self.assertIsInstance(variants, dict)
        self.assertGreater(len(variants), 50)
        # Verifica alcune varianti comuni
        self.assertIn('macchina', variants)
        self.assertIn('auto', variants)
    
    def test_categories_json_structure(self):
        """Test struttura del file categorie"""
        categories_path = self.test_data_dir / 'italian_categories.json'
        with open(categories_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn('categories', data)
        self.assertIn('metadata', data)
        
        categories = data['categories']
        self.assertGreater(len(categories), 10)
        
        # Verifica struttura di una categoria
        category = categories[0]
        required_fields = ['id', 'name', 'description', 'keywords', 'subcategories']
        for field in required_fields:
            self.assertIn(field, category)
    
    def test_seo_keywords_json_structure(self):
        """Test struttura del file parole chiave SEO"""
        seo_path = self.test_data_dir / 'italian_seo_keywords.json'
        with open(seo_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn('seo_keywords', data)
        self.assertIn('metadata', data)
        
        seo_keywords = data['seo_keywords']
        self.assertGreater(len(seo_keywords), 5)
        
        # Verifica struttura di una categoria SEO
        category_key = list(seo_keywords.keys())[0]
        category_seo = seo_keywords[category_key]
        required_fields = ['high_volume', 'medium_volume', 'low_volume', 'long_tail']
        for field in required_fields:
            self.assertIn(field, category_seo)
            self.assertIsInstance(category_seo[field], list)
    
    def test_analysis_rules_json_structure(self):
        """Test struttura del file regole di analisi"""
        rules_path = self.test_data_dir / 'italian_analysis_rules.json'
        with open(rules_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        required_sections = [
            'title_analysis',
            'description_analysis',
            'seo_optimization',
            'technical_terms',
            'compatibility',
            'quality_indicators',
            'brand_recognition'
        ]
        
        for section in required_sections:
            self.assertIn(section, data)
    
    def test_categorizer_initialization(self):
        """Test inizializzazione del categorizzatore"""
        self.assertIsNotNone(self.categorizer)
        self.assertEqual(self.categorizer.language, 'it')
    
    def test_product_categorization_integration(self):
        """Test integrazione completa della categorizzazione"""
        test_products = [
            {
                'title': 'Pastiglie Freni Anteriori Brembo per Fiat 500',
                'description': 'Pastiglie freni anteriori originali Brembo per Fiat 500. Materiale ceramico ad alte prestazioni, durata superiore, frenata progressiva e silenziosa.'
            },
            {
                'title': 'Filtro Olio Mann-Filter per Volkswagen Golf',
                'description': 'Filtro olio di alta qualità Mann-Filter compatibile con Volkswagen Golf. Garantisce una filtrazione ottimale e protezione del motore.'
            },
            {
                'title': 'Ammortizzatori Posteriori Sachs per BMW Serie 3',
                'description': 'Coppia di ammortizzatori posteriori Sachs per BMW Serie 3. Tecnologia monotubo, gas ad alta pressione, comfort di guida superiore.'
            }
        ]
        
        for product in test_products:
            result = self.categorizer.categorize_product(
                title=product['title'],
                description=product['description']
            )
            
            self.assertIsInstance(result, ItalianProductAnalysis)
            self.assertGreater(result.confidence, 0.5)
            self.assertIsNotNone(result.primary_category)
            self.assertIsInstance(result.seo_keywords, list)
            self.assertGreater(len(result.seo_keywords), 0)
    
    def test_title_analysis_integration(self):
        """Test integrazione analisi titoli"""
        test_titles = [
            'Pastiglie Freni Brembo Fiat 500',
            'SUPER OFFERTA!!! Filtro Olio Mann-Filter VW Golf !!!',
            'Ammortizzatori Sachs BMW Serie 3 E90 Posteriori Gas Monotubo'
        ]
        
        for title in test_titles:
            analysis = analyze_italian_product_title(title)
            
            self.assertIsInstance(analysis, dict)
            self.assertIn('score', analysis)
            self.assertIn('suggestions', analysis)
            self.assertIn('issues', analysis)
            self.assertIsInstance(analysis['score'], (int, float))
            self.assertGreaterEqual(analysis['score'], 0)
            self.assertLessEqual(analysis['score'], 100)
    
    def test_seo_keywords_generation_integration(self):
        """Test integrazione generazione parole chiave SEO"""
        test_data = [
            {
                'category': 'freni',
                'brand': 'Brembo',
                'product_type': 'pastiglie'
            },
            {
                'category': 'motore',
                'brand': 'Mann-Filter',
                'product_type': 'filtro olio'
            },
            {
                'category': 'sospensioni',
                'brand': 'Sachs',
                'product_type': 'ammortizzatori'
            }
        ]
        
        for data in test_data:
            keywords = generate_italian_seo_keywords(
                category=data['category'],
                brand=data['brand'],
                product_type=data['product_type']
            )
            
            self.assertIsInstance(keywords, list)
            self.assertGreater(len(keywords), 5)
            
            # Verifica che le parole chiave contengano elementi rilevanti
            keywords_text = ' '.join(keywords).lower()
            self.assertIn(data['brand'].lower(), keywords_text)
            self.assertIn(data['product_type'].lower(), keywords_text)
    
    def test_performance_benchmarks(self):
        """Test prestazioni del sistema"""
        import time
        
        test_product = {
            'title': 'Kit Frizione Completo LUK per Volkswagen Golf 1.9 TDI',
            'description': '''Kit frizione completo LUK per Volkswagen Golf 1.9 TDI.
            Il kit include disco frizione, spingidisco e cuscinetto reggispinta.
            Materiale di alta qualità, durata garantita, facile installazione.
            Compatibile con Golf IV, Golf V, Bora, Caddy, Touran.
            Codice originale: 624 3052 00. Garanzia 2 anni.'''
        }
        
        # Test velocità di categorizzazione
        start_time = time.time()
        result = self.categorizer.categorize_product(
            title=test_product['title'],
            description=test_product['description']
        )
        end_time = time.time()
        
        processing_time = end_time - start_time
        self.assertLess(processing_time, 5.0, "Categorizzazione troppo lenta")
        
        # Test velocità di analisi titolo
        start_time = time.time()
        title_analysis = analyze_italian_product_title(test_product['title'])
        end_time = time.time()
        
        analysis_time = end_time - start_time
        self.assertLess(analysis_time, 1.0, "Analisi titolo troppo lenta")
    
    def test_memory_usage(self):
        """Test utilizzo memoria"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Esegui multiple categorizzazioni
        for i in range(50):
            result = self.categorizer.categorize_product(
                title=f'Test Product {i}',
                description=f'Test description for product {i}'
            )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Verifica che l'aumento di memoria sia ragionevole (< 100MB)
        self.assertLess(memory_increase, 100, "Utilizzo memoria eccessivo")
    
    def test_error_handling(self):
        """Test gestione errori"""
        # Test con input vuoti
        with self.assertRaises(ValueError):
            self.categorizer.categorize_product(title="", description="")
        
        # Test con input None
        with self.assertRaises(ValueError):
            self.categorizer.categorize_product(title=None, description="test")
        
        # Test con input troppo lunghi
        long_text = "a" * 10000
        result = self.categorizer.categorize_product(
            title="Test", 
            description=long_text
        )
        # Dovrebbe gestire gracefully senza errori
        self.assertIsNotNone(result)
    
    def test_multilingual_fallback(self):
        """Test fallback per testo non italiano"""
        english_product = {
            'title': 'Brake Pads for BMW 3 Series',
            'description': 'High quality brake pads for BMW 3 Series. OEM quality, long lasting.'
        }
        
        result = self.categorizer.categorize_product(
            title=english_product['title'],
            description=english_product['description']
        )
        
        # Dovrebbe comunque fornire un risultato, anche se con confidenza più bassa
        self.assertIsNotNone(result)
        self.assertIsInstance(result, ItalianProductAnalysis)


class TestItalianDataQuality(unittest.TestCase):
    """Test per la qualità dei dati italiani"""
    
    def setUp(self):
        self.test_data_dir = Path(__file__).parent.parent / 'data'
    
    def test_stopwords_quality(self):
        """Test qualità delle stopwords"""
        stopwords = load_italian_stopwords()
        
        # Verifica presenza di stopwords comuni
        common_stopwords = ['il', 'la', 'di', 'che', 'e', 'a', 'un', 'per', 'con', 'da']
        for word in common_stopwords:
            self.assertIn(word, stopwords, f"Stopword mancante: {word}")
        
        # Verifica assenza di duplicati
        stopwords_list = list(stopwords)
        self.assertEqual(len(stopwords_list), len(set(stopwords_list)))
    
    def test_automotive_terms_quality(self):
        """Test qualità dei termini automobilistici"""
        terms = load_italian_automotive_terms()
        
        # Verifica presenza di categorie principali
        main_categories = ['motore', 'freni', 'trasmissione', 'sospensioni', 'sterzo']
        for category in main_categories:
            self.assertIn(category, terms, f"Categoria mancante: {category}")
            self.assertIsInstance(terms[category], list)
            self.assertGreater(len(terms[category]), 5)
    
    def test_categories_consistency(self):
        """Test consistenza delle categorie"""
        categories_path = self.test_data_dir / 'italian_categories.json'
        with open(categories_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        categories = data['categories']
        category_ids = [cat['id'] for cat in categories]
        
        # Verifica unicità degli ID
        self.assertEqual(len(category_ids), len(set(category_ids)))
        
        # Verifica che le sottocategorie esistano
        for category in categories:
            for subcategory_id in category['subcategories']:
                self.assertIn(subcategory_id, category_ids, 
                            f"Sottocategoria inesistente: {subcategory_id}")


if __name__ == '__main__':
    # Configura il logging per i test
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Esegui i test
    unittest.main(verbosity=2)