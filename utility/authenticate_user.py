from jose import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
import os


def is_authenticated(request: Request):

    # token = request.headers.get("Authorization", None)
    token = request.cookies.get('session_cookie')
    # print(token)

    if token is not None:

        try:
            encoded_jwt = token.split(" ")[1]
            # print(encoded_jwt)
            # print(os.getenv('JWT_SECRET_KEY'))

            payload = jwt.decode(
                encoded_jwt,
                os.getenv('JWT_SECRET_KEY'),
                os.getenv('ALGORITHM')
            )
            # print(payload)

            return {
                "flag": True,
                "message": "Decode successfully",
                "payload": payload
            }

        except jwt.ExpiredSignatureError:

            return {"flag": False, "message": "token expired"}

    return {"flag": False, "message": "cookie is not present"}


def is_admin_authenticated(request: Request):

    # token = request.headers.get("Authorization", None)
    token = request.cookies.get('admin_session_cookie')
    # print(token)

    if token is not None:

        try:
            encoded_jwt = token.split(" ")[1]
            print(encoded_jwt)
            print(os.getenv('JWT_SECRET_KEY'))

            payload = jwt.decode(
                encoded_jwt,
                os.getenv('JWT_SECRET_KEY'),
                os.getenv('ALGORITHM')
            )
            # print(payload)

            return {
                "flag": True,
                "message": "Decode successfully",
                "payload": payload
            }

        except jwt.ExpiredSignatureError:

            return {"flag": False, "message": "token expired"}

    return {"flag": False, "message": "admin cookie is not present"}
