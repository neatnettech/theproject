# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from staging.config import settings
from staging.models import Base
import structlog

logger = structlog.get_logger()


def get_engine():
    return create_engine(settings.DATABASE_URL)


def get_session_factory(engine=None):
    if engine is None:
        engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db(engine=None):
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)


def seed_db(engine=None):
    from staging.models.core_model import MarketRecord
    import uuid

    if engine is None:
        engine = get_engine()

    SessionLocal = get_session_factory(engine)
    session = SessionLocal()

    # Add seed data
    seed_records = [
        MarketRecord(
            id=uuid.uuid4(),
            directory="THOMSON",
            record_id="123091211111",
            record_value={"field": "value1"},
        ),
    ]

    session.bulk_save_objects(seed_records)
    session.commit()
    session.close()

    logger.info("✅ Seeded MarketRecord with initial data.")
