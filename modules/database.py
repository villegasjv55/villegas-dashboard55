"""
database.py - SQLite persistence layer (optional upgrade path to PostgreSQL)
Insurance Sales Performance Dashboard
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "sales.db"


def get_engine(db_url: str = None):
    """Return a SQLAlchemy engine. Defaults to local SQLite."""
    url = db_url or f"sqlite:///{DB_PATH}"
    return create_engine(url, echo=False)


def init_db(engine=None):
    """Create the sales table if it doesn't exist."""
    engine = engine or get_engine()
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                agent_name TEXT,
                lead_source TEXT,
                product_type TEXT,
                lead_status TEXT,
                premium_amount REAL,
                commission_rate REAL,
                region TEXT,
                calls_made INTEGER,
                quote_sent INTEGER,
                policy_sold INTEGER
            )
        """))
        conn.commit()


def csv_to_db(csv_path: str, engine=None):
    """Load a CSV into the SQLite database (replaces existing data)."""
    engine = engine or get_engine()
    init_db(engine)
    df = pd.read_csv(csv_path)
    df.to_sql("sales", con=engine, if_exists="replace", index=False)
    return len(df)


def read_from_db(engine=None) -> pd.DataFrame:
    """Read all sales records from the database into a DataFrame."""
    engine = engine or get_engine()
    return pd.read_sql("SELECT * FROM sales", con=engine, parse_dates=["date"])


def append_record(record: dict, engine=None):
    """Insert a single sales record dict into the database."""
    engine = engine or get_engine()
    df = pd.DataFrame([record])
    df.to_sql("sales", con=engine, if_exists="append", index=False)
