from fastapi import FastAPI, Query, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from model.student_model import Students, StudentsCreateSchema, StudentsSchema, StudentLoginSchema
from fastapi import APIRouter
# from utility.file_conversion import convertBinaryToFile, convertToBinary
from fastapi.responses import JSONResponse
from utility.password import get_hashed_password, verify_password
from utility.token_handling import create_access_token
from fastapi import Response, Request
from utility.authenticate_user import is_authenticated


def construct_router():

    student = APIRouter(
        tags=["Student"]
    )

    # @student.post("/add_student", response_model=StudentsSchema)
    # async def add_student(student: StudentsCreateSchema, db: Session = Depends(get_db)):
    #     u = Students(name=student.name, email_id=student.email_id,
    #                  roll_no=student.roll_no, course=student.course, department=student.department, year_of_admission=student.year_of_admission, password=student.password)
    #     db.add(u)
    #     db.commit()
    #     return u

    # @student.get("/get_students_detail", response_model=list[StudentsSchema])
    # async def get_students_detail(db: Session = Depends(get_db)):
    #     try:
    #         return db.query(Students).all()
    #     except:
    #         return HTTPException(status_code=404, detail="no record found")

    @student.post("/signup", response_class=JSONResponse)
    async def signup(student: StudentsCreateSchema, db: Session = Depends(get_db)):
        try:
            # return db.query(Students).all()
            st = db.query(Students).filter(
                Students.email_id == student.email_id).first()
            if st:
                return{"This email already exists. Please try with other one."}
            else:
                print(student.password)
                student.password = get_hashed_password(student.password)
                print(student.password)
                # st = Students(name=student.name, email_id=student.email_id,
                #               roll_no=student.roll_no, course=student.course, department=student.department, year_of_admission=student.year_of_admission, password=student.password)
                st = Students(**student.__dict__)
                db.add(st)
                db.commit()
                return {"status_code : 200", "Registration done successfully"}

        except:
            return HTTPException(status_code=404, detail="something went wrong.")

    @student.post("/signin", response_class=JSONResponse)
    async def signin(student: StudentLoginSchema, response: Response, db: Session = Depends(get_db)):
        try:
            st = db.query(Students).filter(
                Students.roll_no == student.roll_no).first()

            # print(st.password)
            if not st:
                return{"Roll number is incorrect"}

            is_password_correct = verify_password(
                student.password, st.password)
            # print(is_password_correct)

            if not is_password_correct:
                return {"Password is incorrect"}

            else:
                jwt_token = create_access_token(student.roll_no)
                response.set_cookie(key="session_cookie",
                                    value=f"Bearer {jwt_token}", max_age=60*60)

                return {"status_code": 200, "access_token": jwt_token, "token_type": "bearer"}

        except:
            return HTTPException(status_code=404, detail="Couldn't logged in. Please try again.")

    @student.get("/my_profile", response_class=JSONResponse)
    async def my_profile(is_auth=Depends(is_authenticated),  db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:
                roll_no = is_auth['payload']['sub']
                st = db.query(Students).filter(
                    Students.roll_no == roll_no).first()
                st = {"name": st.name, "roll_no": st.roll_no,  "course": st.course,
                      "department": st.department, "year_of_admission": st.year_of_admission, "email_id": st.email_id}
                return st
            else:
                return {"message": "Unauthorized access. Please login to see the profile."}
        except:
            return HTTPException(status_code=404, detail="Couldn't logged in. Please try again.")

    @student.get("/logout", response_class=JSONResponse)
    async def logout(response: Response, is_auth=Depends(is_authenticated)):
        try:
            if is_auth['flag']:
                response.delete_cookie('session_cookie')
            return {"message": "You logged out successfully."}
        except:
            return HTTPException(status_code=404, detail="Couldn't logged out. Please try again.")

    # pass key as query here : example .../student/search_by_name?key==value_to_search
    @student.get("/student/search_by_name")
    async def search(key: str = Query(..., min_length=1), db: Session = Depends(get_db)):
        try:
            st = db.query(Students.name).filter(
                Students.name.ilike(f"{key}%")).all()
            st = set(st)
            st = list(st)
            return {"response": st}
        except:
            return HTTPException(status_code=404, detail="something went wrong.")

    # pass key as query here : example .../student/search_by_dept?key==value_to_search
    @student.get("/student/search_by_dept")
    async def search(key: str = Query(..., min_length=1), db: Session = Depends(get_db)):
        try:
            st = db.query(Students.name).filter(
                Students.department.ilike(f"{key}%")).all()
            st = set(st)
            st = list(st)
            return {"response": st}
        except:
            return HTTPException(status_code=404, detail="something went wrong.")

    # pass key as query here : example .../student/search_by_course?key==value_to_search
    @student.get("/student/search_by_course")
    async def search(key: str = Query(..., min_length=1), db: Session = Depends(get_db)):
        try:
            st = db.query(Students.name).filter(
                Students.course.ilike(f"{key}%")).all()
            st = set(st)
            st = list(st)
            return {"response": st}
        except:
            return HTTPException(status_code=404, detail="something went wrong.")

    return student
