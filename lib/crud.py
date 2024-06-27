from sqlalchemy.orm import Session

from . import models, schemas

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    b = models.Book(title=book.title, author_id=book.author_id)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    a = models.Author(name=author.name)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
