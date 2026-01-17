# scripts/load_to_postgres_real.py
import json
import psycopg2
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def load_real_data():
    """Load REAL scraped data to PostgreSQL."""
    
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        database=os.getenv('POSTGRES_DB')
    )
    cur = conn.cursor()
    
    # Create raw schema
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cur.execute("""
    DROP TABLE IF EXISTS raw.telegram_messages;
    CREATE TABLE raw.telegram_messages (
        message_id INTEGER PRIMARY KEY,
        channel_name VARCHAR(100),
        message_date TIMESTAMP,
        message_text TEXT,
        views INTEGER,
        forwards INTEGER,
        has_media BOOLEAN,
        image_path VARCHAR(500)
    );
    """)
    
    # Load REAL data
    json_files = list(Path("data/real_telegram_messages").glob("**/*.json"))
    
    for json_file in json_files:
        with open(json_file, 'r') as f:
            messages = json.load(f)
        
        for msg in messages:
            cur.execute("""
            INSERT INTO raw.telegram_messages 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (message_id) DO NOTHING
            """, (
                msg['message_id'],
                msg['channel_name'],
                msg['message_date'],
                msg['message_text'],
                msg['views'],
                msg['forwards'],
                msg['has_media'],
                msg['image_path']
            ))
    
    conn.commit()
    
    # Show results
    cur.execute("SELECT COUNT(*) FROM raw.telegram_messages")
    print(f"✅ Loaded {cur.fetchone()[0]} REAL messages to PostgreSQL")
    
    cur.execute("SELECT channel_name, COUNT(*) FROM raw.telegram_messages GROUP BY channel_name")
    print("\n📊 Messages per channel:")
    for channel, count in cur.fetchall():
        print(f"  {channel}: {count}")
    
    conn.close()

if __name__ == "__main__":
    load_real_data()