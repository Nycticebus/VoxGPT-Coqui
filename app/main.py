import json
import time
from fastapi import FastAPI, UploadFile, BackgroundTasks, Header
from fastapi.responses import FileResponse
import openai
import shutil
import uuid
import ffmpeg
import base64
from fastapi.staticfiles import StaticFiles
import os
from TTS.api import TTS

# Set up app before running
AI_COMPLETION_MODEL = os.getenv("AI_COMPLETION_MODEL", "gpt-3.5-turbo")
LANGUAGE = os.getenv("LANGUAGE", "en")

# Launch app
app = FastAPI()

# Request creator
@app.post("/inference")
async def infer(audio: UploadFile, background_tasks: BackgroundTasks,
                conversation: str = Header(default=None)) -> FileResponse:
    print("received request")
    start_time = time.time()

    user_prompt = await transcribe(audio)
    ai_response = await get_completion(user_prompt, conversation)

    output_audio_filepath = to_audio(ai_response)
    background_tasks.add_task(delete_file, output_audio_filepath)

    print('total processing time:', time.time() - start_time, 'seconds')

    return FileResponse(path=output_audio_filepath, media_type="audio/mpeg",
                        headers={"text": construct_response_header(user_prompt, ai_response)})


app.mount("/", StaticFiles(directory="app/static", html=True), name="static")

# Transcribe Audio input recording
async def transcribe(audio):
    start_time = time.time()
    initial_filepath = f"/tmp/{uuid.uuid4()}{audio.filename}"

    with open(initial_filepath, "wb+") as file_object:
        shutil.copyfileobj(audio.file, file_object)

    converted_filepath = f"/tmp/ffmpeg-{uuid.uuid4()}{audio.filename}"

    print("running through ffmpeg")
    (
        ffmpeg
        .input(initial_filepath)
        .output(converted_filepath, loglevel="error")
        .run()
    )
    print("ffmpeg done")

    delete_file(initial_filepath)

    read_file = open(converted_filepath, "rb")

    print("calling whisper")
    transcription = (await openai.Audio.atranscribe("whisper-1", read_file, language=LANGUAGE))["text"]
    print("STT response received from whisper in", time.time() - start_time, 'seconds')
    print('user prompt:', transcription)

    delete_file(converted_filepath)

    return transcription

# Send message to ChatGPT 
async def get_completion(user_prompt, conversation_thus_far):
    start_time = time.time()
    messages = [
        {"role": "system",
         "content": f"You are a helpful assistant with a voice interface. Keep your responses succinct since the user is interacting with you through a voice interface. Your responses should be a few sentences at most. Always provide your responses in the language that corresponds to the ISO-639-1 code: {LANGUAGE}."}
    ]
    messages.extend(get_additional_initial_messages())
    messages.extend(json.loads(base64.b64decode(conversation_thus_far)))
    messages.append({"role": "user", "content": user_prompt})

    print("calling", AI_COMPLETION_MODEL)
    res = await openai.ChatCompletion.acreate(model=AI_COMPLETION_MODEL, messages=messages, timeout=15)
    print("response received from", AI_COMPLETION_MODEL, "in", time.time() - start_time, "seconds")

    completion = res['choices'][0]['message']['content']
    print(AI_COMPLETION_MODEL, "response:", completion)

    return completion


def get_additional_initial_messages():
    match AI_COMPLETION_MODEL:
        case "gpt-3.5-turbo":
            return [{"role": "user",
                     "content": f"Make sure you always strictly provide your responses in the language that corresponds to the ISO-639-1 code: {LANGUAGE}."}]
        case _:
            return []

# Convert ChatGPT's response to an Audio File with Coqui TTS
def to_audio(textInput):
    start_time = time.time()
    # Init TTS with the target model name
    tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=True, gpu=True)
    # set filepath
    filepath = f"/tmp/{uuid.uuid4()}.mp3"
    # Run TTS
    tts.tts_to_file(text=textInput, speaker=tts.speakers[3], file_path=filepath)
    
    print('TTS time:', time.time() - start_time, 'seconds')
    return filepath

# Clean Up
def delete_file(filepath: str):
    os.remove(filepath)

# Make Response parsable upon receipt from ChatGPT
def construct_response_header(user_prompt, ai_response):
    return base64.b64encode(
        json.dumps(
            [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": ai_response}]).encode(
            'utf-8')).decode("utf-8")
