from sqlalchemy import Integer, String, Column
from pydantic import BaseModel
from database.database import Base


class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True,  index=True, autoincrement=True)
    sender = Column(String(9), index=True)
    reciever = Column(String(9), index=True)
    #pending, accepted, rejected
    status = Column(String(10), index=True, nullable=False, default="pending")


class FriendSchema(BaseModel):
    sender: str
    reciever: str


class FriendActionSchema(BaseModel):
    sender: str
    status: str

    class Config:
        orm_mode = True
