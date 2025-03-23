from ..schemas.schemas import table_registry
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL_UNPOOLED')

engine = create_engine(DATABASE_URL, echo=True)

table_registry.metadata.create_all(engine)

def getSession():
    with Session(engine) as session:
        return session