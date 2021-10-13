from sqlalchemy.orm import Session

from . import models, schemas


def get_new(db: Session, new_id: int):
    return db.query(models.New).filter(models.New.id == new_id).first()


def get_new_by_title(db: Session, title: str):
    return db.query(models.New).filter(models.New.title == title).first()


def get_news(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.New).offset(skip).limit(limit).all()


def create_new(db: Session, new: schemas.NewCreate):
    db_new = models.New(
        title = new.title,
        date = new.date,
        url = new.url,
        media_outlet = new.media_outlet
    )
    db.add(db_new)
    db.commit()
    db.refresh(db_new)
    return db_new


def get_categorys(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_new_category(db: Session, category: schemas.CategoryCreate, new_id: int):
    db_category = models.Category(**category.dict(), new_id=new_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

