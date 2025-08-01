"""Test per il categorizzatore di prodotti in italiano"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Aggiungi la directory principale al path per l'importazione dei moduli
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa i moduli da testare
from src.italian_categorizer import ItalianProductCategorizer
from src.validators import ProductInput
from src.exceptions import ProductCategorizerError, InvalidInputError

class TestItalianCategorizer(unittest.TestCase):
    """Test case per il categorizzatore di prodotti in italiano"""
    
    def setUp(self):
        """Inizializza il categorizzatore per i test"""
        self.categorizer = ItalianProductCategorizer()
    
    def test_categorize_product_frizione(self):
        """Test di categorizzazione per un prodotto di frizione"""
        # Crea un input di prodotto per il test
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
        result = self.categorizer.categorize_product(product)
        
        # Verifica i risultati
        self.assertEqual(result.product_id, "12345")
        self.assertEqual(result.language, "it")
        
        # Verifica che la categoria principale sia corretta
        self.assertTrue(any(cat["id"] == "trasmissione" for cat in result.categories))
        
        # Verifica che ci siano parole chiave SEO
        self.assertTrue(len(result.keywords) > 0)
        
        # Verifica che ci siano suggerimenti SEO
        self.assertTrue(len(result.seo_suggestions) > 0)
    
    def test_categorize_product_freni(self):
        """Test di categorizzazione per un prodotto di freni"""
        # Crea un input di prodotto per il test
        product = ProductInput(
            product_id="67890",
            title="Pastiglie Freno Anteriori per Alfa Romeo Giulietta 2.0 JTDM 2010-2020 con Sensore Usura",
            description="Pastiglie freno anteriori di alta qualità per Alfa Romeo Giulietta 2.0 JTDM dal 2010 al 2020. "
                        "Set completo con sensore di usura incluso. Materiale d'attrito ad alte prestazioni per una "
                        "frenata efficace e silenziosa. Compatibili con dischi freno originali.",
            brand="Brembo",
            language="it"
        )
        
        # Categorizza il prodotto
        result = self.categorizer.categorize_product(product)
        
        # Verifica i risultati
        self.assertEqual(result.product_id, "67890")
        self.assertEqual(result.language, "it")
        
        # Verifica che la categoria principale sia corretta
        self.assertTrue(any(cat["id"] == "freni" for cat in result.categories))
        
        # Verifica che ci siano parole chiave SEO
        self.assertTrue(len(result.keywords) > 0)
        
        # Verifica che ci siano suggerimenti SEO
        self.assertTrue(len(result.seo_suggestions) > 0)
    
    def test_categorize_product_motore(self):
        """Test di categorizzazione per un prodotto del motore"""
        # Crea un input di prodotto per il test
        product = ProductInput(
            product_id="24680",
            title="Kit Distribuzione con Pompa Acqua per Fiat 500 1.3 Multijet Diesel 2007-2015",
            description="Kit distribuzione completo con pompa acqua per Fiat 500 1.3 Multijet Diesel dal 2007 al 2015. "
                        "Il kit include cinghia distribuzione, tendicinghia, rullo e pompa acqua. "
                        "Componenti di qualità OEM per garantire affidabilità e durata nel tempo.",
            brand="SKF",
            language="it"
        )
        
        # Categorizza il prodotto
        result = self.categorizer.categorize_product(product)
        
        # Verifica i risultati
        self.assertEqual(result.product_id, "24680")
        self.assertEqual(result.language, "it")
        
        # Verifica che la categoria principale sia corretta
        self.assertTrue(any(cat["id"] == "motore" for cat in result.categories))
        
        # Verifica che ci siano parole chiave SEO
        self.assertTrue(len(result.keywords) > 0)
        
        # Verifica che ci siano suggerimenti SEO
        self.assertTrue(len(result.seo_suggestions) > 0)
    
    def test_invalid_language(self):
        """Test con lingua non italiana"""
        # Crea un input di prodotto con lingua inglese
        product = ProductInput(
            product_id="13579",
            title="Clutch Kit for Fiat Punto 1.2 Petrol 2003-2010",
            description="Complete clutch kit for Fiat Punto 1.2 petrol from 2003 to 2010.",
            brand="Valeo",
            language="en"  # Lingua inglese invece di italiano
        )
        
        # Verifica che venga sollevata l'eccezione corretta
        with self.assertRaises(InvalidInputError):
            self.categorizer.categorize_product(product)
    
    def test_empty_title(self):
        """Test con titolo vuoto"""
        # Crea un input di prodotto con titolo vuoto
        with self.assertRaises(Exception):
            product = ProductInput(
                product_id="13579",
                title="",  # Titolo vuoto
                description="Descrizione di prova",
                brand="Test",
                language="it"
            )
    
    @patch('src.italian_support.analyze_italian_product_title')
    def test_error_handling(self, mock_analyze):
        """Test della gestione degli errori"""
        # Configura il mock per sollevare un'eccezione
        mock_analyze.side_effect = Exception("Errore di test")
        
        # Crea un input di prodotto per il test
        product = ProductInput(
            product_id="12345",
            title="Test Prodotto",
            description="Descrizione di test",
            brand="Test",
            language="it"
        )
        
        # Verifica che venga sollevata l'eccezione corretta
        with self.assertRaises(ProductCategorizerError):
            self.categorizer.categorize_product(product)

class TestItalianSupport(unittest.TestCase):
    """Test case per le funzioni di supporto in italiano"""
    
    def test_analyze_italian_product_title(self):
        """Test dell'analisi del titolo in italiano"""
        from src.italian_support import analyze_italian_product_title
        
        # Analizza un titolo di test
        title = "Kit Frizione Originale per Fiat Punto 1.2 Benzina dal 2003 al 2010"
        analysis = analyze_italian_product_title(title)
        
        # Verifica i risultati
        self.assertEqual(analysis["original"], title)
        self.assertTrue("cleaned" in analysis)
        self.assertTrue("normalized" in analysis)
        self.assertTrue("filtered" in analysis)
        self.assertTrue("stemmed" in analysis)
        self.assertTrue("automotive_terms" in analysis)
        self.assertTrue("compound_words" in analysis)
    
    def test_generate_italian_seo_keywords(self):
        """Test della generazione di parole chiave SEO in italiano"""
        from src.italian_support import generate_italian_seo_keywords
        
        # Genera parole chiave SEO di test
        keywords = generate_italian_seo_keywords(
            "Auto", 
            "Trasmissione", 
            ["kit frizione", "disco frizione", "spingidisco"]
        )
        
        # Verifica i risultati
        self.assertTrue(len(keywords) > 0)
        self.assertTrue(any("frizione" in keyword for keyword in keywords))

if __name__ == '__main__':
    unittest.main()