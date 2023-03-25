import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
from os import environ
from database_orm import *
from sqlalchemy.orm import Session
import uuid

engine = sqlalchemy.create_engine(environ['DATABASE_URL_POSTGRESQL'], echo=False) # echo=True
Base.metadata.create_all(engine)


from youtube_transcript_api import YouTubeTranscriptApi



# print(YouTubeTranscriptApi.get_transcript("lZ3bPUKo5zc"))






