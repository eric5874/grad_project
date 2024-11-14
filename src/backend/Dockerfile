FROM python:3.11

# 更新并安装所需的编译器
RUN apt update && apt install -y gcc g++

# 复制依赖文件
COPY requirements.txt /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 使用 python3 -m pip 安装依赖
RUN python3 -m pip install --no-cache -r requirements.txt

# 复制应用文件到容器
COPY . /app

# 暴露端口
EXPOSE 8000

# 设置容器启动命令
CMD ["python3", "main.py"]
