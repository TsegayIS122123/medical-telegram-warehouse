
import os
import json
import psycopg2
from datetime import datetime

print("="*60)
print("📊 LOADING TO POSTGRESQL (PORT 5433)")
print("="*60)

try:
    # Connect to PostgreSQL on PORT 5433
    conn = psycopg2.connect(
        host="localhost",
        database="medical_warehouse",
        user="postgres",
        password="postgres",
        port="5433"  # PORT 5433
    )
    print("✅ Connected to PostgreSQL on port 5433")
    
    cur = conn.cursor()
    
    # Create schema and table
    cur.execute("CREATE SCHEMA IF NOT EXISTS raw;")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS raw.telegram_messages (
        id SERIAL PRIMARY KEY,
        message_id INTEGER,
        channel_name VARCHAR(255),
        message_date TIMESTAMP,
        message_text TEXT,
        has_media BOOLEAN,
        image_path TEXT,
        views INTEGER,
        forwards INTEGER,
        scraped_at TIMESTAMP
    );
    """)
    conn.commit()
    print("✅ Created raw schema and table")
    
    # Load data
    today = datetime.now().strftime('%Y-%m-%d')
    data_dir = f'data/raw/telegram_messages/{today}'
    total = 0
    
    if os.path.exists(data_dir):
        print(f"\n📁 Loading data from: {data_dir}")
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(data_dir, filename)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                
                for msg in messages:
                    cur.execute("""
                    INSERT INTO raw.telegram_messages 
                    (message_id, channel_name, message_date, message_text, 
                     has_media, image_path, views, forwards, scraped_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """, (
                        msg['message_id'],
                        msg['channel_name'],
                        msg['message_date'],
                        msg['message_text'],
                        msg.get('has_media', False),
                        msg.get('image_path'),
                        msg.get('views', 0),
                        msg.get('forwards', 0),
                        msg.get('scraped_at')
                    ))
                    total += 1
        
        conn.commit()
        print(f"✅ Loaded {total} messages")
    
    # Show count
    cur.execute("SELECT COUNT(*) FROM raw.telegram_messages")
    count = cur.fetchone()[0]
    print(f"📊 Total in database: {count}")
    
    # Show by channel
    cur.execute("SELECT channel_name, COUNT(*) FROM raw.telegram_messages GROUP BY channel_name")
    print("\n📈 By channel:")
    for channel, cnt in cur.fetchall():
        print(f"  {channel}: {cnt} messages")
    
    conn.close()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\n💡 SOLUTIONS:")
    print("1. Check if Docker PostgreSQL is running:")
    print("   docker ps | grep medical_postgres")
    print("2. If not running, start it:")
    print("   docker rm medical_postgres 2>/dev/null; docker run -d --name medical_postgres -p 5433:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=medical_warehouse postgres:15")
    print("3. Wait 10 seconds after starting")

print("="*60)
