import sqlalchemy
from dotenv import load_dotenv
load_dotenv()
from os import environ
from database_orm import *
from sqlalchemy.orm import Session
import json
import requests
import re
import uuid
from youtube_transcript_api import YouTubeTranscriptApi

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

def __get_playlist_title(playlist_id):
    req = requests.get(f"https://www.youtube.com/playlist?list={playlist_id}")
    search = re.search('<title>(.*) - YouTube</title>', req.text)
    return search.group(1)

def __get_transcript(video_id):
    try:
        exampleTranscript = YouTubeTranscriptApi.get_transcript(video_id)
        fullTranscript = ""
        for i in range(len(exampleTranscript)):
            fullTranscript += " " + exampleTranscript[i]["text"]
        return fullTranscript
    except:
        return "NO TRANSCRIPT"

def __flatten_array(arr):
    flattened = []
    for i in arr:
        if isinstance(i, list):
            flattened.extend(__flatten_array(i))
        else:
            flattened.append(i)
    return flattened

def get_user(user_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(UserData).where(UserData.id == user_id)
        return session.scalars(selection).one()

def user_exists(user_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(UserData).where(UserData.id == user_id)
        try:
            session.scalars(selection).one()
            return True
        except:
            return False

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

def update_user_course_score(course_id, user_id, num_attempted, num_correct):
    with Session(engine) as session:
        selection = sqlalchemy.select(Course).where(Course.id == course_id)
        course = session.scalars(selection).one()
        course_user_data = json.loads(course.user_data)
        if user_id in course_user_data:
            course_user_data[user_id]["num_attempted"] += num_attempted
            course_user_data[user_id]["num_correct"] += num_correct
        else:
            course_user_data[user_id] = {
                "num_attempted": num_attempted,
                "num_correct": num_correct
            }
        course.user_data = json.dumps(course_user_data)
        session.commit()

def create_course(course_id):
    # new_course = None
    playlist_videos_str = json.dumps(__get_playlist_videos(course_id))
    playlist_title = __get_playlist_title(course_id)
    with Session(engine) as session:
        entry = Course(
            id = course_id,
            lectures = playlist_videos_str,
            title = playlist_title,
            description = "pending...",
            user_data = "{}"
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
            transcript_string = "",
            supplemental_material = "{}"
        )
        session.add(entry)
        session.commit()

def lecture_exists(lecture_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(Lecture).where(Lecture.id == lecture_id)
        try:
            session.scalars(selection).one()
            return True
        except:
            return False

def get_lecture(lecture_id):
    # select quiz questions where lecture_id == lecture_id
    with Session(engine) as session:
        selection = sqlalchemy.select(Lecture).where(Lecture.id == lecture_id)
        lecture = session.scalars(selection).one()
        selection = sqlalchemy.select(QuizQuestion).where(QuizQuestion.lecture_id == lecture_id)
        questions = session.scalars(selection).all()
        return (lecture, questions)

def get_quiz_question(quiz_question_id):
    with Session(engine) as session:
        selection = sqlalchemy.select(QuizQuestion).where(QuizQuestion.id == quiz_question_id)
        question = session.scalars(selection).one()
        return question

def save_lecture_material(lecture_id, lecture_material, summary):
    print(type(summary))
    print(summary)
    supplemental_material = {
        "Summary": summary,
        "Study Guide": lecture_material["Study Guide"],
        "Resources": lecture_material["Resources"]
    }
    question_entries = []

    for question_num in range(len(lecture_material["quiz questions"])):
        prompt = lecture_material["quiz questions"][question_num].split(": ")[1]
        question_type = lecture_material["quiz questions"][question_num].split(": ")[0]
        multiplechoice_options = "[]"
        multiplechoice_correctanswer_index = 0  # It's always 0 lol
        freeresponse_correcttopics = "[]"
        if question_type == "MC":
            print(lecture_material["quiz answers"][question_num])
            if lecture_material["quiz answers"][question_num][0].startswith("MC: "):
                multiplechoice_options = json.dumps([answer[4:] for answer in lecture_material["quiz answers"][question_num]])
            else:
                multiplechoice_options = json.dumps(lecture_material["quiz answers"][question_num])
        else:
            if __flatten_array(lecture_material["quiz answers"][question_num])[0].startswith("F: "):
                freeresponse_correcttopics = json.dumps([topic[3:] for topic in __flatten_array(lecture_material["quiz answers"][question_num])])
            else:
                freeresponse_correcttopics = json.dumps(__flatten_array(lecture_material["quiz answers"][question_num]))
        
        question_entry = QuizQuestion(
            id = uuid.uuid4(),
            lecture_id = lecture_id,
            prompt = prompt,
            question_type = question_type,
            multiplechoice_options = multiplechoice_options,
            multiplechoice_correctanswer_index = multiplechoice_correctanswer_index,
            freeresponse_correcttopics = freeresponse_correcttopics
        )
        question_entries.append(question_entry)
    
    with Session(engine) as session:
        selection = sqlalchemy.select(Lecture).where(Lecture.id == lecture_id)
        print(lecture_id)
        lecture = session.scalars(selection).one()
        lecture.supplemental_material = json.dumps(supplemental_material)

        for question_entry in question_entries:
            session.add(question_entry)
        
        session.commit()
    print("Saved some lecture questions!")
    
