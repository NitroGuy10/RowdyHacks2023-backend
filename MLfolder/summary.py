import openai
import dotenv
dotenv.load_dotenv()
import os
##Use your own openai.api_key
openai.api_key = os.environ["OPENAI_API_KEY"]

def summarize(transcript):

    default = "Summarize this as short as possible:"
    actualText = transcript
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= [{"role": "user", "content": default + '\n' + actualText}],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    answer = response["choices"][0]["message"]["content"]

    return(answer)
