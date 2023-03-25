import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
from os import environ
from database_orm import *
from sqlalchemy.orm import Session
import uuid
import json

engine = sqlalchemy.create_engine(environ['DATABASE_URL_POSTGRESQL'], echo=False) # echo=True
Base.metadata.create_all(engine)

def __json_append(db_entry, new_item):
    entry_list = json.loads(db_entry)
    entry_list.append(new_item)
    return json.dumps(entry_list)

def get_user(user_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(UserData).where(UserData.id == user_id)
        return session.scalars(selection).one()

def create_user(user_id):
    with Session(engine) as session:
        entry = UserData(
            id = user_id,
            courses = "[]",
            videos = "[]"
        )
        session.add(entry)
        session.commit()

def add_user_course(user_id, course_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(UserData).where(UserData.id == user_id)
        user = session.scalars(selection).one()
        user.courses = __json_append(user.courses, course_id)
        session.commit()

def add_user_lecture(user_id, lecture_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(UserData).where(UserData.id == user_id)
        user = session.scalars(selection).one()
        user.lectures = __json_append(user.lectures, lecture_id)
        session.commit()

def get_course(course_id):
    pass
