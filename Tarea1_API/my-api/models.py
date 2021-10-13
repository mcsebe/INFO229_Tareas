from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

class New(Base): 

    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, index=True)
    date = Column(String(50))
    url = Column(String(50), unique=True)
    media_outlet = Column(String(50))

    categorys = relationship("Category", back_populates="owner")

class Category(Base):

    __tablename__ = "categorys"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), index=True)
    new_id = Column(Integer, ForeignKey("news.id"))

    owner = relationship("New", back_populates="categorys")
