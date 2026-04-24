"""
Agent API 调用 Demo
流程：
  1. POST /agents/invoke  → 获取 request_id
  2. 轮询 GET /agents/tasks/{request_id} → 等待 completed
  3. 提取 output_summary
"""

import time
import requests

BASE_URL = "http://192.168.1.97:8012/api/v1"
API_KEY = "28e6d8a5eb18a1b370ea5f9e405f879dafabea297e3eb1bf0a96b2aefc811d09"

HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json",
}

TERMINAL_STATUSES = {"completed", "failed", "dead"}


def invoke_agent(payload: dict) -> str:
    """调用 Agent，返回 request_id。"""
    url = f"{BASE_URL}/agents/invoke"
    resp = requests.post(url, json=payload, headers=HEADERS, timeout=30)
    if not resp.ok:
        print(f"[invoke] HTTP {resp.status_code}  response body:\n{resp.text}")
    resp.raise_for_status()
    data = resp.json()
    request_id = data.get("request_id") or data.get("data", {}).get("request_id")
    if not request_id:
        raise ValueError(f"响应中未找到 request_id: {data}")
    print(f"[invoke] request_id = {request_id}")
    return request_id


def poll_task(request_id: str, interval: float = 2.0, timeout: float = 300.0) -> dict:
    """轮询任务状态，直到终态，返回 data 字段。"""
    url = f"{BASE_URL}/agents/tasks/{request_id}"
    elapsed = 0.0
    while elapsed < timeout:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        task = body.get("data", {})
        status = task.get("status", "unknown")
        print(f"[poll] status = {status}  (elapsed {elapsed:.0f}s)")
        if status in TERMINAL_STATUSES:
            return task
        time.sleep(interval)
        elapsed += interval
    raise TimeoutError(f"任务 {request_id} 在 {timeout}s 内未完成")


def run_agent(payload: dict) -> str:
    """端到端调用：invoke → poll → 返回 output_summary。"""
    request_id = invoke_agent(payload)
    task = poll_task(request_id)

    status = task.get("status")
    if status != "completed":
        raise RuntimeError(f"任务未成功完成，最终状态: {status}\ntask={task}")

    output_summary = task.get("output_summary", "")
    return output_summary


if __name__ == "__main__":
    # 示例 payload，根据实际 Agent 接口调整
    example_payload = {
        "base_id": "664259595006021",
        "agent_id": "disease_prediction",
        # "greenhouse_code": "GH001",
        # "greenhouse_code": "GH002",
        "greenhouse_code": "GH009",
    }

    try:
        summary = run_agent(example_payload)
        print("\n===== output_summary =====")
        print(summary)
    except Exception as e:
        print(f"[ERROR] {e}")
