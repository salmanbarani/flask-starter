import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from src.adapters.orm.user_orm import metadata, start_mappers
from tenacity import retry, stop_after_delay
from src import config

@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine

@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_sqlite_db)
    clear_mappers()

@pytest.fixture
def session(sqlite_session_factory):
    return sqlite_session_factory()

@retry(stop=stop_after_delay(10))
def wait_for_postgres_to_come_up(engine):
    return engine.connect()

@pytest.fixture(scope="session")
def postgres_db():
    engine = create_engine(config.get_postgres_uri(),
                           isolation_level="SERIALIZABLE")
    wait_for_postgres_to_come_up(engine)
    metadata.create_all(engine)
    return engine

@pytest.fixture
def postgres_session_factory(postgres_db):
    start_mappers()
    yield sessionmaker(bind=postgres_db)
    clear_mappers()

@pytest.fixture
def postgres_session(postgres_session_factory):
    return postgres_session_factory()