import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import json

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

#Example Video: Shell vs. Editor?
video_id = 'bHIhgxav9LY'
exampleTranscript = YouTubeTranscriptApi.get_transcript(video_id)
fullTranscript = "This is the transcript: "
for i in range(len(exampleTranscript)):
    fullTranscript += " " + exampleTranscript[i]["text"]
#print(fullTranscript)

##Use your own openai.api_key
openai.api_key = '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'



questionsPrompt = 'Can you give me a quiz with answers based on the transcript. The quiz should have multiple choice questions with one correct answer and multiple incorrect answer choices given. The quiz should also have free response questions where the answer is a list of important topics in an correct answer to that question. Give 5 multiple choice questions and 2 free response questions. Make sure the answer is related to the transcript subject. Also, give a study guide and plan to cover all the material covered in the transcript. The study guide should have a breakdown/summary of topics and their main points. Give resources to learn each of the main topics as well as some advice and internet links to the resources. Please give me this information in JSON format. An example is this: [{"quiz questions": [MC: multiple choice question 1, MC: multiple choice question 2, F: free response question 1, F: free response question 2 ], "quiz answers": [[MC: multiple choice question 1 correct answer, MC: multiple choice question 1 incorrect answer 1, MC: multiple choice question 1 incorrect answer 2], [MC: multiple choice question 2 correct answer, MC: multiple choice question 2 incorrect answer 1, MC: multiple choice question 2 incorrect answer 2], [[F: free response question 1 answer topics], [F: free response question 2 answer topics]], "Study Guide": [StudyguideLine1, StudyguideLine2, StudyguideLine3], "Resources": ["Resource1 and web link to Resource1, Resource2 and web link to Resource2]}. Remember to put a \\ before any \" or \' you use. If the question or answer is of multiple choice, start it with the characters \'MC:\' and if the question or answer is of free response, start it with the characters \'FC:\' as indicated in the example. Make sure it it is in the format of a JSON and the example. Do not return any output besides the JSON formatted section. The content of the transcript is as follows: '
qAndA = []

runs = len(fullTranscript) / (4097 * 4)

for i in range(int(runs)):
    
    actualText = "".join(fullTranscript[i*(4097 * 4):(i+1)*(4097 * 4)])
    print(questionsPrompt + actualText)
    questionResponse = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [{"role": "user", "content": questionsPrompt + actualText}],
    temperature=0.0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )



    qAndA.append(questionResponse["choices"][0]["message"]["content"])

actualText = "".join(fullTranscript[(int(runs))*(4097 * 4):])
questionResponse = openai.ChatCompletion.create(
model="gpt-3.5-turbo",
messages= [{"role": "user", "content": questionsPrompt + actualText}],
temperature=0.0,
top_p=1,
frequency_penalty=0,
presence_penalty=0
)

qAndA.append(questionResponse["choices"][0]["message"]["content"])

for i in qAndA:
   if is_json(i):
      print(True)

