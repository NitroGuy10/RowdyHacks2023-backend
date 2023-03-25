from flask import Flask, request
from flask_cors import CORS
import database

# from youtube_transcript_api import YouTubeTranscriptApi
# print(YouTubeTranscriptApi.get_transcript("lZ3bPUKo5zc"))


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
