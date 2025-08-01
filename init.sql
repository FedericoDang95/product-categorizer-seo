-- Inizializzazione del database per Product Categorizer SEO

-- Creazione delle tabelle

-- Tabella delle categorie
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    parent_id INTEGER REFERENCES categories(id),
    level INTEGER NOT NULL DEFAULT 0,
    path TEXT,
    keywords TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indice per ricerca categorie
CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name);
CREATE INDEX IF NOT EXISTS idx_categories_parent_id ON categories(parent_id);
CREATE INDEX IF NOT EXISTS idx_categories_path ON categories(path);

-- Tabella dei prodotti categorizzati
CREATE TABLE IF NOT EXISTS categorized_products (
    id SERIAL PRIMARY KEY,
    product_id VARCHAR(255) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    confidence FLOAT NOT NULL,
    language VARCHAR(10) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indice per ricerca prodotti
CREATE INDEX IF NOT EXISTS idx_categorized_products_product_id ON categorized_products(product_id);
CREATE INDEX IF NOT EXISTS idx_categorized_products_category_id ON categorized_products(category_id);
CREATE INDEX IF NOT EXISTS idx_categorized_products_language ON categorized_products(language);

-- Tabella delle metriche
CREATE TABLE IF NOT EXISTS metrics (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    endpoint VARCHAR(255) NOT NULL,
    response_time FLOAT NOT NULL,
    status_code INTEGER NOT NULL,
    request_size INTEGER,
    response_size INTEGER,
    client_ip VARCHAR(45),
    user_agent TEXT
);

-- Indice per ricerca metriche
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp);
CREATE INDEX IF NOT EXISTS idx_metrics_endpoint ON metrics(endpoint);
CREATE INDEX IF NOT EXISTS idx_metrics_status_code ON metrics(status_code);

-- Tabella dei log degli errori
CREATE TABLE IF NOT EXISTS error_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    level VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    traceback TEXT,
    endpoint VARCHAR(255),
    request_data JSONB,
    client_ip VARCHAR(45)
);

-- Indice per ricerca log errori
CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_error_logs_level ON error_logs(level);

-- Tabella delle keyword SEO
CREATE TABLE IF NOT EXISTS seo_keywords (
    id SERIAL PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    language VARCHAR(10) NOT NULL,
    search_volume INTEGER,
    competition FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indice per ricerca keyword SEO
CREATE INDEX IF NOT EXISTS idx_seo_keywords_keyword ON seo_keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_seo_keywords_category_id ON seo_keywords(category_id);
CREATE INDEX IF NOT EXISTS idx_seo_keywords_language ON seo_keywords(language);

-- Funzione per aggiornare il timestamp di updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger per aggiornare updated_at nelle tabelle
CREATE TRIGGER update_categories_updated_at
BEFORE UPDATE ON categories
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_categorized_products_updated_at
BEFORE UPDATE ON categorized_products
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_seo_keywords_updated_at
BEFORE UPDATE ON seo_keywords
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Inserimento delle categorie di base per l'italiano
INSERT INTO categories (name, parent_id, level, path, keywords)
VALUES ('Ricambi Auto', NULL, 0, 'ricambi_auto', '{auto,ricambi,parti,componenti,veicolo}')
ON CONFLICT DO NOTHING;

-- Recupera l'ID della categoria principale
DO $$
DECLARE
    main_category_id INTEGER;
BEGIN
    SELECT id INTO main_category_id FROM categories WHERE name = 'Ricambi Auto' AND parent_id IS NULL;
    
    -- Inserimento delle sottocategorie di primo livello
    INSERT INTO categories (name, parent_id, level, path, keywords)
    VALUES 
        ('Motore', main_category_id, 1, 'ricambi_auto/motore', '{motore,engine,propulsore,blocco motore}'),
        ('Freni', main_category_id, 1, 'ricambi_auto/freni', '{freni,freno,brake,frenata,impianto frenante}'),
        ('Sospensioni', main_category_id, 1, 'ricambi_auto/sospensioni', '{sospensioni,ammortizzatori,suspension,assetto}'),
        ('Trasmissione', main_category_id, 1, 'ricambi_auto/trasmissione', '{trasmissione,cambio,transmission,frizione}'),
        ('Elettrico', main_category_id, 1, 'ricambi_auto/elettrico', '{elettrico,elettronica,electrical,batteria,centralina}'),
        ('Carrozzeria', main_category_id, 1, 'ricambi_auto/carrozzeria', '{carrozzeria,body,lamierati,paraurti}')
    ON CONFLICT DO NOTHING;
    
    -- Inserimento di alcune keyword SEO di esempio
    INSERT INTO seo_keywords (keyword, category_id, language, search_volume, competition)
    VALUES 
        ('ricambi auto online', main_category_id, 'it', 5000, 0.8),
        ('parti di ricambio auto', main_category_id, 'it', 3500, 0.7),
        ('componenti auto', main_category_id, 'it', 2800, 0.6)
    ON CONFLICT DO NOTHING;
    
    -- Aggiunge sottocategorie di secondo livello per Motore
    DECLARE motor_id INTEGER;
    BEGIN
        SELECT id INTO motor_id FROM categories WHERE name = 'Motore' AND parent_id = main_category_id;
        
        INSERT INTO categories (name, parent_id, level, path, keywords)
        VALUES 
            ('Pistoni', motor_id, 2, 'ricambi_auto/motore/pistoni', '{pistoni,pistone,piston,cilindro}'),
            ('Valvole', motor_id, 2, 'ricambi_auto/motore/valvole', '{valvole,valvola,valve,aspirazione,scarico}'),
            ('Cinghie', motor_id, 2, 'ricambi_auto/motore/cinghie', '{cinghie,cinghia,belt,distribuzione}')
        ON CONFLICT DO NOTHING;
    END;
    
    -- Aggiunge sottocategorie di secondo livello per Freni
    DECLARE brakes_id INTEGER;
    BEGIN
        SELECT id INTO brakes_id FROM categories WHERE name = 'Freni' AND parent_id = main_category_id;
        
        INSERT INTO categories (name, parent_id, level, path, keywords)
        VALUES 
            ('Pastiglie', brakes_id, 2, 'ricambi_auto/freni/pastiglie', '{pastiglie,pastiglia,brake pad,pad}'),
            ('Dischi', brakes_id, 2, 'ricambi_auto/freni/dischi', '{dischi,disco,brake disc,rotor}'),
            ('Pinze', brakes_id, 2, 'ricambi_auto/freni/pinze', '{pinze,pinza,caliper,mordente}')
        ON CONFLICT DO NOTHING;
    END;
    
    -- Aggiunge sottocategorie di secondo livello per Trasmissione
    DECLARE transmission_id INTEGER;
    BEGIN
        SELECT id INTO transmission_id FROM categories WHERE name = 'Trasmissione' AND parent_id = main_category_id;
        
        INSERT INTO categories (name, parent_id, level, path, keywords)
        VALUES 
            ('Frizione', transmission_id, 2, 'ricambi_auto/trasmissione/frizione', '{frizione,clutch,disco frizione}'),
            ('Cambio', transmission_id, 2, 'ricambi_auto/trasmissione/cambio', '{cambio,gearbox,scatola cambio,marce}'),
            ('Differenziale', transmission_id, 2, 'ricambi_auto/trasmissione/differenziale', '{differenziale,differential,ponte}')
        ON CONFLICT DO NOTHING;
    END;
    
END$$;