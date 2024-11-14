FROM python:3.11

# 安装依赖工具
RUN apt update && apt install -y gcc g++ curl

# 安装 uv 工具
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# 将 requirements.txt 复制到容器中
COPY requirements.txt /app/requirements.txt

# 设置工作目录
WORKDIR /app

# 确保 uv 工具安装成功，并且路径正确
# 使用 uv 安装 Python 依赖
RUN /root/.cargo/bin/uv --version && /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt

# 复制其余应用文件到容器
COPY . /app

# 暴露端口
EXPOSE 8000

# 设置容器启动命令
CMD ["python3", "main.py"]
