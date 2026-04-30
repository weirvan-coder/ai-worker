# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse, PlainTextResponse

from agentscope.message import Msg
from agent.friday_agent import create_agent

_agent = None


def get_agent():
    global _agent
    if _agent is None:
        try:
            _agent = create_agent()
            print("[server] Friday Agent 初始化成功")
        except SystemExit:
            print("[server] Friday Agent 未配置模型，请设置 .env 后重启")
            _agent = None
    return _agent


_ready = False
_error_msg = ""


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _ready, _error_msg
    try:
        agent = get_agent()
        if agent:
            _ready = True
            print("[server] Friday Agent 就绪，监听 http://127.0.0.1:18080")
        else:
            _ready = False
            _error_msg = "未配置模型 API Key，请在 .env 中设置"
            print(f"[server] {_error_msg}")
            print("[server] 服务器仍可启动，等待模型配置后自动恢复")
    except Exception as e:
        _ready = False
        _error_msg = str(e)
        print(f"[server] Agent 启动失败: {e}")
    yield
    print("[server] 服务关闭")


app = FastAPI(title="AI Worker Bridge", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {
        "status": "ok" if _ready else "no_model",
        "agent": "Friday",
        "ready": _ready,
        "error": _error_msg if not _ready else "",
    }


@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    content = body.get("content", "").strip()
    if not content:
        return JSONResponse({"error": "empty content"}, status_code=400)

    agent = get_agent()
    if agent is None:
        return JSONResponse(
            {"error": _error_msg or "Agent 未就绪"},
            status_code=503,
        )

    msg = Msg("user", content, role="user")

    async def generate():
        try:
            response = await agent(msg)
            text = response.get_text_content()
            yield text
        except Exception as e:
            yield f"\n\n[ERROR] {str(e)}"

    return StreamingResponse(generate(), media_type="text/plain; charset=utf-8")


@app.get("/api/reports")
async def list_reports():
    from services.report_service import ReportService
    files = ReportService.list_reports()
    return {"reports": [os.path.basename(f) for f in files]}


@app.get("/api/reports/{filename:path}")
async def get_report(filename: str):
    from services.report_service import ReportService
    import urllib.parse
    safe_name = urllib.parse.unquote(filename)
    for f in ReportService.list_reports():
        if os.path.basename(f) == safe_name:
            with open(f, "r", encoding="utf-8") as fh:
                return PlainTextResponse(fh.read(), media_type="text/plain; charset=utf-8")
    return JSONResponse({"error": "not found"}, status_code=404)


@app.get("/api/models")
async def list_models():
    from config import PROVIDERS
    return {"providers": PROVIDERS}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=18080, log_level="info")
