import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv('REFRESH_TOKEN_EXPIRE_MINUTES')
ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = os.getenv('JWT_REFRESH_SECRET_KEY')


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:

    # print(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=30)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, os.getenv(
        'JWT_SECRET_KEY'), os.getenv('ALGORITHM'))
    return encoded_jwt


# def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
#     if expires_delta is not None:
#         expires_delta = datetime.utcnow() + expires_delta
#     else:
#         expires_delta = datetime.utcnow() + timedelta(minutes=60 * 24 * 7)

#     to_encode = {"exp": expires_delta, "sub": str(subject)}
#     encoded_jwt = jwt.encode(to_encode, os.getenv(
#         'JWT_REFRESH_SECRET_KEY'), os.getenv('ALGORITHM'))
#     return encoded_jwt
