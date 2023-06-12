FROM python:latest

WORKDIR /etlcode

COPY requirements.txt .
RUN pip3.11 install -r requirements.txt

COPY src/ . 

COPY requirements.txt /etlcode


CMD [ "python", "./app.py" ]