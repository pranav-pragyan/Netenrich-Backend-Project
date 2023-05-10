from sqlalchemy import Integer, Boolean, String, Column
from pydantic import BaseModel
from database.database import Base, engine, sessionLocal


# model ==>
class Books(Base):
    __tablename__ = "books"
    title = Column(String(100), index=True, nullable=False)
    author = Column(String(50), index=True, nullable=False)
    genre = Column(String(20), index=True, nullable=False)
    year_of_publication = Column(Integer, index=True, nullable=False)
    ISBN = Column(String(17), primary_key=True, index=True, nullable=False)
    # True ==> book is available
    availability = Column(Boolean, index=True, nullable=False, default=True)


# schema => req, res validation
class BooksSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_of_publication: int
    ISBN: str

    class Config:
        orm_mode = True


class BooksUpdateSchema(BaseModel):
    title: str
    author: str
    genre: str
    year_of_publication: int

    class Config:
        orm_mode = True
