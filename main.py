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


from typing import Union
import os
from fastapi import FastAPI, File, UploadFile
import speech_recognition as sr

app = FastAPI()

def convert_to_wav(source_path: str, destination_path: str):
    """
    Convert audio file to WAV format using ffmpeg.
    """
    os.system(f'ffmpeg -i "{source_path}" -acodec pcm_s16le -ar 44100 -ac 1 "{destination_path}"')

@app.post("/audio")
def process_audio(audio_file: UploadFile = File(...)):
    try:
        # Save the uploaded audio file
        file_path = f"/path/to/save/{audio_file.filename}"
        with open(file_path, "wb") as f:
            f.write(audio_file.file.read())

        # Convert to WAV format
        wav_file_path = f"/path/to/save/{audio_file.filename}.wav"
        convert_to_wav(file_path, wav_file_path)

        # Use SpeechRecognition to transcribe
        r = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = r.record(source)
        transcription = r.recognize_google(audio_data)
        return {"transcription": transcription}
    except Exception as e:
        return {"error": str(e)}
