FROM python:3.8

RUN apt-get update && apt-get install -y ffmpeg alsa-utils

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt requirements.txt
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt
COPY . .


CMD ["python3.8", "main.py"]