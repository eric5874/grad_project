#FROM python:3.11

#RUN apt update && apt install -y gcc g++

#ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
#RUN /install.sh && rm /install.sh

#COPY requirements.txt /app/requirements.txt

#WORKDIR /app

#RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

#COPY . /app

#EXPOSE 8000

#CMD ["python3", "main.py"]
FROM python:3.11

# 安裝系統必要依賴
RUN apt update && apt install -y gcc g++

# 安裝自定義工具，如有需要再安裝 `uv`，否則可以省略
# ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
# RUN /install.sh && rm /install.sh

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY . /app

# 開放 8000 埠並執行
EXPOSE 8000
CMD ["python3", "main.py"]