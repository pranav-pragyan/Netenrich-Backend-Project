from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from model.book_model import Books, BooksSchema, BooksUpdateSchema
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from utility.authenticate_user import is_admin_authenticated


def construct_router():

    book = APIRouter(
        tags=["Books"]
    )

    @book.post("/book/add", response_class=JSONResponse)
    async def add_book(books: list[BooksSchema], db: Session = Depends(get_db), is_auth=Depends(is_admin_authenticated)):
        try:
            if is_auth['flag']:

                existing_book = []
                for book in books:
                    b = db.query(Books).filter(Books.ISBN == book.ISBN).first()
                    if b:
                        # return {"message": "A book with the given ISBN already exists."}
                        existing_book.append(b)
                    else:
                        b = Books(title=book.title, author=book.author, genre=book.genre,
                                  year_of_publication=book.year_of_publication, ISBN=book.ISBN)
                        db.add(b)
                        db.commit()
                return {"message": "All books added successfully", "existing book(s)": existing_book}
            else:
                return {"message": "Unauthorized access. Please login."}
        except:
            return HTTPException(status_code=500, detail="Something went wrong. Couldn't add")

    @book.get("/books/get", response_model=list[BooksSchema])
    async def get_books(db: Session = Depends(get_db)):
        try:
            return db.query(Books).all()
        except:
            return HTTPException(status_code=404, detail="no record found")

    @book.put("/book/update", response_class=JSONResponse)
    async def update_book(books: list[BooksSchema], response: Response, is_auth=Depends(is_admin_authenticated), db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:

                not_found_book = []
                for book in books:
                    b = db.query(Books).filter(Books.ISBN == book.ISBN).first()

                    if not b:
                        # return {"message": f" no record found with ISBN : {isbn}."}
                        not_found_book.append(book.ISBN)
                    else:
                        b.title = book.title
                        b.author = book.author
                        b.genre = book.genre
                        b.year_of_publication = b.year_of_publication
                        db.add(b)
                        db.commit()
                return {"message": f"books updated successfully.", "Book not found":  not_found_book}
            else:
                return {"message": "Unauthorized access. Please login."}

        except:
            return HTTPException(status_code=500, detail="Something went wrong. Couldn't update")

    # pass ISBNs of the books, as query seperated by comma.
    # example .../book/delete?isbn=isbn1,isbn2,...
    @book.delete("/book/delete/{isbn}", response_class=JSONResponse)
    async def delete_book(isbn: str, is_auth=Depends(is_admin_authenticated), db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:
                # print(isbn)
                isbn_list = isbn.split(",")
                # print(isbn_list)
                not_found_book = []
                for i in isbn_list:
                    b = db.query(Books).filter(Books.ISBN == i).first()

                    if not b:
                        # return {"message": f" no record found with ISBN : {isbn}."}
                        not_found_book.append(i)
                    else:
                        db.delete(b)
                        db.commit()
                return {"message": f"books deleted successfully.", "Book not found": not_found_book}
            else:
                return {"message": "Unauthorized access. Please login."}

        except:
            return HTTPException(status_code=500, detail="Something went wrong. Couldn't delete")

    # pass search keyas query.
    # example http://127.0.0.1:8000/The_Page_Turners/book/search_by_title?key=KEY
    @book.get("/book/search_by_title")
    async def search(key: str = Query(..., min_length=1), db: Session = Depends(get_db)):
        try:
            st = db.query(Books).filter(
                Books.title.ilike(f"{key}%")).all()
            st = set(st)
            st = list(st)
            return {"response": st}
        except:
            return HTTPException(status_code=500, detail="something went wrong.")
    return book
