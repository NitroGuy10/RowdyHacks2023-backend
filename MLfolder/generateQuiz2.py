import os
import openai
from dotenv import load_dotenv
load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi
import json
import time
import database

PRINTING_OR_SAVING = True  # False for printing, true for saving

##Use your own openai.api_key
openai.api_key = os.environ["OPENAI_API_KEY"]

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def getQuizJSON(video_id, timeLimit):
    # video_id = 'bHIhgxav9LY'
    exampleTranscript = YouTubeTranscriptApi.get_transcript(video_id)
    fullTranscript = "This is the transcript: "
    for i in range(len(exampleTranscript)):
        fullTranscript += " " + exampleTranscript[i]["text"]

    questionsPrompt = 'Can you give me a quiz with answers based on the transcript. The quiz should have multiple choice questions with one correct answer and multiple incorrect answer choices given. The quiz should also have free response questions where the answer is a list of important topics in an correct answer to that question. Give 2 multiple choice question and 1 free response question. Make sure the answer is related to the transcript subject. Also, give a study guide and plan to cover all the material covered in the transcript. The study guide should have a breakdown/summary of topics and their main points. Give resources to learn each of the main topics as well as some advice and internet links to the resources. Please give me this information in JSON format. An example is this: {"quiz questions": [MC: multiple choice question 1, MC: multiple choice question 2, F: free response question 1, F: free response question 2 ], "quiz answers": [[MC: multiple choice question 1 correct answer, MC: multiple choice question 1 incorrect answer 1, MC: multiple choice question 1 incorrect answer 2], [MC: multiple choice question 2 correct answer, MC: multiple choice question 2 incorrect answer 1, MC: multiple choice question 2 incorrect answer 2]], [[F: free response question 1 answer topics], [F: free response question 2 answer topics]], "Study Guide": [StudyguideLine1, StudyguideLine2, StudyguideLine3], "Resources": ["Resource1 and web link to Resource1, Resource2 and web link to Resource2]}. Remember to put a \\ before any \" or \' you use. If the question or answer is of multiple choice, start it with the characters \'MC:\' and if the question or answer is of free response, start it with the characters \'FC:\' as indicated in the example. Make sure it it is in the format of a JSON and the example. Do not return any output besides the JSON formatted section. The content of the transcript is as follows: '

    checks = 100

    runs = len(fullTranscript) / (checks * 4)

    runningTime = 0
    i = 0

    #Main iteration through video
    #While less than time limit and within video transcript bound
    while i in range(int(runs)) and runningTime <= timeLimit:

        #OpenAI api call
        start = time.time()
        actualText = "".join(fullTranscript[i*(checks * 4):(i+1)*(checks * 4)])
        questionResponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "user", "content": questionsPrompt + actualText}],
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )


        a = questionResponse["choices"][0]["message"]["content"]

        #Temp (REMOVE LATER) print JSON output
        # print(a)

        # (ADD LATER) if function is eligible json format -> pass to database
        if (is_json(a)):
          if PRINTING_OR_SAVING:
            database.save_lecture_material(video_id, json.loads(a))
          else:
             print(a)

        #Increment Time
        end = time.time()
        runningTime += end - start

        #Inc check (video transcript) block
        i += 1


    #Check last hanging content in video (Last loop)
    if runningTime <= timeLimit:

        actualText = "".join(fullTranscript[(int(runs))*(checks * 4):])
        questionResponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= [{"role": "user", "content": questionsPrompt + actualText}],
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        #Temp (REMOVE LATER) print JSON output
        # print(a)

        # (ADD LATER) if function is eligible json format -> pass to database
        if (is_json(a)):
          if PRINTING_OR_SAVING:
            database.save_lecture_material(video_id, json.loads(a))
          else:
             print(a)


    

# getQuizJSON('MqnpIwN7dz0', 60)