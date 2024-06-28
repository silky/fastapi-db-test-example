import pytest
from dataclasses import dataclass
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from lib.database import get_db, get_transient_db
from lib.app import app

@dataclass
class TestSession:
    db: Session
    client: TestClient


@pytest.fixture
def global_db():
    # TODO: Have a pytest argument to make it optionally transient, if, say,
    # someone wants to persist testing data to the database.
    x = get_transient_db()
    yield next(x)


@pytest.fixture
def test_session(global_db):
    """ Set a global database that is shared by every request. Also provide a
    reference to that database to any people that may like to use it to
    directly add rows, etc.
    """
    app.dependency_overrides[get_db] = lambda: global_db

    client = TestClient(
                app,
                base_url="http://localhost:8080",
                raise_server_exceptions=True
                )

    yield TestSession(db=global_db, client=client)

    # Note that this kills any other potential overrides; one could be more
    # careful here if they wished.
    app.dependency_overrides = {}


@pytest.fixture
def test_session_transient_db_only():
    """ Don't set a global database; just use the transient one per-request.
    This means no requests database changes will ever be persisted.
    """
    app.dependency_overrides[get_db] = get_transient_db
    client = TestClient(
                app,
                base_url="http://localhost:8080",
                raise_server_exceptions=True
                )

    yield TestSession(db=None, client=client)
