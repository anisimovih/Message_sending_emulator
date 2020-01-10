FROM python:3.6-slim
WORKDIR /app_code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY message_sender Message_sending_emulator manage.py ./