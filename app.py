from flask import Flask, request
from flask_cors import CORS
import json
import database

# from youtube_transcript_api import YouTubeTranscriptApi
# print(YouTubeTranscriptApi.get_transcript("lZ3bPUKo5zc"))

# Terminology:
# Course == YouTube playlist
# Lecture == YouTube video

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, RowdyHacks2023-backend!</p>"

@app.route("/user/<user_id>")
def get_user(user_id):
    user = database.get_user(user_id)
    user_dict = {
        "id": user.id,
        "courses": json.loads(user.courses),
        "lectures": json.loads(user.videos)
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
    try:
        course = database.get_course(course_id)
    except:
        database.create_course(course_id)
    
    course = database.get_course(course_id)
    course_dict = {
        "id": course.id,
        "courses": json.loads(course.lectures)
    }
    return course_dict

    

@app.route("/lecture/<lecture_id>")
def get_or_create_lecture(lecture_id):
    # TODO
    pass


if __name__ == "__main__":
    app.run(port=9001)
