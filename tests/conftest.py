import pytest

from fastapi.testclient import TestClient

from lib.database import get_transient_db, get_db
from lib.app import app

from lib import models

@pytest.fixture
def client():
    def some_prep():
        db = get_transient_db()

        # TODO: Somehow run some initial actions against the database here.
        # db.add(models.Author(name="Some author"))

        yield next(db)

    app.dependency_overrides[get_db] = some_prep
    return TestClient(
                app,
                base_url="http://localhost:8080",
                raise_server_exceptions=True
                )
