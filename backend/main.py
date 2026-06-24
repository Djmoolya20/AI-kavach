from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import AgentPayload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Kavach Backend Running"
    }

@app.post("/test")
def test(payload: AgentPayload):
    return {
        "agent": payload.agent_name,
        "query": payload.user_query
    }

@app.post("/v1/proxy/evaluate")
def evaluate(payload: AgentPayload):

    if "password" in payload.user_query.lower():
        return {
            "status": "BLOCKED",
            "reason": "Sensitive information request detected"
        }

    return {
        "status": "SAFE",
        "reason": "No threat detected"
    }