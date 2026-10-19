import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("voiceform")

# Database URL configuration (Default to MySQL if available, fallback to SQLite)
MYSQL_URL = os.getenv(
    "MYSQL_DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/voiceform_db"
)
SQLITE_URL = os.getenv(
    "SQLITE_DATABASE_URL",
    "sqlite:///./voiceform.db"
)

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None
Base = declarative_base()

def init_db_engine():
    global engine, SessionLocal
    selected_url = DATABASE_URL
    
    if not selected_url:
        # Try MySQL first
        try:
            test_engine = create_engine(
                MYSQL_URL,
                pool_pre_ping=True,
                connect_args={"connect_timeout": 3}
            )
            with test_engine.connect():
                pass
            engine = test_engine
            selected_url = MYSQL_URL
            print(f"[Database] Successfully connected to MySQL at {MYSQL_URL.split('@')[-1]}")
        except Exception as e:
            print(f"[Database] MySQL connection unavailable ({e}). Falling back to SQLite.")
            selected_url = SQLITE_URL
            engine = create_engine(
                SQLITE_URL,
                connect_args={"check_same_thread": False}
            )
            print(f"[Database] Using SQLite at {SQLITE_URL}")
    else:
        is_sqlite = selected_url.startswith("sqlite")
        connect_args = {"check_same_thread": False} if is_sqlite else {}
        engine = create_engine(selected_url, connect_args=connect_args)
        print(f"[Database] Using configured database: {selected_url}")

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine

def get_db():
    if SessionLocal is None:
        init_db_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
