FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip gcc g++

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "Home.py"]