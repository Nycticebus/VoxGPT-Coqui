FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10-slim

WORKDIR /

ENV MAX_WORKERS=5
ENV AUDIO_SPEED=1
ENV OPENAI_API_KEY="[redacted]"

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade -r /app/requirements.txt

RUN apt-get update && apt-get install -y ffmpeg && apt-get install -y espeak-ng

COPY ./app /app
