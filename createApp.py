from fastapi import FastAPI
from database.database import Base, engine
from controller import student, book, admin, borrow, friend, recommendation


def create_app():

    app = FastAPI()

    Base.metadata.create_all(bind=engine)

    base_path = "/The_Page_Turners"

    app.include_router(
        student.construct_router(),
        prefix=base_path
    )

    app.include_router(
        book.construct_router(),
        prefix=base_path
    )

    app.include_router(
        admin.construct_router(),
        prefix=base_path
    )

    app.include_router(
        borrow.construct_router(),
        prefix=base_path
    )

    app.include_router(
        friend.construct_router(),
        prefix=base_path
    )

    app.include_router(
        recommendation.construct_router(),
        prefix=base_path
    )

    return app
