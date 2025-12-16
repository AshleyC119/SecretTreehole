# 使用一个轻量且稳定的Python 3.10镜像作为基础
FROM python:3.10-slim

# 设置环境变量，防止Python输出被缓冲，确保日志实时显示
ENV PYTHONUNBUFFERED=1

# 设置工作目录为 /app，之后的命令都在此目录下执行
WORKDIR /app

# 首先只复制依赖列表文件，利用Docker缓存层，避免依赖未变时重复安装
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 将整个项目代码复制到容器的 /app 目录
COPY . .

# 切换到你的Django项目实际所在的src目录
WORKDIR /app/src

# 执行数据库迁移（生产环境通常需要这一步，也可在启动后手动执行）
RUN python manage.py migrate --noinput

# 声明容器运行时对外暴露的端口，需与Koyeb内部端口一致
EXPOSE 8000

# 使用gunicorn启动Django应用
# `--bind 0.0.0.0:8000` 表示监听所有网络接口的8000端口
# `--workers` 根据CPU核心数设置，对于免费实例，1个worker足够稳定
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]