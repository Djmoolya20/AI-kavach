from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import AgentPayload
from security_core import evaluate_prompt

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Kavach Backend Running"
    }

# Test Route
@app.post("/test")
def test(payload: AgentPayload):
    return {
        "agent": payload.agent_name,
        "query": payload.user_query
    }

# Security Evaluation Route
@app.post("/v1/proxy/evaluate")
def evaluate(payload: AgentPayload):
    return evaluate_prompt(payload.user_query)