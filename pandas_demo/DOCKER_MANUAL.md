# pandas_demo Docker 操作手册

## 目录
1. [环境要求](#1-环境要求)
2. [快速启动](#2-快速启动)
3. [配置说明](#3-配置说明)
4. [服务清单](#4-服务清单)
5. [常用操作](#5-常用操作)
6. [运行各模块](#6-运行各模块)
7. [连接外部已有服务](#7-连接外部已有服务)
8. [常见问题](#8-常见问题)

---

## 1. 环境要求

| 软件 | 最低版本 | 说明 |
|------|---------|------|
| Docker Desktop | 24.x | Windows/Mac/Linux 均可 |
| docker-compose | v2.x | Desktop 版本已内置 |
| 可用内存 | 8 GB+ | Weaviate + Kafka + ClickHouse 合计约 3 GB |
| 磁盘空间 | 20 GB+ | 含模型缓存、数据卷 |

---

## 2. 快速启动

### 第一步：准备配置文件

```bash
# 进入项目目录
cd D:\code\python\pandas_demo

# 复制环境变量模板
cp .env.example .env

# 用编辑器打开 .env，填入真实的 API Key 和密码
# 重要：.env 不要提交到 Git！
notepad .env
```

### 第二步：构建并启动所有服务

```bash
# 首次构建（约 10-20 分钟，需下载镜像和安装依赖）
docker compose up -d --build

# 查看启动状态
docker compose ps
```

### 第三步：访问 JupyterLab

浏览器打开：http://localhost:8888

首次访问无需密码，可直接使用。

---

## 3. 配置说明

### `.env` 文件各配置项

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `PG_TEST_HOST` | PostgreSQL 测试环境地址 | `postgres`（容器内）或 `10.10.2.30` |
| `PG_TEST_PASSWORD` | PostgreSQL 密码 | — |
| `CK_HOST` | ClickHouse 地址 | `clickhouse`（容器内）或 `192.168.1.124` |
| `KAFKA_BROKERS` | Kafka 地址 | `kafka:9092`（容器内）|
| `WEAVIATE_HOST` | Weaviate 地址 | `weaviate`（容器内）|
| `MODEL_API_KEY` | 阿里云百炼 API Key | `sk-xxxxx` |
| `OLLAMA_BASE_URL` | Ollama 地址 | `http://ollama:11434` |

> **注意**：`docker-compose.yml` 中的 `environment` 段会覆盖 `.env` 中同名变量，
> 将各服务地址替换为容器名，保证容器间互联。如需对接局域网真实服务，
> 请删除 `docker-compose.yml` 对应的 `environment` 覆盖行。

---

## 4. 服务清单

| 服务 | 容器名 | 对外端口 | 说明 |
|------|--------|---------|------|
| Python 应用 | pandas_demo_app | 8888 | JupyterLab |
| PostgreSQL | pandas_demo_postgres | 5432 | 工作流数据库 |
| ClickHouse | pandas_demo_clickhouse | 8123 / 9000 | 分析数据库 |
| Kafka | pandas_demo_kafka | 9092 | 消息队列 |
| Zookeeper | pandas_demo_zookeeper | — | Kafka 依赖 |
| Weaviate | pandas_demo_weaviate | 18080 / 50051 | 向量数据库 |
| Ollama | pandas_demo_ollama | 11434 | 本地 LLM（可选）|

---

## 5. 常用操作

### 启动 / 停止

```bash
# 启动所有服务
docker compose up -d

# 停止所有服务（保留数据）
docker compose down

# 停止并删除所有数据卷（⚠️ 数据会丢失）
docker compose down -v
```

### 查看日志

```bash
# 查看所有服务日志
docker compose logs -f

# 只看 app 服务日志
docker compose logs -f app

# 只看 kafka 日志
docker compose logs -f kafka
```

### 进入容器执行命令

```bash
# 进入 Python 应用容器的 bash
docker compose exec app bash

# 在容器内执行单个脚本
docker compose exec app python kafka_test/agriculture/main.py

# 进入 PostgreSQL 客户端
docker compose exec postgres psql -U postgres -d labillion-workflow
```

### 重建镜像（修改了 requirements.txt 或 Dockerfile 后）

```bash
docker compose build app
docker compose up -d app
```

### 只启动部分服务

```bash
# 只启动 app + postgres（不启动 Kafka 等）
docker compose up -d app postgres
```

---

## 6. 运行各模块

进入容器后，按照以下方式运行各模块脚本：

```bash
# 进入容器
docker compose exec app bash
```

### Pandas 基础教程

```bash
python 1_base.py
python 2_dataframe.py
python 4_clean.py
```

### Kafka 农业传感器数据生成

```bash
# 启动前确保 Kafka 已就绪（docker compose ps 确认状态）
python kafka_test/agriculture/main.py
```

### Weaviate 向量搜索

```bash
# 文本向量化 Demo
python weaviate_test/demo1.py

# 以图搜图 Demo（需提前下载 CLIP 模型，首次运行较慢）
python weaviate_test/demo_image_search.py
```

### ClickHouse 向量查询

```bash
python clickhouse_test/demo_query_with_vector.py
```

### 大模型测试（需配置 .env 中的 MODEL_API_KEY）

```bash
python llm_test/test_api_key.py
python llm_test/test_vision.py
```

### PostgreSQL → ClickHouse DDL 转换

```bash
python clickhouse_test/pg_to_ck.py
```

### Marimo 交互应用

```bash
marimo run app.py --host 0.0.0.0 --port 2718
# 浏览器访问 http://localhost:2718
```

需要同时在 `docker-compose.yml` 的 `app` service 中暴露 `2718` 端口，或直接修改命令。

---

## 7. 连接外部已有服务

如果你的 PostgreSQL、ClickHouse、Kafka、Weaviate 已经部署在局域网服务器上，
不需要启动对应的容器，只需修改 `.env` 和 `docker-compose.yml`：

**方法一（推荐）**：修改 `.env` 中的 HOST 地址为局域网 IP，
然后删除 `docker-compose.yml` `app` service 中 `environment` 段内对应的覆盖行。

**方法二**：只启动 `app` 服务：

```bash
# 不启动基础设施，只启动 Python 应用
docker compose up -d app

# .env 中的地址会直接生效，指向局域网服务器
```

---

## 8. 常见问题

### Q: 构建时 sentence-transformers 安装超时？

sentence-transformers 依赖 PyTorch，体积约 2-3 GB。建议配置国内镜像源：

在 `Dockerfile` 中 pip install 行替换为：
```dockerfile
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### Q: Kafka 连接失败？

确认 Kafka 和 Zookeeper 都已健康启动：
```bash
docker compose ps
docker compose logs kafka | tail -20
```

容器内使用 `kafka:9092`，容器外（本机）使用 `localhost:9092`。

### Q: Weaviate 查询时模型报错？

`docker-compose.yml` 中 Weaviate 配置了 `DEFAULT_VECTORIZER_MODULE: none`，
意味着向量化由 Python 代码（sentence-transformers/Ollama）自行完成，
这与项目中 `demo_image_search.py` 和 `demo3_ollama_vector.py` 的做法一致。

### Q: HuggingFace 模型下载太慢？

设置镜像加速：
```bash
# 在 .env 中添加
HF_ENDPOINT=https://hf-mirror.com
```

### Q: 如何只打一个独立镜像（不用 docker-compose）？

```bash
# 构建镜像
docker build -t pandas_demo:latest .

# 运行（挂载当前目录，传入 .env）
docker run -it --rm \
  -p 8888:8888 \
  -v $(pwd):/app \
  --env-file .env \
  pandas_demo:latest
```

### Q: Ollama 如何下载模型？

```bash
# 进入 Ollama 容器
docker compose exec ollama bash

# 下载 nomic-embed-text 嵌入模型
ollama pull nomic-embed-text

# 下载对话模型（按需选择）
ollama pull qwen2.5:7b
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `Dockerfile` | Python 应用镜像构建文件 |
| `docker-compose.yml` | 完整服务编排配置 |
| `.env.example` | 环境变量模板（复制为 `.env` 使用）|
| `.dockerignore` | 构建时排除的文件列表 |
| `requirements.txt` | Python 依赖包列表 |
| `DOCKER_MANUAL.md` | 本操作手册 |
