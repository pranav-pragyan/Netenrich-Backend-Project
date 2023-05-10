from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from utility.authenticate_user import is_authenticated
# from model.friend_model import Friend, FriendSchema, FriendActionSchema
from model.student_model import Students, StudentsSchema
from model.borrow_model import Borrow
from model.book_model import Books


def construct_router():
    recommend = APIRouter(
        tags=['Recommand']
    )

    @recommend.get("/recommend/friend", response_model=list[StudentsSchema])
    async def recommand(is_auth=Depends(is_authenticated), db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:
                roll_no = is_auth['payload']['sub']
                print(roll_no)
                st = db.query(Students).filter(
                    Students.roll_no == roll_no).first()

                st = db.query(Students).filter(
                    Students.department == st.department or Students.course == st.course).all()

                return st
            else:
                return {"message": "Unauthorized access. Please login."}

        except:
            return {"message": "Unauthorized access. Please login get recommendations."}

    @recommend.get("/recommend/book", response_class=JSONResponse)
    async def recommand(is_auth=Depends(is_authenticated), db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:
                roll_no = is_auth['payload']['sub']
                st = db.query(Borrow).filter(Borrow.roll_no == roll_no).all()

                # print(st[0].isbn)
                ISBNs = []
                for i in range(len(st)):
                    ISBNs.append(st[i].isbn)

                # print(ISBNs)
                # ISBNs = set(ISBNs)
                # ISBNs = list(ISBNs)
                # print(ISBNs)

                books = []
                for i in ISBNs:
                    bk = db.query(Books).filter(Books.ISBN == i).first()
                    print(bk.title)
                    books.append(bk)

                print(books[0].genre)

                genre = []
                for i in range(len(books)):
                    genre.append(books[i].genre)

                print(genre)
                genre = set(genre)
                genre = list(genre)
                books = []
                for g in genre:
                    bk = db.query(Books).filter(Books.genre == g).all()
                    books.append(bk)

                print(books)
                return {"recommended books": books}
            else:
                return {"message": "Unauthorized access. Please login."}

        except:
            return {"message": "Unauthorized access. Please login to get recommendation."}

    return recommend
