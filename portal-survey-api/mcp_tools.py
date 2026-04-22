from datetime import date
from typing import Any

from fastmcp import FastMCP
from pydantic import ValidationError
from sqlmodel import Session

from database import engine
from requests import SurveyCreateRequest, SurveyUpdateRequest
from services import (
    create_survey_record,
    delete_survey_record,
    get_survey_record,
    list_survey_records,
    search_survey_records,
    update_survey_record,
)

mcp = FastMCP("Student Survey MCP Tool Server")


def _error(message: str, details: Any | None = None) -> dict[str, Any]:
    response: dict[str, Any] = {"ok": False, "message": message}
    if details is not None:
        response["details"] = details
    return response


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


@mcp.tool
def create_survey(payload: dict[str, Any]) -> dict[str, Any]:
    """Create one student survey record after the agent has collected all required fields."""
    try:
        request = SurveyCreateRequest.model_validate(payload)
    except ValidationError as exc:
        return _error("Survey payload failed validation.", exc.errors())

    with Session(engine) as session:
        survey = create_survey_record(session, request)
        return {"ok": True, "message": "Survey created successfully.", "survey": survey}


@mcp.tool
def list_surveys() -> dict[str, Any]:
    """Return all student survey records as structured JSON."""
    with Session(engine) as session:
        return {"ok": True, **list_survey_records(session)}


@mcp.tool
def get_survey_by_id(survey_id: int) -> dict[str, Any]:
    """Return one survey by its database ID."""
    with Session(engine) as session:
        survey = get_survey_record(session, survey_id)
        if not survey:
            return _error(f"Survey with id {survey_id} was not found.")
        return {"ok": True, "survey": survey}


@mcp.tool
def search_surveys(
    first_name: str | None = None,
    last_name: str | None = None,
    liked_most: str | None = None,
    interest_source: str | None = None,
    recommendation: str | None = None,
    submitted_from: str | None = None,
    submitted_to: str | None = None,
) -> dict[str, Any]:
    """Search surveys by student name, liked-most criteria, interest source, recommendation, or date range."""
    try:
        from_date = _parse_date(submitted_from)
        to_date = _parse_date(submitted_to)
    except ValueError as exc:
        return _error("Date filters must use YYYY-MM-DD format.", str(exc))

    with Session(engine) as session:
        return {
            "ok": True,
            **search_survey_records(
                session=session,
                first_name=first_name,
                last_name=last_name,
                liked_most=liked_most,
                interest_source=interest_source,
                recommendation=recommendation,
                submitted_from=from_date,
                submitted_to=to_date,
            ),
        }


@mcp.tool
def update_survey(survey_id: int, changes: dict[str, Any]) -> dict[str, Any]:
    """Update selected fields on a survey after the agent has shown a summary and received approval."""
    try:
        request = SurveyUpdateRequest.model_validate(changes)
    except ValidationError as exc:
        return _error("Survey update failed validation.", exc.errors())

    with Session(engine) as session:
        survey = update_survey_record(session, survey_id, request)
        if not survey:
            return _error(f"Survey with id {survey_id} was not found.")
        return {"ok": True, "message": "Survey updated successfully.", "survey": survey}


@mcp.tool
def delete_survey(survey_id: int) -> dict[str, Any]:
    """Delete one survey by ID after the agent has shown the record and received explicit confirmation."""
    with Session(engine) as session:
        deleted = delete_survey_record(session, survey_id)
        if not deleted:
            return _error(f"Survey with id {survey_id} was not found.")
        return {"ok": True, "message": f"Survey {survey_id} deleted successfully."}
