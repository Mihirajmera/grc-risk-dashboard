import sqlite3
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db.seed_data import build_database, DB_PATH

def test_database_seeding(tmp_path, monkeypatch):
    # Use a temporary database file for testing
    test_db = tmp_path / "test_risk_register.db"
    monkeypatch.setattr("db.seed_data.DB_PATH", test_db)
    
    # Run the seeder
    build_database()
    
    # Verify the database exists and has records
    assert test_db.exists()
    
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    
    # Check risks table
    cursor.execute("SELECT COUNT(*) FROM risks")
    risk_count = cursor.fetchone()[0]
    assert risk_count > 0
    
    # Check remediation_actions table
    cursor.execute("SELECT COUNT(*) FROM remediation_actions")
    action_count = cursor.fetchone()[0]
    assert action_count > 0
    
    # Check KRI snapshots table
    cursor.execute("SELECT COUNT(*) FROM kri_snapshots")
    kri_count = cursor.fetchone()[0]
    assert kri_count > 0
    
    conn.close()
