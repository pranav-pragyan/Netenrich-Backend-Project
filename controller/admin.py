from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from model.admin_model import Admin, AdminSchema, AdminCreateSchema, AdminLoginSchema
from fastapi import APIRouter
from typing import List
from fastapi.responses import JSONResponse
from utility.token_handling import create_access_token
from utility.password import get_hashed_password, verify_password
from fastapi.responses import Response
from utility.authenticate_user import is_admin_authenticated


base_path = "/The_Page_Turners"


def construct_router():

    admin = APIRouter(
        tags=["Admin"]
    )

    # @admin.post("/add_admin", response_model=AdminSchema)
    # async def add_admin(admin: AdminCreateSchema, db: Session = Depends(get_db)):
    #     u = Admin(name=admin.name, email_id=admin.email_id,
    #               position=admin.position, password=admin.password)
    #     db.add(u)
    #     db.commit()
    #     return u

    # @admin.get("/get_admins_detail", response_model=List[AdminSchema])
    # async def get_admins_detail(db: Session = Depends(get_db)):
    #     try:
    #         return db.query(Admin).all()
    #     except:
    #         return HTTPException(status_code=404, detail="no record found")

    @admin.post("/admin/signup", response_class=JSONResponse)
    async def signup(admin: AdminCreateSchema, db: Session = Depends(get_db)):
        try:
            ad = db.query(Admin).filter(
                Admin.email_id == admin.email_id).first()
            if ad:
                return{"This email already exists. Please try with other one."}
            else:
                admin.password = get_hashed_password(admin.password)
                ad = Admin(**admin.__dict__)
                db.add(ad)
                db.commit()
                return {"status_code : 200", "Registration done successfully"}

        except:
            return HTTPException(status_code=500, detail="something went wrong.")

    @admin.post("/admin/signin", response_class=JSONResponse)
    async def signin(admin: AdminLoginSchema, response: Response, db: Session = Depends(get_db)):
        try:
            ad = db.query(Admin).filter(
                Admin.email_id == admin.email_id).first()

            # print(st.password)
            if not ad:
                return{"Email id is incorrect"}

            is_password_correct = verify_password(admin.password, ad.password)
            # print(is_password_correct)

            if not is_password_correct:
                return {"Password is incorrect"}

            else:
                jwt_token = create_access_token(admin.email_id)
                response.set_cookie(key="admin_session_cookie",
                                    value=f"Bearer {jwt_token}", max_age=60*60)
                return {"status_code": 200, "admin_access_token": jwt_token, "token_type": "bearer"}

        except:
            return HTTPException(status_code=500, detail="Couldn't logged in. Please try again.")

    @admin.get("/admin/my_profile", response_class=JSONResponse)
    async def my_profile(is_auth=Depends(is_admin_authenticated),  db: Session = Depends(get_db)):
        try:
            if is_auth['flag']:
                print(is_auth)
                email_id = is_auth['payload']['sub']
                ad = db.query(Admin).filter(Admin.email_id == email_id).first()
                ad = {"name": ad.name, "position": ad.position,
                      "email_id": ad.email_id}
                return ad
            else:
                return {"message": "Unauthorized access. Please login to see the profile."}
        except:
            return HTTPException(status_code=500, detail="something went wrong. Please try again")

    @admin.get("/admin/logout", response_class=JSONResponse)
    async def logout(response: Response, is_auth=Depends(is_admin_authenticated)):
        try:
            if is_auth['flag']:
                response.delete_cookie('admin_session_cookie')
            return {"message": "You logged out successfully."}
        except:
            return HTTPException(status_code=500, detail="Couldn't logged out. Please try again.")

    return admin
