from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from dotenv import load_dotenv
import os

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# SQLALCHEMY_DB_URL = "mysql+pymysql://root:pran@127.0.0.1:3306/The_Page_Turners"
SQLALCHEMY_DB_URL = os.getenv('SQLALCHEMY_DB_URL')
engine = create_engine(SQLALCHEMY_DB_URL)

if engine:
    print("Database is connected to the server.")
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
