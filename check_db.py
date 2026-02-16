import psycopg2

print("\n" + "="*50)
print("POSTGRESQL DATABASE CHECK")
print("="*50)

# Try to connect and list databases
try:
    conn = psycopg2.connect(
        host='localhost',
        port=5433,
        user='postgres',
        password='postgres'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Get list of databases
    cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false")
    databases = cur.fetchall()
    
    print("\nDatabases found:")
    for db in databases:
        print(f"  - {db[0]}")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Connection error: {e}")
