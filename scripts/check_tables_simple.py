"""
Check if Task 2 was completed successfully
Simple version without special characters
"""

import sqlite3

print("="*60)
print("CHECKING TASK 2 RESULTS")
print("="*60)

try:
    conn = sqlite3.connect('data/warehouse.db')
    cursor = conn.cursor()
    
    # Check what tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print("Tables found:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  OK {table[0]}: {count} rows")
    
    # Show sample data
    if 'fact_messages' in [t[0] for t in tables]:
        print("\nSample data from fact_messages:")
        cursor.execute("SELECT * FROM fact_messages LIMIT 3")
        for row in cursor.fetchall():
            print(f"  Message ID: {row[0]}, Channel: {row[1]}, Length: {row[3]}")
    
    # Show channels
    if 'dim_channels' in [t[0] for t in tables]:
        print("\nChannels:")
        cursor.execute("SELECT channel_name, channel_type, total_posts FROM dim_channels")
        for row in cursor.fetchall():
            print(f"  {row[0]} ({row[1]}): {row[2]} posts")
    
    conn.close()
    
    print("\n" + "="*60)
    if len(tables) >= 4:
        print("TASK 2 PASSED - All tables created!")
    else:
        print(f"TASK 2 FAILED - Only {len(tables)} tables found (need 4)")
    print("="*60)
    
except Exception as e:
    print(f"Error: {e}")
    print("\nMake sure you ran: python scripts/load_data_simple.py")
