FROM python:3.11

RUN apt update && apt install -y gcc g++

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY requirements.txt /app/requirements.txt

WORKDIR /app

# 使用 python3 -m pip 安装依赖
RUN /root/.cargo/bin/uv python3 -m pip install --system --no-cache -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python3", "main.py"]
