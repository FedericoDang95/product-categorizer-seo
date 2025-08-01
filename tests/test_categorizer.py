import unittest
import sys
import os

# Aggiungi il path src per importare i moduli
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

from product_categorizer import ProductCategorizer, ProductAnalysis, CategoryResult
from nlp_analyzer import MultilingualNLPAnalyzer
from seo_optimizer import SEOOptimizer
from utils import TextProcessor, CategoryUtils, ValidationUtils
from sample_data import SAMPLE_CATEGORY_TREE, SAMPLE_PRODUCTS, TEST_SCENARIOS

class TestProductCategorizer(unittest.TestCase):
    """Test per il ProductCategorizer"""
    
    def setUp(self):
        """Setup per ogni test"""
        self.categorizer = ProductCategorizer()
        self.sample_tree = SAMPLE_CATEGORY_TREE.copy()
    
    def test_analyze_product_basic(self):
        """Test analisi base di un prodotto"""
        product = SAMPLE_PRODUCTS[0]  # Pastiglie freno BMW
        
        analysis = self.categorizer.analyze_product(
            title=product['title'],
            description=product['description']
        )
        
        self.assertIsInstance(analysis, ProductAnalysis)
        self.assertIn('bmw', analysis.brands)
        self.assertIn('freno', ' '.join(analysis.keywords).lower())
        self.assertEqual(analysis.language, 'it')
    
    def test_categorize_existing_category(self):
        """Test categorizzazione in categoria esistente"""
        product = SAMPLE_PRODUCTS[0]  # Pastiglie freno BMW
        
        result = self.categorizer.categorize_product(
            title=product['title'],
            description=product['description'],
            current_tree=self.sample_tree
        )
        
        self.assertIsInstance(result, CategoryResult)
        self.assertEqual(result.main_category, "Ricambi Auto")
        self.assertIn("Freni", result.subcategory_path)
        self.assertIn("Pastiglie", result.subcategory_path)
    
    def test_create_new_subcategory(self):
        """Test creazione nuova sottocategoria"""
        # Prodotto che richiede nuova sottocategoria
        title = "Sensore Parcheggio Ultrasonico BMW X5"
        description = "Sensore di parcheggio ultrasonico per BMW X5. Tecnologia avanzata per assistenza parcheggio."
        
        result = self.categorizer.categorize_product(
            title=title,
            description=description,
            current_tree=self.sample_tree
        )
        
        self.assertIsInstance(result, CategoryResult)
        # Dovrebbe creare una nuova sottocategoria sotto Elettrico > Sensori
        self.assertIn("Sensori", result.subcategory_path)
    
    def test_multilingual_analysis(self):
        """Test analisi multilingua"""
        # Prodotto in inglese
        title = "Brake Pads Front BMW 3 Series E90"
        description = "Front brake pads for BMW 3 Series E90. High performance ceramic compound."
        
        analysis = self.categorizer.analyze_product(title, description)
        
        self.assertEqual(analysis.language, 'en')
        self.assertIn('bmw', analysis.brands)
    
    def test_seo_optimization(self):
        """Test ottimizzazione SEO"""
        product = SAMPLE_PRODUCTS[0]
        
        result = self.categorizer.categorize_product(
            title=product['title'],
            description=product['description'],
            current_tree=self.sample_tree,
            seo_keywords=product.get('keywords', [])
        )
        
        self.assertIsInstance(result.seo_tags, list)
        self.assertGreater(len(result.seo_tags), 0)
        # Dovrebbe contenere keywords rilevanti
        seo_text = ' '.join(result.seo_tags).lower()
        self.assertIn('freno', seo_text)
    
    def test_category_tree_update(self):
        """Test aggiornamento albero categorie"""
        original_tree = self.sample_tree.copy()
        
        # Prodotto che dovrebbe creare nuova categoria
        title = "Casco Moto AGV K6"
        description = "Casco integrale per motociclismo AGV K6. Protezione massima per motociclisti."
        
        result = self.categorizer.categorize_product(
            title=title,
            description=description,
            current_tree=self.sample_tree
        )
        
        # L'albero dovrebbe essere stato aggiornato
        self.assertIsInstance(result.updated_tree, dict)
        # Potrebbe aver creato una nuova categoria principale o sottocategoria
        self.assertNotEqual(original_tree, result.updated_tree)

