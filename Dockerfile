# 使用官方 Python 3.11 轻量镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /code

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制应用代码
COPY . .

# 暴露端口（与 FC 监听端口一致）
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]