from typing import List, Optional

from pydantic import BaseModel


class CategoryBase(BaseModel):
    category: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    new_title: str

    class Config:
        orm_mode = True


class NewBase(BaseModel):
    title: str
    date: str
    url: str
    media_outlet: str


class NewCreate(NewBase):
    pass


class New(NewBase):
    id: int
    categorys: List[Category] = []

    class Config:
        orm_mode = True

