from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "leadops.db"

def connect(db_path=DB_PATH):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db(db_path=DB_PATH):
    with connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS lead_processing (
            record_id TEXT PRIMARY KEY,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            company TEXT,
            country TEXT,
            source_campaign TEXT,
            consent_status TEXT,
            normalized_email TEXT,
            is_valid INTEGER,
            validation_errors TEXT,
            is_duplicate INTEGER,
            industry TEXT,
            company_size TEXT,
            lead_score INTEGER,
            route_queue TEXT,
            processing_status TEXT,
            processed_at TEXT
        )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lead_email ON lead_processing(normalized_email)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_lead_status ON lead_processing(processing_status)")
