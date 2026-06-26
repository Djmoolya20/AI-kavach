import uuid
from datetime import datetime
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from schemas import AgentPayload
from security_core import evaluate_prompt
from datetime import datetime

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
                # For simulator (proxy_client.py)
                "status": result["status"],
                "reason": result["reason"],
                "similarity_score": result["similarity_score"],
                "confidence": result["confidence"],
                # For frontend dashboard
                "id": f"evt_{uuid.uuid4().hex[:6]}",
                "timestamp": datetime.now().isoformat(),
                "ip": websocket.client.host,
                "query": user_query,
                "response": "[Threat Intercepted] Blocked by security guardrails." if is_blocked else "Request processed safely.",
                "violatedRule": result["reason"] if is_blocked else "None",
                "riskScore": result["similarity_score"] or "0.0",
            }
            # Send result back to simulator
            await websocket.send_json(payload)
            # Broadcast to all other connected clients (frontend)
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