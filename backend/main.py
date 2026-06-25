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
@app.websocket("/ws/live-stream")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:

            user_query = await websocket.receive_text()

            result = evaluate_prompt(user_query)

            await websocket.send_json(result)

    except Exception:
        await websocket.close()