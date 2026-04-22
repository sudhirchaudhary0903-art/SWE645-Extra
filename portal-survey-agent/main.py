from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from graph import SurveyAgent
from models import AgentRequest, AgentResponse, new_session_id

app = FastAPI(
    title="Student Survey LangGraph Agent",
    description="Agentic AI workflow service for natural-language survey CRUD operations.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = SurveyAgent()
sessions: dict[str, dict] = {}


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/agent/query", response_model=AgentResponse, tags=["Agent"])
async def query_agent(payload: AgentRequest) -> AgentResponse:
    session_id = payload.session_id or new_session_id()
    session = sessions.setdefault(session_id, {})
    result = await agent.run(payload.message, session)

    if result.get("session"):
        sessions[session_id] = result["session"]
    else:
        sessions.pop(session_id, None)

    return AgentResponse(
        session_id=session_id,
        response=result.get("response", "I could not produce a response."),
        intent=result.get("intent", "unknown"),
        requires_confirmation=result.get("requires_confirmation", False),
        pending_action=result.get("pending_action"),
        data={
            "tool_name": result.get("tool_name"),
            "tool_args": result.get("tool_args"),
            "tool_output": result.get("tool_output"),
        },
    )