class TestNLPAnalyzer(unittest.TestCase):
    """Test per MultilingualNLPAnalyzer"""
    
    def setUp(self):
        self.analyzer = MultilingualNLPAnalyzer()
    
    def test_language_detection(self):
        """Test rilevamento lingua"""
        italian_text = "Pastiglie freno per BMW Serie 3"
        english_text = "Brake pads for BMW 3 Series"
        
        lang_it = self.analyzer.detect_language(italian_text)
        lang_en = self.analyzer.detect_language(english_text)
        
        self.assertEqual(lang_it, 'it')
        self.assertEqual(lang_en, 'en')
    
    def test_entity_extraction(self):
        """Test estrazione entità"""
        text = "Pastiglie freno Brembo per BMW Serie 3 E90 2008"
        
        entities = self.analyzer.extract_entities(text)
        
        self.assertIn('brands', entities)
        self.assertIn('years', entities)
        self.assertIn('product_categories', entities)
        
        # Verifica che abbia trovato BMW come brand
        brands = [brand.lower() for brand in entities['brands']]
        self.assertIn('bmw', brands)
    
    def test_keyword_generation(self):
        """Test generazione keywords SEO"""
        text = "Pastiglie freno anteriori per BMW Serie 3"
        
        keywords = self.analyzer.generate_seo_keywords(text)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)
        
        # Dovrebbe contenere keywords rilevanti
        keywords_text = ' '.join(keywords).lower()
        self.assertIn('freno', keywords_text)

class TestSEOOptimizer(unittest.TestCase):
    """Test per SEOOptimizer"""
    
    def setUp(self):
        self.optimizer = SEOOptimizer()
    
    def test_keyword_analysis(self):
        """Test analisi keywords"""
        keywords = ["pastiglie freno", "ricambi auto", "bmw"]
        
        analysis = self.optimizer.analyze_keywords(keywords)
        
        self.assertIsInstance(analysis, dict)
        for keyword in keywords:
            self.assertIn(keyword, analysis)
            self.assertIn('search_volume', analysis[keyword])
            self.assertIn('competition', analysis[keyword])
    
    def test_category_seo_analysis(self):
        """Test analisi SEO categoria"""
        category_path = ["Ricambi Auto", "Freni", "Pastiglie Freno"]
        keywords = ["pastiglie freno", "freni auto"]
        
        seo_analysis = self.optimizer.analyze_category_seo(category_path, keywords)
        
        self.assertIsNotNone(seo_analysis)
        self.assertIsInstance(seo_analysis.primary_keywords, list)
        self.assertIsInstance(seo_analysis.long_tail_keywords, list)
    
    def test_meta_tags_generation(self):
        """Test generazione meta tags"""
        category = "Pastiglie Freno"
        keywords = ["pastiglie freno", "bmw", "ricambi auto"]
        
        meta_tags = self.optimizer.generate_meta_tags(category, keywords)
        
        self.assertIn('title', meta_tags)
        self.assertIn('description', meta_tags)
        self.assertIn('keywords', meta_tags)
        
        # Verifica lunghezza title
        self.assertLessEqual(len(meta_tags['title']), 60)
        # Verifica lunghezza description
        self.assertLessEqual(len(meta_tags['description']), 160)

