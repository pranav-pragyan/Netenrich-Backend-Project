from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from utility.authenticate_user import is_admin_authenticated, is_authenticated
from model.borrow_model import Borrow, BorrowUpdateSchema
from model.book_model import Books
from datetime import datetime


def construct_router():
    borrow = APIRouter(
        tags=['Borrows']
    )

    @borrow.get("/book/request", response_class=JSONResponse)
    async def req_book(isbn: str, db: Session = Depends(get_db), is_auth=Depends(is_authenticated)):
        try:
            if is_auth['flag']:

                b = db.query(Books).filter(Books.ISBN == isbn).first()
                if not b:
                    return {"message": "This book doesn't exist"}

                if b.availability == False:
                    return {"message": "this book is not available"}

                roll_no = is_auth['payload']['sub']

                st = db.query(Borrow).filter(
                    Borrow.isbn == isbn and Borrow.roll_no == roll_no).first()

                if st.status == "pending":
                    return {"message": "You cannot request an already pending status book."}

                b = Borrow(roll_no=roll_no, isbn=isbn, req_date=datetime.now())

                db.add(b)
                db.commit()
                return {"message": "successfully made a request for the book"}
            else:
                return {"message": "Unauthorized access. Please login to borrow."}
        except:
            return HTTPException(status_code=500, detail="Something went wrong. Couldn't make request")

    @borrow.post("/book/action", response_class=JSONResponse)
    async def act_book(borrow: BorrowUpdateSchema, db: Session = Depends(get_db), is_auth=Depends(is_admin_authenticated)):
        try:
            if is_auth['flag']:
                b = db.query(Borrow).filter(
                    Borrow.isbn == borrow.isbn and Borrow.status == "pending").first()
                if not b:
                    return {"message": "Incorrect ISBN"}
                else:
                    b.status = borrow.status
                    b.action_date = datetime.now()
                    db.add(b)
                    db.commit()

                    # now make the availability of the ISBN False
                    if borrow.status == "accepted":
                        b = db.query(Books).filter(
                            Books.ISBN == borrow.isbn).first()
                        b.availability = 0
                        db.add(b)
                        db.commit()

                    return {"message": "updated successfully."}
                pass
            else:
                return {"message": "Unauthorized access. Please login."}
        except:
            return HTTPException(status_code=500, detail="Something went wrong. Couldn't make request")

    return borrow
