# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core_model import Base
from app import create_app
from app.containers import Container
from app.logging_config import setup_logger

# Shared test logger
test_logger = setup_logger("test-suite", level="DEBUG")

# Shared in-memory test DB URI
TEST_DB_URI = "sqlite:///file::memory:?cache=shared"

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        TEST_DB_URI,
        connect_args={"check_same_thread": False},
        echo=True,
    )
    Base.metadata.create_all(bind=engine)
    return engine

@pytest.fixture(scope="session")
def session_factory(engine):
    return sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session(engine, session_factory):
    """Provide a scoped session tied to a rollback after each test."""
    connection = engine.connect()
    transaction = connection.begin()

    session = session_factory(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Flask test client with overridden DI container."""
    container = Container()
    container.db_session.override(db_session)


    app = create_app(container)
    return app.test_client()