class TestUtils(unittest.TestCase):
    """Test per le utilità"""
    
    def test_text_processor(self):
        """Test TextProcessor"""
        processor = TextProcessor()
        
        # Test pulizia testo
        dirty_text = "  Testo   con    spazi   multipli  \n\r\t  "
        clean_text = processor.clean_text(dirty_text)
        self.assertEqual(clean_text, "Testo con spazi multipli")
        
        # Test estrazione keywords
        text = "Pastiglie freno Brembo per BMW Serie 3"
        keywords = processor.extract_keywords(text)
        self.assertIn('pastiglie', keywords)
        self.assertIn('freno', keywords)
        self.assertIn('brembo', keywords)
    
    def test_category_utils(self):
        """Test CategoryUtils"""
        utils = CategoryUtils()
        
        # Test normalizzazione nome categoria
        name = "  pastiglie   FRENO  "
        normalized = utils.normalize_category_name(name)
        self.assertEqual(normalized, "Pastiglie Freno")
        
        # Test costruzione path
        categories = ["Ricambi Auto", "Freni", "Pastiglie"]
        path = utils.build_category_path(categories)
        self.assertEqual(path, "Ricambi Auto > Freni > Pastiglie")
        
        # Test parsing path
        parsed = utils.parse_category_path(path)
        self.assertEqual(parsed, categories)
    
    def test_validation_utils(self):
        """Test ValidationUtils"""
        utils = ValidationUtils()
        
        # Test validazione prodotto valido
        valid_product = {
            'title': 'Pastiglie freno per BMW',
            'description': 'Pastiglie freno di alta qualità per BMW Serie 3. Materiale ceramico per prestazioni ottimali.'
        }
        is_valid, errors = utils.validate_product_data(valid_product)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Test validazione prodotto non valido
        invalid_product = {
            'title': 'Corto',  # Troppo corto
            'description': 'Breve'  # Troppo breve
        }
        is_valid, errors = utils.validate_product_data(invalid_product)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)

class TestIntegration(unittest.TestCase):
    """Test di integrazione"""
    
    def setUp(self):
        self.categorizer = ProductCategorizer()
    
    def test_full_workflow(self):
        """Test workflow completo"""
        # Usa uno scenario di test
        scenario = TEST_SCENARIOS['new_product_existing_category']
        product = scenario['product']
        
        # Esegui categorizzazione completa
        result = self.categorizer.categorize_product(
            title=product['title'],
            description=product['description'],
            current_tree=SAMPLE_CATEGORY_TREE.copy()
        )
        
        # Verifica risultato
        self.assertIsInstance(result, CategoryResult)
        self.assertIsNotNone(result.main_category)
        self.assertIsNotNone(result.subcategory_path)
        self.assertIsInstance(result.seo_tags, list)
        self.assertIsInstance(result.updated_tree, dict)
        
        # Verifica che la categorizzazione sia sensata
        self.assertEqual(result.main_category, "Ricambi Auto")
        self.assertIn("Freni", result.subcategory_path)
    
    def test_batch_processing(self):
        """Test elaborazione batch"""
        products = SAMPLE_PRODUCTS[:3]  # Primi 3 prodotti
        results = []
        
        for product in products:
            result = self.categorizer.categorize_product(
                title=product['title'],
                description=product['description'],
                current_tree=SAMPLE_CATEGORY_TREE.copy()
            )
            results.append(result)
        
        # Verifica che tutti i prodotti siano stati categorizzati
        self.assertEqual(len(results), 3)
        for result in results:
            self.assertIsInstance(result, CategoryResult)
            self.assertIsNotNone(result.main_category)

def run_tests():
    """Esegue tutti i test"""
    # Crea test suite
    test_classes = [
        TestProductCategorizer,
        TestNLPAnalyzer,
        TestSEOOptimizer,
        TestUtils,
        TestIntegration
    ]
    
    suite = unittest.TestSuite()
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Esegui i test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("🧪 Avvio test del sistema di categorizzazione prodotti...\n")
    
    try:
        success = run_tests()
        
        if success:
            print("\n✅ Tutti i test sono passati con successo!")
        else:
            print("\n❌ Alcuni test sono falliti.")
            
    except Exception as e:
        print(f"\n💥 Errore durante l'esecuzione dei test: {e}")
        print("\n⚠️ Nota: Alcuni test potrebbero fallire se le dipendenze NLP non sono installate.")
        print("Per installare le dipendenze: pip install -r requirements.txt")