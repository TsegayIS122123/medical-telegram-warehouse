"""
Task 2: Load JSON data to SQLite database
Simple version without special characters
"""

import json
import sqlite3
from pathlib import Path

print("="*60)
print("TASK 2: LOADING DATA TO DATABASE")
print("="*60)

# 1. Create database
conn = sqlite3.connect('data/warehouse.db')
cursor = conn.cursor()

# 2. Create raw table
cursor.execute('''
CREATE TABLE IF NOT EXISTS raw_messages (
    message_id INTEGER,
    channel_name TEXT,
    message_date TEXT,
    message_text TEXT,
    views INTEGER,
    forwards INTEGER,
    has_media INTEGER,
    image_path TEXT
)
''')
print("OK Created table: raw_messages")

# 3. Load JSON files
json_files = list(Path('data/raw/telegram_messages').glob('**/*.json'))
total = 0

for file_path in json_files:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for msg in data:
        cursor.execute('''
        INSERT INTO raw_messages VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            msg.get('message_id', 0),
            msg.get('channel_name', ''),
            msg.get('message_date', ''),
            msg.get('message_text', ''),
            msg.get('views', 0),
            msg.get('forwards', 0),
            1 if msg.get('has_media', False) else 0,
            msg.get('image_path', '')
        ))
    
    total += len(data)
    print(f"OK Loaded {len(data)} messages from {file_path.name}")

conn.commit()
print(f"\nTotal messages loaded: {total}")

# 4. Create cleaned table
cursor.execute('''
CREATE TABLE IF NOT EXISTS clean_messages AS
SELECT
    message_id,
    channel_name,
    message_date,
    message_text,
    views,
    forwards,
    has_media,
    image_path,
    LENGTH(message_text) as message_length,
    CASE WHEN image_path IS NOT NULL AND image_path != '' THEN 1 ELSE 0 END as has_image
FROM raw_messages
WHERE message_id IS NOT NULL
''')
print("OK Created table: clean_messages")

# 5. Create channels table
cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_channels AS
SELECT
    ROW_NUMBER() OVER (ORDER BY channel_name) as channel_key,
    channel_name,
    CASE 
        WHEN channel_name LIKE '%cosmetic%' THEN 'Cosmetics'
        WHEN channel_name LIKE '%pharma%' THEN 'Pharmaceutical'
        ELSE 'Medical'
    END as channel_type,
    COUNT(*) as total_posts,
    AVG(views) as avg_views
FROM clean_messages
GROUP BY channel_name
''')
print("OK Created table: dim_channels")

# 6. Create fact table
cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_messages AS
SELECT
    c.message_id,
    ch.channel_key,
    c.message_text,
    c.message_length,
    c.views as view_count,
    c.forwards as forward_count,
    c.has_image
FROM clean_messages c
LEFT JOIN dim_channels ch ON c.channel_name = ch.channel_name
''')
print("OK Created table: fact_messages")

conn.close()

print("\n" + "="*60)
print("TASK 2 COMPLETE!")
print("="*60)
print("Database: data/warehouse.db")
print("Tables created:")
print("  - raw_messages")
print("  - clean_messages")
print("  - dim_channels")
print("  - fact_messages")
print("="*60)
