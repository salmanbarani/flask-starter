import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from src.adapters.user_orm import metadata, start_mappers

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