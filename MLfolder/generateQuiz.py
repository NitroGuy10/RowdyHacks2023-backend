import os
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import json
import time
import re
from nltk import tokenize
from dotenv import load_dotenv
load_dotenv()



video_id = 'YRgBLVI3suM'
# video_id = 'MqnpIwN7dz0'
exampleTranscript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US', 'en'])
fullTranscript = "This is the transcript: "
for i in range(len(exampleTranscript)):
    fullTranscript += " " + exampleTranscript[i]["text"]
#print(fullTranscript)

##Use your own openai.api_key
openai.api_key = os.environ["OPENAI_API_KEY"]






#Add back study guide
#Add back resources/advice


def parseResponse(response):
    words = tokenize.sent_tokenize(response)

    mcq = []
    mcaC = []
    mcaI = []
    frq = []
    fra = []

    onTerm = "mcq"

    for i in range(len(words)):
        if 'Multiple Choice Questions:' in words[i]:
            onTerm = "mcq"
        if '(Correct)' in words[i]:
            onTerm = "mcaC"
        if '(Incorrect)' in words[i]:
            onTerm = "mcaI"
        if 'Free Response Questions' in words[i]:
            onTerm = "frq"
        if 'Free Response Answers' in words[i]:
            onTerm = "fra"

        word = words[i].split(':')[-1]
        word = word.replace('\n', "")
        if '(Correct)' in word:
            word = word.replace('(Correct)', "")
        if '(Incorrect)' in word:
            word = word.replace('(Incorrect)', "")
        if onTerm == "mcq":
            mcq.append(word)
        if onTerm == "mcaC":
            mcaC.append(word)
        if onTerm == "mcaI":
            mcaI.append(word)
        if onTerm == "frq":
            frq.append(word)
        if onTerm == "fra":
            fra.append(word)

    formatDict = {}
    listSet = [mcq, mcaC, mcaI, frq, fra]
    listSetLabels = ["Multiple Choice Questions", "Correct Multiple Choice Answers", "Incorrect Multiple Choice Answers", "Free Response Questions", "Free Response Answers"]
    for j in range(len(listSetLabels)):
        formatDict[listSetLabels[j]] = listSet[j]
    print(json.dumps(formatDict))
    return(json.dumps(formatDict))
        



questionsPrompt = 'Give me a question and an answer seperated by a space with no labels. There should be no punctuation in the end result and no formatting. based on this paragraph: '


split = 500
runs = len(fullTranscript) / (split * 4)
for i in range(int(runs)):
    print(i, '/', int(runs) + 1)
    start = time.time()
    actualText = "".join(fullTranscript[i*(split * 4):(i+1)*(split * 4)])
    questionResponse = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [{"role": "user", "content": questionsPrompt + actualText}],
    temperature=0.0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    ret = questionResponse["choices"][0]["message"]["content"]
    print(ret)

    # formatPrompt = "Replace the questions in the following transcript line to fit this format: Question 1: text of question? The transcript is:["
    # formatResponse = openai.ChatCompletion.create(
    # model="gpt-3.5-turbo",
    # messages= [{"role": "user", "content": formatPrompt + ret}],
    # temperature=0.0,
    # top_p=1,
    # frequency_penalty=0,
    # presence_penalty=0
    # )

    # ret = formatResponse["choices"][0]["message"]["content"]
    # print(ret)
    # parseResponse(ret)








# actualText = "".join(fullTranscript[(int(runs))*(split * 4):])
# questionResponse = openai.ChatCompletion.create(
# model="gpt-3.5-turbo",
# messages= [{"role": "user", "content": questionsPrompt + actualText}],
# temperature=0.0,
# top_p=1,
# frequency_penalty=0,
# presence_penalty=0
# )
# ret = questionResponse["choices"][0]["message"]["content"]

# parseResponse(ret)





