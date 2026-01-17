
#!/usr/bin/env python3
"""Setup PostgreSQL database for the project"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode, result.stdout, result.stderr

def main():
    print("="*60)
    print("POSTGRESQL SETUP SCRIPT")
    print("="*60)
    
    # Check if PostgreSQL is installed
    print("\n1. Checking PostgreSQL installation...")
    returncode, stdout, stderr = run_command("psql --version")
    
    if returncode != 0:
        print("❌ PostgreSQL not found or not in PATH")
        print("\n💡 Please install PostgreSQL:")
        print("   Windows: https://www.postgresql.org/download/windows/")
        print("   Mac: brew install postgresql")
        print("   Linux: sudo apt-get install postgresql")
        return 1
    
    print(f"✅ PostgreSQL found: {stdout.strip()}")
    
    # Check if PostgreSQL service is running
    print("\n2. Checking PostgreSQL service...")
    
    if sys.platform == "win32":
        # Windows
        returncode, stdout, stderr = run_command('sc query postgresql')
        if "RUNNING" not in stdout:
            print("❌ PostgreSQL service not running")
            print("\n💡 Start PostgreSQL service:")
            print("   Press Win + R, type 'services.msc'")
            print("   Find 'PostgreSQL' service and start it")
            print("   OR run: net start postgresql-x64-18")
            return 1
    else:
        # Linux/Mac
        returncode, stdout, stderr = run_command('pg_isready')
        if returncode != 0:
            print("❌ PostgreSQL not responding")
            print("\n💡 Start PostgreSQL:")
            print("   Linux: sudo service postgresql start")
            print("   Mac: brew services start postgresql")
            return 1
    
    print("✅ PostgreSQL service is running")
    
    # Create database
    print("\n3. Creating database 'medical_warehouse'...")
    
    # Try to create database using createdb
    returncode, stdout, stderr = run_command('createdb medical_warehouse')
    
    if returncode != 0:
        print(f"⚠️  Could not create database with createdb: {stderr}")
        print("\n💡 Alternative: Connect to PostgreSQL and create manually:")
        print("   psql -U postgres")
        print("   CREATE DATABASE medical_warehouse;")
        print("   \\q")
        
        # Try SQL
        sql = "CREATE DATABASE medical_warehouse;"
        returncode, stdout, stderr = run_command(f'psql -U postgres -c "{sql}"')
        
        if returncode != 0:
            print(f"❌ Failed to create database: {stderr}")
            return 1
    
    print("✅ Database 'medical_warehouse' created")
    
    # Test connection
    print("\n4. Testing database connection...")
    test_sql = "SELECT '✅ PostgreSQL is working!' as status;"
    returncode, stdout, stderr = run_command(f'psql -U postgres -d medical_warehouse -c "{test_sql}"')
    
    if returncode == 0:
        print("✅ Database connection successful")
        print(f"   {stdout.strip()}")
    else:
        print(f"❌ Database connection failed: {stderr}")
        print("\n💡 Set password for postgres user:")
        print("   psql -U postgres")
        print("   ALTER USER postgres WITH PASSWORD 'postgres';")
        print("   \\q")
        return 1
    
    print("\n" + "="*60)
    print("✅ POSTGRESQL SETUP COMPLETE")
    print("="*60)
    print("\n🎯 You can now:")
    print("1. Run scraper: python src/scraper.py")
    print("2. Load to PostgreSQL: python src/loader.py")
    print("3. Run dbt: cd medical_warehouse && dbt run")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
