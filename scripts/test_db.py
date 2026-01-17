import psycopg2

print("Testing database connections...")

# Test warehouse_user
try:
    conn = psycopg2.connect(
        host="localhost",
        database="medical_warehouse",
        user="warehouse_user",
        password="warehouse_pass",
        port="5432"
    )
    print("✅ SUCCESS with warehouse_user/warehouse_pass")
    conn.close()
except Exception as e:
    print(f"❌ FAILED warehouse_user: {e}")

# Test postgres
try:
    conn = psycopg2.connect(
        host="localhost",
        database="medical_warehouse",
        user="postgres",
        password="postgres",
        port="5432"
    )
    print("✅ SUCCESS with postgres/postgres")
    conn.close()
except Exception as e:
    print(f"❌ FAILED postgres: {e}")

# Test default postgres database
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="warehouse_user",
        password="warehouse_pass",
        port="5432"
    )
    print("✅ SUCCESS with database 'postgres'")
    conn.close()
except Exception as e:
    print(f"❌ FAILED: {e}")
