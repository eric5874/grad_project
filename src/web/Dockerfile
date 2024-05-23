FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip gcc g++

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "app.py"]