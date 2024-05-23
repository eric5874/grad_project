FROM python:3.11

RUN apt update && apt install -y gcc g++

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

CMD ["python3", "app.py"]