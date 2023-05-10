from sqlalchemy import Integer, Boolean, String, Column
from pydantic import BaseModel, EmailStr
from database.database import Base


# model ==>
class Admin(Base):
    __tablename__ = "admin"
    name = Column(String(40), index=True, nullable=False)
    email_id = Column(String(50),  primary_key=True,
                      index=True, nullable=False)
    position = Column(String(20), index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)


# schema => req, res validation
class AdminSchema(BaseModel):
    name: str
    email_id: EmailStr
    position: str

    class Config:
        orm_mode = True


class AdminCreateSchema(AdminSchema):
    password: str

    class Config:
        orm_mode = True


class AdminLoginSchema(BaseModel):
    email_id: EmailStr
    password: str

    class Config:
        orm_mode = True
