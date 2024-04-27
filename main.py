# from typing import Union

# from fastapi import FastAPI,File, UploadFile

# import speech_recognition as sr


# app = FastAPI()


# @app.post("/audio")
# def read_root(audio_file: UploadFile = File(...)):
    
    
#     r = sr.Recognizer()
#     with sr.WavFile(audio_file.file) as source:              # use "test.wav" as the audio source
#         audio = r.record(source)                        # extract audio data from the file

#     try:
#         print("Transcription: " + r.recognize(audio)) 
#         out = r.recognize(audio)
        
#         # recognize speech using Google Speech Recognition
#     except LookupError:                                 # speech is unintelligible
#         print("Could not understand audio")
#     return {"text": out}




from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import speech_recognition as sr

app = FastAPI()

@app.post("/audio")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        r = sr.Recognizer()
        with sr.WavFile(audio_file.file) as source:
            audio = r.record(source)
        
        transcription = r.recognize_google(audio)  # You can use any other speech recognition method here
        
        return {"transcription": transcription}
    
    except sr.AudioFileError as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": "Failed to transcribe audio"})
