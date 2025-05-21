# 使用官方Python运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /usr/src/app

# 将当前目录内容复制到容器中的/usr/src/app目录下
COPY . .

# 更新包列表并安装必要的系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip install -r requirements.txt

# 创建SQLite数据库文件（如果需要的话，可以根据实际情况调整）
RUN python manage.py makemigrations && \
    python manage.py migrate

# 暴露端口8000，这是Django开发服务器默认监听的端口
EXPOSE 8000

# 启动命令，这里我们直接使用Django内置的服务器来启动应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]