"""
FastAPI 服务 — 供 LibreChat Actions 调用
启动：uvicorn agent_test.api_server:app --port 8099
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_test.mcp_server import _run, resolve_greenhouse_code

app = FastAPI(title="Agriculture Agent API", version="1.0.0")


class PredictionRequest(BaseModel):
    greenhouse: str  # 支持"一号棚"/"GH001"/1 等


@app.post("/disease_prediction", summary="病害预测")
def disease_prediction(req: PredictionRequest):
    try:
        code = resolve_greenhouse_code(req.greenhouse)
        summary = _run("disease_prediction", code)
        return {"greenhouse_code": code, "output_summary": summary}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/pest_control", summary="虫害防治")
def pest_control(req: PredictionRequest):
    try:
        code = resolve_greenhouse_code(req.greenhouse)
        summary = _run("pest_control", code)
        return {"greenhouse_code": code, "output_summary": summary}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
