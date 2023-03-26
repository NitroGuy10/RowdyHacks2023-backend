import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
from os import environ
from database_orm import *
from sqlalchemy.orm import Session
import json
import requests
import re

engine = sqlalchemy.create_engine(environ['DATABASE_URL_POSTGRESQL'], echo=False) # echo=True
Base.metadata.create_all(engine)

def __json_append(db_entry, new_item):
    entry_list = json.loads(db_entry)
    entry_list.append(new_item)
    return json.dumps(entry_list)

def __get_playlist_videos(playlist_id):
    req = requests.get(f"https://www.youtube.com/playlist?list={playlist_id}")
    matches = re.findall('"watchEndpoint":\\{"videoId":"..........."', req.text)
    playlist_video_ids = set()
    for match in matches:
        playlist_video_ids.add(match[28:-1])
    return list(playlist_video_ids)

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

def create_course(course_id):
    # new_course = None
    playlist_videos_str = json.dumps(__get_playlist_videos(course_id))
    with Session(engine) as session:
        entry = Course(
            id = course_id,
            lectures = playlist_videos_str
        )
        session.add(entry)
        # new_course = entry
        session.commit()
    # return new_course

def get_course(course_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(Course).where(Course.id == course_id)
        return session.scalars(selection).one()

def create_empty_lecture(lecture_id):
    with Session(engine) as session:
        entry = Lecture(
            id = lecture_id,
            transcript_json = "",
            transcript_string = ""
        )
        session.add(entry)
        session.commit()

def get_lecture_questions(lecture_id):
    # select quiz questions where lecture_id == lecture_id
    pass
