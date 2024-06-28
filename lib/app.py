from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session

from . import schemas
from . import crud
from . import models

from .database import get_db, engine


# ~ Setup

models.Base.metadata.create_all(bind=engine)


# ~ App

app = FastAPI(title="Examples", separate_input_output_schemas=False)


# ~ Routes

@app.get("/hello")
def hello():
    return "hello world!"

@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.post("/books", response_model=schemas.Book)
def create_author(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)
