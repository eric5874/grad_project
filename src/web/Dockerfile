FROM ubuntu:22.04

RUN apt update && apt install -y python3 python3-pip curl wget iputils-ping

RUN pip3 install -U pip

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN uv pip install --system --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "Home.py"]