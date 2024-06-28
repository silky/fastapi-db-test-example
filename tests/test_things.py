import pytest

from lib.schemas import AuthorCreate, BookCreate
from lib.models import Author

def test_create_author(test_session):
    """ Does the API even work at all? """
    client = test_session.client

    some_author = AuthorCreate(name="hello")
    r = client.post("/authors", json=some_author.model_dump())
    r.raise_for_status()


def test_create_book_variant_1(test_session):
    """ Create a book; i.e. create an author _then_ a book, using the API in
    both cases. This requires that the state of the database be persisted
    _across_ calls. This is the most normal behaviour; except here none of
    this data is persisted once the test is completed.
    """
    client = test_session.client

    some_author = AuthorCreate(name="hello")
    r = client.post("/authors", json=some_author.model_dump())
    r.raise_for_status()
    j = r.json()

    some_book = BookCreate(title="hello", author_id=j["id"])
    r = client.post("/books", json=some_book.model_dump())
    r.raise_for_status()


def test_create_book_variant_2(test_session):
    """ Same as above, but access the database directly this time, and just
    add our models ourselves.
    """
    client = test_session.client
    db = test_session.db

    some_author = Author(name="hello")
    db.add(some_author)
    db.commit()
    db.refresh(some_author)

    some_book = BookCreate(title="hello", author_id=some_author.id)
    r = client.post("/books", json=some_book.model_dump())
    r.raise_for_status()


def test_transient_db_works(test_session_transient_db_only):
    """
    Run two author inserts, then observe that the yield the exact same
    results; i.e. two authors with the same id. This means that _neither_
    request was able to make changes to the database.
    """
    client = test_session_transient_db_only.client

    some_author = AuthorCreate(name="hello")
    r1 = client.post("/authors", json=some_author.model_dump())
    r1.raise_for_status()

    some_author = AuthorCreate(name="hello")
    r2 = client.post("/authors", json=some_author.model_dump())
    r2.raise_for_status()

    assert r1.json() == r2.json()
