import openai

##Use your own openai.api_key
openai.api_key = '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'

def summarize(transcript):

    default = "Summarize this as short as possible:"
    actualText = transcript
    response = openai.Completion.create(
    model="gpt-3.5-turbo",
    prompt= default + "\n\n" + actualText,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    answer = response["choices"][0]["text"]

    return(answer)
