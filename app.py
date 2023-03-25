from flask import Flask, request
from flask_cors import CORS
import database
from bs4 import BeautifulSoup
import requests
import re

# from youtube_transcript_api import YouTubeTranscriptApi
# print(YouTubeTranscriptApi.get_transcript("lZ3bPUKo5zc"))

# Terminology:
# Course == YouTube playlist
# Lecture == YouTube video

app = Flask(__name__)
CORS(app)

def __get_playlist_videos(playlist_id):
    req = requests.get(f"https://www.youtube.com/playlist?list={playlist_id}")
    matches = re.findall('"watchEndpoint":\\{"videoId":"..........."', req.text)
    playlist_video_ids = set()
    for match in matches:
        playlist_video_ids.add(match[28:-1])
    return list(playlist_video_ids)

@app.route("/")
def hello_world():
    return "<p>Hello, RowdyHacks2023-backend!</p>"

@app.route("/user/<user_id>")
def get_user(user_id):
    user = database.get_user(user_id)
    user_dict = {
        "id": user.id,
        "courses": user.courses,
        "lectures": user.videos
    }
    return user_dict

@app.route("/user/<user_id>/create")
def create_user(user_id):
    database.create_user(user_id)
    return "done"

@app.route("/user/<user_id>/addcourse/<course_id>")
def add_user_course(user_id, course_id):
    database.add_user_course(user_id, course_id)
    return "done"

@app.route("/user/<user_id>/addlecture/<lecture_id>")
def add_user_lecture(user_id, lecture_id):
    database.add_user_lecture(user_id, lecture_id)
    return "done"

@app.route("/course/<course_id>")
def get_or_create_course(course_id):
    playlist_videos = __get_playlist_videos(course_id)
    return playlist_videos

@app.route("/lecture/<lecture_id>")
def get_or_create_lecture(lecture_id):
    # TODO
    pass
