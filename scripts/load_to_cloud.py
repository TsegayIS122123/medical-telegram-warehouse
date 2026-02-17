import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.loader import DataLoader

# You'll replace this URL after deployment
DATABASE_URL = "postgresql://user:pass@your-render-db-host:5432/medical_warehouse"

print("íº€ Loading data to cloud database...")
loader = DataLoader()
loader.load_json_files('2026-01-17')
print("âœ… Data loaded successfully!")
