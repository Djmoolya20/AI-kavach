from pydantic import BaseModel

class AgentPayload(BaseModel):
    agent_name: str
    user_query: str