import pytest

from lib.schemas import AuthorCreate

def test_create_author(client):
    some_user = AuthorCreate(name="hello")

    r = client.post("/authors", json=some_user.model_dump())
    j1 = r.json()
    assert r.status_code == 200

    r = client.post("/authors", json=some_user.model_dump())
    j2 = r.json()
    assert r.status_code == 200

    assert j1 == j2
