from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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
    news = crud.get_news(db, skip=skip, limit=limit)
    return news


@app.get("/news/{new_id}", response_model=schemas.New)
def read_new(new_id: int, db: Session = Depends(get_db)):
    db_new = crud.get_new(db, new_id=new_id)
    if db_new is None:
        raise HTTPException(status_code=404, detail="New not found")
    return db_new


@app.post("/news/{new_id}/categorys/", response_model=schemas.Category)
def create_category_for_new(
    new_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)
):
    return crud.create_new_category(db=db, category=category, new_id=new_id)


@app.get("/categorys/", response_model=List[schemas.Category])
def read_categorys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorys = crud.get_categorys(db, skip=skip, limit=limit)
    return categorys

