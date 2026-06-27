import uuid
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from schemas import AgentPayload
from security_core import evaluate_prompt
import sys
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI(
    title="AI Kavach Backend API",
    description="Backend API for AI prompt injection detection and security evaluation.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Home Route
# -----------------------------
@app.get("/", summary="Backend Status")
def home():
    return {
        "message": "AI Kavach Backend Running"
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health", summary="Health Check")
def health():
    return {
        "status": "healthy",
        "service": "AI Kavach Backend"
    }


# -----------------------------
# Echo Test
# -----------------------------
@app.post("/test", summary="Echo Test")
def test(payload: AgentPayload):
    return {
        "agent": payload.agent_name,
        "query": payload.user_query
    }


# -----------------------------
# Prompt Security Evaluation
# -----------------------------
@app.post("/v1/proxy/evaluate", summary="Evaluate User Prompt")
def evaluate(payload: AgentPayload):
    return evaluate_prompt(payload.user_query)


# -----------------------------
# Frontend Integration API
# -----------------------------
@app.post("/v1/chat", summary="Frontend Chat API")
def chat(payload: AgentPayload):
    security_result = evaluate_prompt(payload.user_query)
    return {
        "agent": payload.agent_name,
        "query": payload.user_query,
        "security": security_result,
        "timestamp": datetime.now().isoformat()
    }


# -----------------------------
# Judge Demo Endpoint
# -----------------------------
@app.post("/v1/demo", summary="Side-by-side demo for judges")
async def demo(payload: AgentPayload):
    simulator_path = os.path.join(os.path.dirname(__file__), "..", "simulator")
    if simulator_path not in sys.path:
        sys.path.insert(0, simulator_path)
    from agent import run_single_query

    # 1. Without protection — call agent directly
    without_protection = run_single_query(payload.user_query)

    # 2. With protection — check security first
    security_result = evaluate_prompt(payload.user_query)
    is_blocked = security_result["status"] == "BLOCKED"

    if is_blocked:
        with_protection = "[Threat Intercepted] This prompt was blocked by AI-Kavach before reaching the agent."
    else:
        with_protection = run_single_query(payload.user_query)

    # Broadcast to dashboard WebSocket
    ws_payload = {
        "status": security_result["status"],
        "reason": security_result.get("reason"),
        "similarity_score": security_result.get("similarity_score"),
        "confidence": security_result.get("confidence"),
        "id": f"evt_{uuid.uuid4().hex[:6]}",
        "timestamp": datetime.now().isoformat(),
        "ip": "judge-demo",
        "query": payload.user_query,
        "response": with_protection,
        "violatedRule": security_result.get("reason") if is_blocked else "None",
        "riskScore": security_result.get("similarity_score") or "0.0",
    }
    for connection in active_connections:
        try:
            await connection.send_json(ws_payload)
        except Exception:
            pass

    return {
        "query": payload.user_query,
        "blocked": is_blocked,
        "reason": security_result.get("reason") or "None",
        "risk_score": str(security_result.get("similarity_score") or "0.0"),
        "without_protection": without_protection,
        "with_protection": with_protection,
    }


# -----------------------------
# Live WebSocket Endpoint
# -----------------------------
active_connections = []

@app.websocket("/ws/live-stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            user_query = await websocket.receive_text()
            result = evaluate_prompt(user_query)
            is_blocked = result["status"] == "BLOCKED"
            payload = {
                "status": result["status"],
                "reason": result["reason"],
                "similarity_score": result["similarity_score"],
                "confidence": result["confidence"],
                "id": f"evt_{uuid.uuid4().hex[:6]}",
                "timestamp": datetime.now().isoformat(),
                "ip": websocket.client.host,
                "query": user_query,
                "response": "[Threat Intercepted] Blocked by security guardrails." if is_blocked else "Request processed safely.",
                "violatedRule": result["reason"] if is_blocked else "None",
                "riskScore": result["similarity_score"] or "0.0",
            }
            await websocket.send_json(payload)
            for connection in active_connections:
                if connection != websocket:
                    try:
                        await connection.send_json(payload)
                    except Exception:
                        pass
    except Exception:
        pass
    finally:
        if websocket in active_connections:
            active_connections.remove(websocket)