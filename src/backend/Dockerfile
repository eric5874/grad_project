FROM python:3.11

RUN apt update && apt install -y gcc g++

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

COPY . /app

CMD ["python3", "main.py"]