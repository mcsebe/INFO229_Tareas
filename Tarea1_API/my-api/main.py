from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

from datetime import datetime

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

database = SessionLocal()
database.add(models.New(title = 'noticia 1', date = datetime.strptime('15/01/2021', "%d/%m/%Y"), url = 'www.noticia1.cl', media_outlet = 'Medio 1'))
database.add(models.New(title = 'noticia 2', date = datetime.strptime('15/02/2021', "%d/%m/%Y"), url = 'www.noticia2.cl', media_outlet = 'Medio 2'))
database.add(models.New(title = 'noticia 3', date = datetime.strptime('15/03/2021', "%d/%m/%Y"), url = 'www.noticia3.cl', media_outlet = 'Medio 3'))
database.add(models.New(title = 'noticia 4', date = datetime.strptime('15/04/2021', "%d/%m/%Y"), url = 'www.noticia4.cl', media_outlet = 'Medio 4'))
database.commit()
database.add(models.Category(category = 'sport', new_title = 'noticia 1'))
database.add(models.Category(category = 'policies', new_title = 'noticia 1'))
database.add(models.Category(category = 'scientific', new_title = 'noticia 2'))
database.add(models.Category(category = 'economical', new_title = 'noticia 2'))
database.add(models.Category(category = 'policies', new_title = 'noticia 3'))
database.add(models.Category(category = 'economical', new_title = 'noticia 3'))
database.add(models.Category(category = 'scientific', new_title = 'noticia 4'))
database.add(models.Category(category = 'sport', new_title = 'noticia 4'))
database.commit()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/news/", response_model=schemas.New)
def create_user(new: schemas.NewCreate, db: Session = Depends(get_db)):
    db_new = crud.get_new_by_title(db, title = new.title)
    if db_new:
        raise HTTPException(status_code=400, detail="Title already registered")
    return crud.create_new(db=db, new=new)


@app.get("/news/", response_model=List[schemas.New])
def read_news(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_new = crud.get_news(db, skip=skip, limit=limit)
    return db_new


@app.get("/news/{new_id}", response_model=schemas.New)
def read_new(new_id: int, db: Session = Depends(get_db)):
    db_new = crud.get_new(db, new_id=new_id)
    if db_new is None:
        raise HTTPException(status_code=404, detail="New not found")
    return db_new

@app.get("/news", response_model=List[schemas.New])
def read_news(From: str, To: str,category: str, db: Session = Depends(get_db)):
    db_new = crud.get_news_endpoint (db, inicio = From, fin = To, category = category)
    return db_new


@app.post("/news/{titulo}/categorys/", response_model=schemas.Category)
def create_category_for_new(
    titulo: str, category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_new_category(db=db, category=category, title=titulo)


@app.get("/categorys/", response_model=List[schemas.Category])
def read_categorys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorys = crud.get_categorys(db, skip=skip, limit=limit)
    return categorys

