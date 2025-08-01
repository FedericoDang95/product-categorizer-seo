# 🏷️ Product Categorizer SEO

Sistema intelligente per la categorizzazione automatica di prodotti con ottimizzazione SEO. Analizza titoli e descrizioni di prodotti per assegnarli automaticamente alla categoria più adatta all'interno di una struttura ad albero ottimizzata per la SEO.

## 🎯 Caratteristiche Principali

- **Analisi Semantica Avanzata**: Comprende tipologia, brand, modello e compatibilità dei prodotti
- **Categorizzazione Dinamica**: Crea automaticamente nuove sottocategorie quando necessario
- **Ottimizzazione SEO**: Genera keywords, meta tags e strutture SEO-friendly
- **Supporto Multilingua**: Analizza prodotti in italiano, inglese e altre lingue
- **Riconoscimento Entità**: Identifica brand, modelli, anni e specifiche tecniche
- **API REST**: Interfaccia web per integrazione facile
- **Elaborazione Batch**: Gestisce grandi volumi di prodotti

## 🚀 Installazione Rapida

### Prerequisiti
- Python 3.8+
- pip

### Setup

```bash
# Clona il repository
git clone <repository-url>
cd product-categorizer-seo

# Crea ambiente virtuale
python -m venv venv

# Attiva ambiente virtuale
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Download modelli NLP (opzionale per funzionalità avanzate)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
python -m spacy download it_core_news_sm
python -m spacy download en_core_web_sm
```

## 🔧 Utilizzo

### Utilizzo Base

```python
from src.product_categorizer import ProductCategorizer
from examples.sample_data import SAMPLE_CATEGORY_TREE

# Inizializza il categorizzatore
categorizer = ProductCategorizer()

# Categorizza un prodotto
result = categorizer.categorize_product(
    title="Pastiglie Freno Brembo per BMW Serie 3 E90",
    description="Pastiglie freno anteriori di alta qualità Brembo per BMW Serie 3 E90. Materiale ceramico per prestazioni ottimali e durata superiore.",
    current_tree=SAMPLE_CATEGORY_TREE
)

print(f"Categoria: {result.main_category}")
print(f"Sottocategoria: {result.subcategory_path}")
print(f"SEO Tags: {result.seo_tags}")
```

### API REST

```bash
# Avvia il server
python src/api.py

# Il server sarà disponibile su http://localhost:5000
```

#### Endpoint Principali

- `POST /categorize` - Categorizza un singolo prodotto
- `POST /batch-categorize` - Categorizza più prodotti
- `GET /categories` - Ottieni l'albero delle categorie
- `POST /analyze` - Analisi semantica di un prodotto
- `GET /health` - Stato del sistema

#### Esempio Richiesta

```bash
curl -X POST http://localhost:5000/categorize \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Pastiglie Freno Brembo BMW",
    "description": "Pastiglie freno anteriori per BMW Serie 3",
    "seo_keywords": ["pastiglie freno", "bmw", "ricambi auto"]
  }'
```

## 📊 Struttura del Progetto

```
product-categorizer-seo/
├── src/
│   ├── __init__.py
│   ├── product_categorizer.py    # Classe principale
│   ├── nlp_analyzer.py          # Analisi NLP multilingua
│   ├── seo_optimizer.py         # Ottimizzazione SEO
│   ├── api.py                   # API REST Flask
│   ├── config.py                # Configurazioni
│   └── utils.py                 # Utilità comuni
├── examples/
│   └── sample_data.py           # Dati di esempio
├── tests/
│   └── test_categorizer.py      # Test suite
├── requirements.txt             # Dipendenze
└── README.md                    # Documentazione
```

## 🧠 Come Funziona

### 1. Analisi Semantica
Il sistema analizza titolo e descrizione per estrarre:
- Tipologia di prodotto
- Brand e modello
- Compatibilità e specifiche
- Keywords SEO rilevanti

### 2. Categorizzazione Intelligente
- Cerca la categoria più adatta nell'albero esistente
- Crea dinamicamente nuove sottocategorie se necessario
- Mantiene la struttura SEO-friendly (max 3-4 livelli)

### 3. Ottimizzazione SEO
- Genera keywords primarie e long-tail
- Calcola metriche SEO (volume ricerca, competizione)
- Crea meta tags ottimizzati
- Suggerisce miglioramenti

## 📈 Output Esempio

