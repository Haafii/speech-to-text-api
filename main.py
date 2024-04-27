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
import os
import tempfile
import wave

app = FastAPI()

@app.post("/audio")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    try:
        # Save the uploaded file locally
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await audio_file.read())
            tmp_file_path = tmp_file.name
        
        # Verify the format of the saved file
        with wave.open(tmp_file_path, 'rb') as wav_file:
            if wav_file.getnchannels() != 2 or wav_file.getsampwidth() != 2:
                raise ValueError("Invalid WAV file format. Channels: {}, Sample Width: {}".format(wav_file.getnchannels(), wav_file.getsampwidth()))

        # If format verification succeeds, proceed with transcription
        # Add your transcription logic here
        
        return {"status": "success"}

    except Exception as e:
        return {"error": str(e)}
    finally:
        # Remove the temporary file
        os.unlink(tmp_file_path)

