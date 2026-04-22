from datetime import date
from typing import Any

from sqlmodel import Session, select

from models import Survey
from requests import SurveyCreateRequest, SurveyUpdateRequest


def survey_to_dict(survey: Survey) -> dict[str, Any]:
    liked_most = []
    if survey.liked_most:
        liked_most = [item.strip() for item in survey.liked_most.split(",") if item.strip()]

    return {
        "id": survey.id,
        "first_name": survey.first_name,
        "last_name": survey.last_name,
        "street_address": survey.street_address,
        "city": survey.city,
        "state": survey.state,
        "zip_code": survey.zip_code,
        "telephone": survey.telephone,
        "email": survey.email,
        "date_of_survey": survey.date_of_survey.isoformat()
        if isinstance(survey.date_of_survey, date)
        else survey.date_of_survey,
        "liked_most": liked_most,
        "interest_source": survey.interest_source,
        "recommendation": survey.recommendation,
        "raffle": survey.raffle,
        "comments": survey.comments,
    }


def create_survey_record(session: Session, payload: SurveyCreateRequest) -> dict[str, Any]:
    survey = Survey(
        **payload.model_dump(exclude={"liked_most"}),
        liked_most=",".join(payload.liked_most),
    )
    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey_to_dict(survey)


def list_survey_records(session: Session) -> dict[str, Any]:
    surveys = session.exec(select(Survey).order_by(Survey.id.desc())).all()
    return {
        "total": len(surveys),
        "surveys": [survey_to_dict(survey) for survey in surveys],
    }


def get_survey_record(session: Session, survey_id: int) -> dict[str, Any] | None:
    survey = session.get(Survey, survey_id)
    if not survey:
        return None
    return survey_to_dict(survey)


def search_survey_records(
    session: Session,
    first_name: str | None = None,
    last_name: str | None = None,
    liked_most: str | None = None,
    interest_source: str | None = None,
    recommendation: str | None = None,
    submitted_from: date | None = None,
    submitted_to: date | None = None,
) -> dict[str, Any]:
    statement = select(Survey)

    if first_name:
        statement = statement.where(Survey.first_name.ilike(f"%{first_name}%"))
    if last_name:
        statement = statement.where(Survey.last_name.ilike(f"%{last_name}%"))
    if liked_most:
        statement = statement.where(Survey.liked_most.ilike(f"%{liked_most}%"))
    if interest_source:
        statement = statement.where(Survey.interest_source == interest_source)
    if recommendation:
        statement = statement.where(Survey.recommendation == recommendation)
    if submitted_from:
        statement = statement.where(Survey.date_of_survey >= submitted_from)
    if submitted_to:
        statement = statement.where(Survey.date_of_survey <= submitted_to)

    surveys = session.exec(statement.order_by(Survey.date_of_survey.desc())).all()
    return {
        "total": len(surveys),
        "surveys": [survey_to_dict(survey) for survey in surveys],
    }


def update_survey_record(
    session: Session,
    survey_id: int,
    payload: SurveyUpdateRequest,
) -> dict[str, Any] | None:
    survey = session.get(Survey, survey_id)
    if not survey:
        return None

    update_data = payload.model_dump(exclude_none=True)
    if "liked_most" in update_data:
        update_data["liked_most"] = ",".join(update_data["liked_most"])

    for field, value in update_data.items():
        setattr(survey, field, value)

    session.add(survey)
    session.commit()
    session.refresh(survey)
    return survey_to_dict(survey)


def delete_survey_record(session: Session, survey_id: int) -> bool:
    survey = session.get(Survey, survey_id)
    if not survey:
        return False
    session.delete(survey)
    session.commit()
    return True
