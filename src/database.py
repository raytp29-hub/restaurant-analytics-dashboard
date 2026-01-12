import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/restaurants.db")

def init_db():
    """Crea database e tabella se non esistono"""
    
    # 1. Connetti al database (crea file se non esiste)
    conn = sqlite3.connect(DB_PATH)
    
    # 2. Crea "cursore" per eseguire comandi SQL
    cursor = conn.cursor()
    
    # 3. Crea tabella (se non esiste già)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        name TEXT,
        lat REAL,
        lon REAL,
        rating REAL,
        categories TEXT,
        review_count INTEGER,         
        address TEXT,                 
        phone TEXT,                  
        url TEXT,                     
        distance INTEGER,             
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
    
    # 4. Salva modifiche
    conn.commit()
    
    # 5. Chiudi connessione
    conn.close()
    
    print("✅ Database inizializzato!")
    
    
    

def save_to_db(df, city):
    """Salva DataFrame nel database"""
    # Add column city
    df['city'] = city
    
    # Connect to db
    conn = sqlite3.connect(DB_PATH)
    
    
    # Save DataFrame into table
    df.to_sql(
        'restaurants',
        conn,
        if_exists='append',
        index=False
    )
    
    conn.close()
    
    print(f"Saved {len(df)} restaurant per {city}")
    
    
    

def load_from_db(city):
    """Carica dati dal database per una città"""
    
    
    conn = sqlite3.connect(DB_PATH)
    
    query = "SELECT * FROM restaurants WHERE city = ?"
        
    df = pd.read_sql(query, conn, params=(city,))
    
    conn.close()
    
    
    return df




