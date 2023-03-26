from flask import Flask, request, abort
from flask_cors import CORS
import json
import database
import MLfolder.generateQuiz2 as generateQuiz
from dotenv import load_dotenv
load_dotenv()
from os import environ

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

@app.route("/user/<user_id>/basic")
def get_user_basic(user_id):
    if not database.user_exists(user_id):
        database.create_user(user_id)
    user = database.get_user(user_id)
    user_dict = {
        "id": user.id,
        "courses": json.loads(user.courses),
        "lectures": json.loads(user.videos)
    }
    return user_dict

@app.route("/user/<user_id>")
def get_user(user_id):
    if not database.user_exists(user_id):
        database.create_user(user_id)
    user = database.get_user(user_id)

    courses = {}
    for course_id in json.loads(user.courses):
        course = get_or_create_course(course_id)
        lectures = {}
        for lecture_id in course["lectures"]:
            lecture = get_lecture(lecture_id)
            lectures[lecture_id] = (lecture)
        course["lectures"] = lectures
        courses[course_id] = course

    user_dict = {
        "id": user.id,
        "courses": courses
    }
    return user_dict

# @app.route("/user/<user_id>/create")
# def create_user(user_id):
#     database.create_user(user_id)
#     return "done"

@app.route("/user/<user_id>/addcourse/<course_id>")
def add_user_course(user_id, course_id):
    if not database.user_exists(user_id):
        database.create_user(user_id)
    database.add_user_course(user_id, course_id)
    return "done"

@app.route("/user/<user_id>/addlecture/<lecture_id>")
def add_user_lecture(user_id, lecture_id):
    if not database.user_exists(user_id):
        database.create_user(user_id)
    database.add_user_lecture(user_id, lecture_id)
    return "done"

@app.route("/course/<course_id>")
def get_or_create_course(course_id):
    course = None
    try:
        course = database.get_course(course_id)
    except:
        database.create_course(course_id)
        course = database.get_course(course_id)
        for lecture_id in json.loads(course.lectures):
            database.create_empty_lecture(lecture_id)
    
    course_dict = {
        "id": course.id,
        "lectures": json.loads(course.lectures)
    }
    return course_dict
    # After this request responds, the client should make a request
    # to generate for every lecture in the course

@app.route("/lecture/<lecture_id>/generate")
def generate_lecture(lecture_id):
    if not database.lecture_exists(lecture_id):
        database.create_empty_lecture(lecture_id)
    transcript = database.__get_transcript(lecture_id)
    generateQuiz.getQuizJSON(lecture_id, 60, transcript)

    return "complete"

@app.route("/lecture/<lecture_id>")
def get_lecture(lecture_id):
    lecture, questions = database.get_lecture(lecture_id)

    quiz_questions_list = []
    for question in questions:
        question_object = {
            "id": question.id,
            "prompt": question.prompt,
            "question_type": question.question_type,
            "multiplechoice_options": json.loads(question.multiplechoice_options),
            "multiplechoice_correctanswer_index": question.multiplechoice_correctanswer_index,
            "freeresponse_correcttopics": json.loads(question.freeresponse_correcttopics)
        }
        quiz_questions_list.append(question_object)

    lecture_dict = {
        "id": lecture_id,
        "transcript_json": lecture.transcript_json,
        "transcript_string": lecture.transcript_string,
        "supplemental_material": lecture.supplemental_material,
        "quiz_questions": quiz_questions_list
    }
    return lecture_dict
    


if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=environ["PORT"])
