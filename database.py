import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Usa DATABASE_URL se disponibile (es. Render Postgres), altrimenti SQLite locale.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./wordflow.db")

# Render puo fornire URL con schema postgres://, SQLAlchemy richiede postgresql+psycopg2://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

engine_kwargs = {"pool_pre_ping": True}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

# Engine
engine = create_engine(DATABASE_URL, **engine_kwargs)

# Sessione DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base per i modelli
Base = declarative_base()
