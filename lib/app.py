import json
import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi import APIRouter, Depends
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
routes = APIRouter()

@routes.get("/hello")
def hello():
    return "hello world!"

app.include_router(routes)


@app.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)
