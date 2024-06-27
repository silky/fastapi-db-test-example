from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base


class Book(Base):
    __tablename__ = "books"

    id        = Column(Integer, primary_key=True)
    title     = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")


class Author(Base):
    __tablename__ = "authors"

    id   = Column(Integer, primary_key=True)
    name = Column(String, index=True)

    books = relationship("Book", back_populates="author")