```json
{
  "categoria_principale": "Ricambi Auto",
  "sottocategoria": "Freni > Pastiglie Freno",
  "tags_seo": [
    "pastiglie freno bmw",
    "ricambi freni serie 3",
    "brembo pastiglie anteriori"
  ],
  "confidence_score": 0.95,
  "seo_metrics": {
    "primary_keywords": ["pastiglie freno", "bmw serie 3"],
    "search_volume": 2400,
    "competition": "medium"
  },
  "nuovo_albero": {
    "Ricambi Auto": {
      "Freni": {
        "Pastiglie Freno": {
          "Pastiglie Anteriori": {},
          "Pastiglie Posteriori": {}
        }
      }
    }
  }
}
```

## 🧪 Test

```bash
# Esegui tutti i test
python tests/test_categorizer.py

# Test specifici
python -m unittest tests.test_categorizer.TestProductCategorizer
```

## ⚙️ Configurazione

Il sistema può essere configurato tramite variabili d'ambiente o modificando `src/config.py`:

```python
# Configurazioni principali
CONFIDENCE_THRESHOLD = 0.7        # Soglia confidenza categorizzazione
MAX_CATEGORY_DEPTH = 4            # Profondità massima albero
SEO_KEYWORDS_LIMIT = 10           # Numero massimo keywords SEO
CACHE_ENABLED = True              # Abilita cache
MULTILINGUAL_SUPPORT = True       # Supporto multilingua
```

## 🌍 Supporto Multilingua

Il sistema supporta:
- **Italiano** (it) - Lingua principale
- **Inglese** (en) - Supporto completo
- **Francese** (fr) - Supporto base
- **Tedesco** (de) - Supporto base
- **Spagnolo** (es) - Supporto base

## 🔌 Integrazioni

### E-commerce Platforms
- WooCommerce
- Magento
- Shopify
- PrestaShop

### CMS
- WordPress
- Drupal
- Joomla

### API Integration
```python
# Esempio integrazione personalizzata
from src.product_categorizer import ProductCategorizer

def integrate_with_ecommerce(products):
    categorizer = ProductCategorizer()
    
    for product in products:
        result = categorizer.categorize_product(
            title=product['name'],
            description=product['description']
        )
        
        # Aggiorna categoria nel tuo sistema
        update_product_category(product['id'], result)
```

## 📚 Esempi Avanzati

### Categorizzazione Batch

```python
from src.api import app
import requests

# Prepara dati
products = [
    {
        "title": "Olio Motore Castrol 5W30",
        "description": "Olio motore sintetico Castrol GTX 5W30 per auto benzina e diesel"
    },
    {
        "title": "Filtro Aria Mann BMW",
        "description": "Filtro aria originale Mann per BMW Serie 3 e Serie 5"
    }
]

# Categorizzazione batch
response = requests.post('http://localhost:5000/batch-categorize', 
                        json={'products': products})
results = response.json()
```

### Analisi SEO Avanzata

```python
from src.seo_optimizer import SEOOptimizer

optimizer = SEOOptimizer()

# Analizza keywords
keywords = ["pastiglie freno", "bmw", "ricambi auto"]
analysis = optimizer.analyze_keywords(keywords)

# Genera meta tags
meta_tags = optimizer.generate_meta_tags(
    category="Pastiglie Freno",
    keywords=keywords
)

print(f"Title: {meta_tags['title']}")
print(f"Description: {meta_tags['description']}")
```

## 🐛 Troubleshooting

### Problemi Comuni

1. **Errore import spaCy**
   ```bash
   python -m spacy download it_core_news_sm
   python -m spacy download en_core_web_sm
   ```

2. **Errore NLTK data**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **Performance lente**
   - Abilita cache in `config.py`
   - Usa modelli NLP più leggeri
   - Considera l'uso di GPU per modelli transformer

## 🤝 Contribuire

1. Fork il repository
2. Crea un branch per la tua feature (`git checkout -b feature/AmazingFeature`)
3. Commit le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri una Pull Request

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## 🙏 Ringraziamenti

- [spaCy](https://spacy.io/) per l'analisi NLP
- [NLTK](https://www.nltk.org/) per il processing del testo
- [scikit-learn](https://scikit-learn.org/) per il machine learning
- [Flask](https://flask.palletsprojects.com/) per l'API REST

## 📞 Supporto

Per supporto, bug report o richieste di feature:
- Apri un issue su GitHub
- Contatta il team di sviluppo

---

**Sviluppato con ❤️ per l'ottimizzazione SEO e la categorizzazione intelligente dei prodotti**