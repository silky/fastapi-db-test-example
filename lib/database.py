from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from alembic import command
from alembic.config import Config
import logging

from functools import partial

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

log = logging.getLogger(__name__)


def get_db_nested(commit=True):
    connection  = engine.connect()
    transaction = connection.begin()
    connection.begin_nested()

    with SessionLocal(bind=connection) as db:
        try:
            yield db
        finally:
            if commit:
                transaction.commit()
            else:
                transaction.rollback()
            connection.close()


def get_db_og():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db           = partial(get_db_nested, commit=True)
get_transient_db = partial(get_db_nested, commit=False)

# get_db = partial(get_db_nested, commit=False)
# get_db = get_db_og
