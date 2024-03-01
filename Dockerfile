FROM python:3.13.0a4-slim

WORKDIR /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt

COPY . /app


CMD [ "python3", "-O",  "main.py" ]
