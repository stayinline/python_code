"""
MCP Server — 将 Agent API 包装为 LibreChat 可调用的工具

安装依赖：pip install mcp

在 LibreChat 的 librechat.yaml 中配置：
  mcpServers:
    agriculture-agent:
      command: python
      args:
        - D:/code/python/pandas_demo/agent_test/mcp_server.py

用户在对话中提问示例：
  "一号棚的病害预测是怎样的？"
  "帮我查一下 GH003 的病害情况"
"""

import time
import requests
from mcp.server.fastmcp import FastMCP

BASE_URL = "http://192.168.1.97:8012/api/v1"
API_KEY = "28e6d8a5eb18a1b370ea5f9e405f879dafabea297e3eb1bf0a96b2aefc811d09"
BASE_ID = "664259595006021"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

TERMINAL_STATUSES = {"completed", "failed", "dead"}

# 温室编号映射：支持"一号棚"/"1号棚"/"GH001" 等多种输入
GREENHOUSE_ALIAS = {
    "一": "GH001", "1": "GH001", "gh001": "GH001",
    "二": "GH002", "2": "GH002", "gh002": "GH002",
    "三": "GH003", "3": "GH003", "gh003": "GH003",
    "四": "GH004", "4": "GH004", "gh004": "GH004",
    "五": "GH005", "5": "GH005", "gh005": "GH005",
    "六": "GH006", "6": "GH006", "gh006": "GH006",
    "七": "GH007", "7": "GH007", "gh007": "GH007",
    "八": "GH008", "8": "GH008", "gh008": "GH008",
    "九": "GH009", "9": "GH009", "gh009": "GH009",
}


def resolve_greenhouse_code(raw: str) -> str:
    """将用户输入的温室标识标准化为 GHxxx 格式。"""
    key = raw.strip().lower().replace("号棚", "").replace("棚", "").replace("#", "")
    code = GREENHOUSE_ALIAS.get(key)
    if code is None:
        raise ValueError(f"无法识别温室编号：{raw!r}，支持的输入：一/1/GH001 … 九/9/GH009")
    return code


def _invoke(agent_id: str, greenhouse_code: str) -> str:
    payload = {"base_id": BASE_ID, "agent_id": agent_id, "greenhouse_code": greenhouse_code}
    resp = requests.post(f"{BASE_URL}/agents/invoke", json=payload, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    request_id = data.get("request_id") or data.get("data", {}).get("request_id")
    if not request_id:
        raise ValueError(f"响应中未找到 request_id: {data}")
    return request_id


def _poll(request_id: str, interval: float = 2.0, timeout: float = 300.0) -> dict:
    url = f"{BASE_URL}/agents/tasks/{request_id}"
    elapsed = 0.0
    while elapsed < timeout:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        task = resp.json().get("data", {})
        if task.get("status") in TERMINAL_STATUSES:
            return task
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"任务 {request_id} 超时（{timeout}s）")


def _run(agent_id: str, greenhouse_code: str) -> str:
    request_id = _invoke(agent_id, greenhouse_code)
    task = _poll(request_id)
    if task.get("status") != "completed":
        raise RuntimeError(f"任务未成功，状态: {task.get('status')}")
    return task.get("output_summary", "（无输出）")


# ── MCP Server ──────────────────────────────────────────────────────────────

mcp = FastMCP("agriculture-agent")


@mcp.tool()
def disease_prediction(greenhouse: str) -> str:
    """
    查询指定温室的病害预测结果。
    参数 greenhouse：温室编号，支持"一号棚"、"1号棚"、"GH001" 等格式（1-9号）。
    """
    code = resolve_greenhouse_code(greenhouse)
    return _run("disease_prediction", code)


@mcp.tool()
def pest_control(greenhouse: str) -> str:
    """
    查询指定温室的虫害防治建议。
    参数 greenhouse：温室编号，支持"一号棚"、"1号棚"、"GH001" 等格式（1-9号）。
    """
    code = resolve_greenhouse_code(greenhouse)
    return _run("pest_control", code)


if __name__ == "__main__":
    mcp.run()
