from sqlalchemy import Integer, Boolean, String, Column, BLOB
from pydantic import BaseModel, EmailStr
from database.database import Base


# model ==>
class Students(Base):
    __tablename__ = "students"
    name = Column(String(40), index=True, nullable=False)
    roll_no = Column(String(9), primary_key=True,  index=True, nullable=False)
    course = Column(String(15), index=True, nullable=False)
    department = Column(String(25), index=True, nullable=False)
    year_of_admission = Column(Integer, index=True, nullable=False)
    email_id = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(64), index=True, nullable=False)
    # profile_picture = Column(BLOB, index=True)


# schema => req, res validation
class StudentsSchema(BaseModel):
    name: str
    roll_no: str
    course: str
    department: str
    year_of_admission: int
    email_id: EmailStr
    # profile_picture: BLOB

    class Config:
        orm_mode = True


class StudentsCreateSchema(StudentsSchema):
    password: str

    class Config:
        orm_mode = True


class StudentLoginSchema(BaseModel):
    roll_no: str
    password: str

    class Config:
        orm_mode = True
