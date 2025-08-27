# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from staging.settings import settings
from staging.models import Base
from staging.azure_auth import AzureAuthManager
import structlog
import asyncio

logger = structlog.get_logger()

# Global Azure auth manager instance
azure_auth = AzureAuthManager(client_id=settings.AZURE_CLIENT_ID)


async def get_database_url() -> str:
    """Get database URL, either from Key Vault (production) or settings (development)."""
    if settings.USE_AZURE_AUTH and settings.AZURE_KEY_VAULT_URL:
        try:
            logger.info("Retrieving database connection string from Azure Key Vault")
            return await azure_auth.get_database_connection_string(settings.AZURE_KEY_VAULT_URL)
        except Exception as e:
            logger.error("Failed to retrieve connection string from Key Vault, falling back to settings", error=str(e))
            return settings.DATABASE_URL
    else:
        logger.info("Using database URL from settings")
        return settings.DATABASE_URL


def get_engine():
    """Get SQLAlchemy engine with appropriate connection string."""
    try:
        # For async context, we need to handle this differently
        database_url = asyncio.run(get_database_url())
        return create_engine(database_url)
    except RuntimeError:
        # If we're already in an async context, use the sync fallback
        logger.info("Using fallback database URL from settings")
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
    from staging.models import MarketRecord
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
