from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from sqlalchemy import text

# Track whether we've ensured vendor columns exist to avoid repeated ALTERs
_vendor_columns_ensured = False

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    global _vendor_columns_ensured
    if not _vendor_columns_ensured:
        try:
            # Ensure the vendors table has the new columns we recently added via migrations
            # This is a safe, idempotent operation: it uses IF NOT EXISTS so it won't fail
            db.execute(text("""
                ALTER TABLE vendors
                ADD COLUMN IF NOT EXISTS hours VARCHAR;
            """))
            db.execute(text("""
                ALTER TABLE vendors
                ADD COLUMN IF NOT EXISTS accepts_meal_plan BOOLEAN DEFAULT true;
            """))
            # If the Barnes & Noble row should accept Raider card, ensure it's set (dev convenience)
            db.execute(text("""
                UPDATE vendors
                SET accepts_raider_card = true
                WHERE name ILIKE 'barnes%noble%';
            """))
            db.commit()
        except Exception:
            # If any of these operations fail (e.g., vendors table doesn't exist), rollback
            try:
                db.rollback()
            except Exception:
                pass
        finally:
            _vendor_columns_ensured = True
    try:
        yield db
    finally:
        db.close()

