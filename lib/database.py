from fastapi import Query
from functools import partial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Annotated

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Note:
# Due to what is, I think, a bug in FastAPI, we need to mark thes parameters
# as ignored, otherwise they appear in the FastAPI docs! as arguments to the
# functions that depend on them.
#
# Luckily, you can't actually set them (especially because of the partial
# definitions below) but FastAPI seems to think you can.
#
# Hiding the parameter solves the problem.

def get_db_nested(commit: Annotated[bool, Query(include_in_schema=False)] = True):
    """ Uses nested transactions to allow for arbitrary .commits() in a larger
    transaction that can ultimately either be committed or rolled-back.
    """
    connection  = engine.connect()
    transaction = connection.begin()
    connection.begin_nested()

    with SessionLocal(bind=connection) as db:
        try:
            yield db
        finally:
            if commit:
                transaction.commit()
            # Note: One could call `transaction.rollback()` here; but actually
            # there's no need, we just simply don't commit.
            connection.close()


def get_db_og():
    """ Original style; left for comparision. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db           = partial(get_db_nested, commit=True)
get_transient_db = partial(get_db_nested, commit=False)
