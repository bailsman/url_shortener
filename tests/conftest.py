import pytest
from app import app, db

@pytest.fixture(scope='session')
def _db():
    return db

@pytest.fixture
def client(db_session):
    client = app.test_client()
    yield client
