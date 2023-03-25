import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
from os import environ
from database_orm import Base, Product
from sqlalchemy.orm import Session
import uuid

engine = sqlalchemy.create_engine(environ['DATABASE_URL_POSTGRESQL'], echo=False) # echo=True
Base.metadata.create_all(engine)

def add_entry(dataframe_json):
    id = uuid.uuid4()
    with Session(engine) as session:
        entry = Product(
            id=id,
            dataframe=dataframe_json
        )
        session.add(entry)
        session.commit()
    return id

def get_entry(id):
    with Session(engine) as session:
        selection = sqlalchemy.select(Product).where(Product.id == id)
        for entry in session.scalars(selection):
            return entry
    return None


