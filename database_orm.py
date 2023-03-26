from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class UserData(Base):
    __tablename__ = "user_data"
    id = Column(String, primary_key=True)  # User's email address
    courses = Column(String)  # JSON Array
    videos = Column(String)  # JSON Array
    quiz_question_responses = relationship("QuizQuestionResponse")  # User -> QuizQuestionResponse (one to many)

    def __repr__(self) -> str:
        return f"UserData(id={self.id!r}, courses={self.courses!r}), videos={self.videos!r})"

class Course(Base):  # i.e. playlist
    __tablename__ = "course"
    id = Column(String, primary_key=True)  # YouTube playlist ID
    lectures = Column(String)  # JSON Array
    title = Column(String)
    description = Column(String)
    user_data = Column(String)  # JSON Object

    def __repr__(self) -> str:
        return f"Course(id={self.id!r}, lectures={self.lectures!r})"

class Lecture(Base):  # i.e. video
    __tablename__ = "lecture"
    id = Column(String, primary_key=True)  # YouTube video ID
    transcript_json = Column(String)
    transcript_string = Column(String)
    quiz_questions = relationship("QuizQuestion")  # Lecture -> QuizQuestion (one to many)
    supplemental_material = Column(String)  # JSON Object

    def __repr__(self) -> str:
        return f"Lecture(id={self.id!r}, transcript_json={self.transcript_json!r}, transcript_string={self.transcript_string!r}, supplemental_material={self.supplemental_material!r})"

class QuizQuestion(Base):
    __tablename__ = "quiz_question"
    id = Column(UUID(as_uuid=True), primary_key=True)  # Unique UUID
    lecture_id = Column(ForeignKey("lecture.id"))  # Lecture -> QuizQuestion (one to many)
    prompt = Column(String)
    question_type = Column(String)  # MC or F
    multiplechoice_options = Column(String)  # JSON Array
    multiplechoice_correctanswer_index = Column(Integer)
    freeresponse_correcttopics = Column(String)  # JSON Array

    def __repr__(self) -> str:
        return f"QuizQuestion(id={self.id!r}, lecture_id={self.lecture_id!r}, prompt={self.prompt!r}, question_type={self.question_type!r}, multiplechoice_options={self.multiplechoice_options!r}, multiplechoice_correctanswer_index={self.multiplechoice_correctanswer_index!r}, freeresponse_correcttopics={self.multiplechoice_correctanswer_index!r})"

class QuizQuestionResponse(Base):
    __tablename__ = "quiz_question_response"
    id = Column(String, primary_key=True)  # Unique UUID
    user_id = Column(ForeignKey("user_data.id"))  # User -> QuizQuestionResponse (one to many)
    quiz_question_id = Column(UUID(as_uuid=True), primary_key=True)  # Quiz Question UUID
    multiple_choice_response_index = Column(Integer)
    free_response_response = Column(String)
    free_response_feedback = Column(String)  # JSON Object

    def __repr__(self) -> str:
        return f"QuizQuestionResponse(id={self.id!r}, quiz_question_id={self.quiz_question_id!r}, user_id={self.user_id!r}, multiple_choice_response_index={self.multiple_choice_response_index!r}), free_response_response={self.free_response_response!r})"


# User:
# auth stuff
# Courses - Text[]

# Course:
# (primary key) - “youtube playlist id”
# Lectures - Text[]

# Lecture:
# (primary key) - “youtube playlist id”
# Transcript - JSON
# QuizQuestions - QuizQuestion[]

# QuizQuestion:                         
# (primary key) - UUID
# Lecture - Lecture
# Prompt - Text
# Type - “Multiple Choice” || “Short Free Response” || “Long Free Response”
# MultipleChoiceAnswers - Text[]
# MultipleChoiceCorrectAnswerIndex - Integer


# QuizQuestionResponse:          
# (primary key) - “quiz question uuid”
# MultipleChoiceResponseIndex - Integer
# FreeResponseResponse - Text

