'''REST API that provides speech transcription
in the form json response
There is no authorization as it is. If it is needed, please specify
'''

from fastapi import FastAPI

app = FastAPI()


@app.get("/greetings")
async def transcribe():

    hello_dict = {
        'greetings': 'Hello World!'
    }

    return hello_dict
