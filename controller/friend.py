from fastapi import FastAPI, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import Base
from database.get_db_session import get_db
from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response
from utility.authenticate_user import is_authenticated
from model.friend_model import Friend, FriendSchema, FriendActionSchema
from model.student_model import Students


def construct_router():
    friend = APIRouter(
        tags=['Friends']
    )

    # pass a roll number of the the student, whom you want to connect as query.
    # example .../conn_req?conn_roll=ROLLNO
    @friend.get("/conn_req", response_class=JSONResponse)
    async def conn_req(conn_roll: str, db: Session = Depends(get_db), is_auth=Depends(is_authenticated)):
        try:
            if is_auth['flag']:

                s = db.query(Students).filter(
                    Students.roll_no == conn_roll).first()

                if not s:
                    return {"message": "this id doesn't exist"}

                roll_no = is_auth['payload']['sub']

                # print(roll_no, conn_roll)
                f = db.query(Friend).filter(Friend.sender ==
                                            roll_no and Friend.reciever == conn_roll).first()

                # print(f.status, f.sender, f.reciever)
                if f and f.status == "accepted":
                    return {"status_code": 200, "mesage": "Already accepted."}

                if f and f.status == "pending":
                    return {"message": "request is already in pending."}

                f = Friend(sender=roll_no, reciever=conn_roll)
                db.add(f)
                db.commit()
                return {"status_code : 200", "Request sent successfully."}
            else:
                return {"message": "Unauthorized access. Please login to make friends."}
        except:
            return HTTPException(status_code=404, detail="Something went wrong. Couldn't make request")

    # pass a roll number of the the student, whom you want to connect as query.
    # example .../conn_accept?req_roll=ROLLNO
    @friend.put("/conn_accept", response_class=JSONResponse)
    async def conn_accept(req_roll: str, db: Session = Depends(get_db), is_auth=Depends(is_authenticated)):
        try:
            if is_auth['flag']:
                roll_no = is_auth['payload']['sub']
                print("login", roll_no)
                print(req_roll)
                f = db.query(Friend).filter(
                    Friend.sender == req_roll and Friend.reciever == roll_no and Friend.status == "pending").first()

                if f and f.status == "accepted":
                    return {"status_code : 200", "Already accepted."}
                elif f and not f.status == "accepted":
                    print(f.sender)
                    print(f.reciever)
                    print(f.status)
                    f.status = "accepted"
                    db.add(f)
                    db.commit()
                    return {"status_code : 200", "Request accepted successfully."}
                else:
                    return {"status_code : 404", "not found."}
            else:
                return {"message": "Unauthorized access. Please login to make friends."}
        except:
            return HTTPException(status_code=404, detail="Something went wrong. Couldn't make request")

    # pass a roll number of the the student, whom you want to connect as query.
    # example .../conn_reject?req_roll=ROLLNO
    @friend.put("/conn_reject", response_class=JSONResponse)
    async def conn_accept(req_roll: str, db: Session = Depends(get_db), is_auth=Depends(is_authenticated)):
        try:
            if is_auth['flag']:
                roll_no = is_auth['payload']['sub']
                print("roll", roll_no)
                print("req_roll", req_roll)

                f = db.query(Friend).filter(Friend.sender ==
                                            req_roll and Friend.reciever == roll_no and Friend.status == "pending").first()

                print(f.status, f.sender, f.reciever)
                if f and f.status == "rejected":
                    return {"status_code : 200", "Already rejected."}
                elif f and not f.status == "rejected":
                    # print(f.sender)
                    # print(f.reciever)
                    # print(f.status)
                    f.status = "rejected"
                    db.add(f)
                    db.commit()
                    return {"status_code : 200", "Request rejected successfully."}
                else:
                    return {"status_code : 404", "not found."}
            else:
                return {"message": "Unauthorized access. Please login to make friends."}
        except:
            return HTTPException(status_code=404, detail="Something went wrong. Couldn't make request")

    return friend
