from sqlalchemy import Integer, Boolean, String, Column, DateTime, ForeignKey
from pydantic import BaseModel
from database.database import Base, engine, sessionLocal
from datetime import datetime


class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True,  index=True, autoincrement=True)
    roll_no = Column(String(9), index=True)
    isbn = Column(String(17), index=True, nullable=False)
    # accepted, decline, pending
    status = Column(String(10), index=True, nullable=False, default="pending")
    req_date = Column(DateTime, index=True, nullable=False)
    action_date = Column(DateTime, index=True)


class BorrowUpdateSchema(BaseModel):
    isbn: str
    status: str

    class Config:
        orm_mode = True


# class BooksUpdateSchema(BaseModel):
#     title: str
#     author: str
#     genre: str
#     year_of_publication: int

#     class Config:
#         orm_mode = True
