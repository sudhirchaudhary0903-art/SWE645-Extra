from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


class AgentResponse(BaseModel):
    session_id: str
    response: str
    intent: str
    requires_confirmation: bool = False
    pending_action: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)


class SurveyDraft(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    street_address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    telephone: str | None = None
    email: str | None = None
    date_of_survey: str | None = None
    liked_most: list[str] = Field(default_factory=list)
    interest_source: str | None = None
    recommendation: str | None = None
    raffle: str | None = None
    comments: str | None = None

    def as_payload(self) -> dict[str, Any]:
        return self.model_dump(exclude_none=True)


def new_session_id() -> str:
    return str(uuid4())
