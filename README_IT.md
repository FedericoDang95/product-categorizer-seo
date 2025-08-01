# Sistema di Categorizzazione Prodotti con Ottimizzazione SEO

## Panoramica

Questo sistema è progettato per categorizzare automaticamente i prodotti in base ai loro titoli e descrizioni, con un focus particolare sull'ottimizzazione SEO. Il sistema è attualmente ottimizzato per la lingua italiana e specificamente per il settore automotive (ricambi auto).

## Caratteristiche

- **Categorizzazione automatica** dei prodotti in base a titolo e descrizione
- **Analisi NLP avanzata** con supporto specifico per la lingua italiana
- **Ottimizzazione SEO** con generazione di parole chiave rilevanti
- **Suggerimenti SEO** per migliorare titoli e descrizioni
- **API RESTful** per l'integrazione con altri sistemi
- **Gestione degli errori robusta** con messaggi di errore dettagliati
- **Monitoraggio delle prestazioni** con metriche dettagliate
- **Validazione degli input** con modelli Pydantic
- **Sicurezza avanzata** con sanitizzazione degli input e limitazione delle richieste

## Requisiti

- Python 3.8 o superiore
- Dipendenze elencate in `requirements.txt`

## Installazione

1. Clona il repository:

```bash
git clone https://github.com/tuoutente/product-categorizer-seo.git
cd product-categorizer-seo
```

2. Crea un ambiente virtuale e attivalo:

```bash
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
```

3. Installa le dipendenze:

```bash
pip install -r requirements.txt
```

4. Copia il file `.env.example` in `.env` e configura le variabili d'ambiente:

```bash
cp .env.example .env
# Modifica il file .env con le tue configurazioni
```

## Utilizzo

### Avvio dell'API

```bash
python src/italian_api.py
```

L'API sarà disponibile all'indirizzo `http://localhost:5000`.

### Esempi di utilizzo dell'API

#### Categorizzazione di un prodotto

```bash
curl -X POST http://localhost:5000/api/categorize \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "12345",
    "title": "Kit Frizione Completo per Fiat Punto 1.2 Benzina 2003-2010",
    "description": "Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina prodotta dal 2003 al 2010.",
    "brand": "Valeo",
    "language": "it"
  }'
```

#### Generazione di parole chiave SEO

```bash
curl -X POST http://localhost:5000/api/seo/keywords \
  -H "Content-Type: application/json" \
  -d '{
    "category": "Auto",
    "subcategory": "Trasmissione",
    "product_terms": ["kit frizione", "disco frizione", "spingidisco"]
  }'
```

#### Analisi di un titolo di prodotto

```bash
curl -X POST http://localhost:5000/api/analyze/title \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Kit Frizione Originale per Fiat Punto 1.2 Benzina dal 2003 al 2010"
  }'
```

### Utilizzo come libreria

Puoi anche utilizzare il sistema come libreria Python:

```python
from src.italian_categorizer import ItalianProductCategorizer
from src.validators import ProductInput

# Inizializza il categorizzatore
categorizer = ItalianProductCategorizer()

# Crea un input di prodotto
product = ProductInput(
    product_id="12345",
    title="Kit Frizione Completo per Fiat Punto 1.2 Benzina 2003-2010",
    description="Kit frizione completo di alta qualità compatibile con Fiat Punto 1.2 benzina.",
    brand="Valeo",
    language="it"
)

# Categorizza il prodotto
result = categorizer.categorize_product(product)

# Stampa i risultati
print(f"Categorie: {result.categories}")
print(f"Parole chiave: {result.keywords}")
print(f"Suggerimenti SEO: {result.seo_suggestions}")
```

## Struttura del progetto

```
product-categorizer-seo/
├── src/
│   ├── __init__.py
│   ├── api.py                  # API principale
│   ├── italian_api.py          # API specifica per l'italiano
│   ├── config.py               # Configurazione generale
│   ├── italian_config.py       # Configurazione specifica per l'italiano
│   ├── exceptions.py           # Definizioni delle eccezioni
│   ├── italian_categorizer.py  # Categorizzatore per l'italiano
│   ├── italian_support.py      # Funzioni di supporto per l'italiano
│   ├── monitoring.py           # Sistema di monitoraggio
│   ├── nlp_analyzer.py         # Analizzatore NLP multilingua
│   ├── product_categorizer.py  # Categorizzatore di prodotti base
│   └── validators.py           # Validatori di input
├── tests/
│   ├── __init__.py
│   ├── test_italian_categorizer.py  # Test per il categorizzatore italiano
│   └── test_api.py             # Test per l'API
├── examples/
│   ├── sample_data.py          # Dati di esempio
│   └── usage_examples.py       # Esempi di utilizzo
├── .env.example                # Esempio di file di configurazione
├── requirements.txt            # Dipendenze
├── README.md                   # Documentazione in inglese
└── README_IT.md                # Documentazione in italiano
```

## Test

Per eseguire i test:

```bash
python -m unittest discover tests
```

Oppure con pytest:

```bash
python -m pytest tests/
```

## Configurazione

Le principali opzioni di configurazione sono disponibili nel file `.env.example`. Ecco alcune delle configurazioni più importanti:

- `API_HOST`: Host su cui eseguire l'API (default: 0.0.0.0)
- `API_PORT`: Porta su cui eseguire l'API (default: 5000)
- `API_DEBUG`: Modalità debug (default: False)
- `MODEL_EMBEDDING`: Modello di embedding da utilizzare
- `SIMILARITY_THRESHOLD`: Soglia di similarità per la corrispondenza delle categorie
- `CONFIDENCE_THRESHOLD`: Soglia di confidenza per l'accettazione delle categorie
- `MAX_CATEGORIES`: Numero massimo di categorie da restituire

## Estensione ad altre lingue

Il sistema è progettato per essere facilmente estendibile ad altre lingue. Per aggiungere il supporto per una nuova lingua, è necessario:

1. Creare un nuovo file di configurazione (es. `french_config.py`)
2. Creare un nuovo file di supporto (es. `french_support.py`)
3. Creare un nuovo categorizzatore (es. `french_categorizer.py`)
4. Aggiungere i test per la nuova lingua

## Contribuire

I contributi sono benvenuti! Per contribuire:

1. Forka il repository
2. Crea un branch per la tua feature (`git checkout -b feature/amazing-feature`)
3. Committa le tue modifiche (`git commit -m 'Aggiunta una feature incredibile'`)
4. Pusha il branch (`git push origin feature/amazing-feature`)
5. Apri una Pull Request

## Licenza

Questo progetto è distribuito con licenza MIT. Vedi il file `LICENSE` per maggiori dettagli.

## Contatti

Per domande o supporto, contatta l'autore del progetto.