# ============================================================
# pandas_demo — Python 3.13 开发环境镜像
# ============================================================
FROM python:3.13-slim

# 系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    libpng-dev \
    zlib1g-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 先复制依赖文件，利用 Docker layer 缓存
COPY requirements.txt .

# 安装 Python 依赖（sentence-transformers 体积较大，耐心等待）
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# HuggingFace 模型缓存目录
ENV HF_HOME=/app/huggingface_cache
ENV TRANSFORMERS_CACHE=/app/huggingface_cache

# 从 .env 读取配置（由 python-dotenv 在运行时加载）
# 敏感信息请勿写入镜像，统一通过 .env 或 docker-compose env_file 注入

EXPOSE 8888

# 默认启动 JupyterLab，也可在 docker-compose 中覆盖
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", \
     "--no-browser", "--allow-root", \
     "--NotebookApp.token=''", "--NotebookApp.password=''"]