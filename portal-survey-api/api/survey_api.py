from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from requests import SurveyCreateRequest, SurveyUpdateRequest
from responses import MessageResponse, SurveyListResponse, SurveyResponse
from services import (
    create_survey_record,
    delete_survey_record,
    get_survey_record,
    list_survey_records,
    update_survey_record,
)

router = APIRouter(prefix="/api/surveys", tags=["Surveys"])


@router.post(
    "",
    response_model=SurveyResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new survey",
)
def create_survey(
    payload: SurveyCreateRequest,
    session: Session = Depends(get_session),
) -> SurveyResponse:
    return SurveyResponse(**create_survey_record(session, payload))


@router.get(
    "",
    response_model=SurveyListResponse,
    summary="Get all surveys",
)
def list_surveys(session: Session = Depends(get_session)) -> SurveyListResponse:
    return SurveyListResponse(**list_survey_records(session))


@router.get(
    "/{survey_id}",
    response_model=SurveyResponse,
    summary="Get a survey by ID",
)
def get_survey(
    survey_id: int,
    session: Session = Depends(get_session),
) -> SurveyResponse:
    survey = get_survey_record(session, survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found.",
        )
    return SurveyResponse(**survey)


@router.put(
    "/{survey_id}",
    response_model=SurveyResponse,
    summary="Update a survey",
)
def update_survey(
    survey_id: int,
    payload: SurveyUpdateRequest,
    session: Session = Depends(get_session),
) -> SurveyResponse:
    survey = update_survey_record(session, survey_id, payload)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found.",
        )
    return SurveyResponse(**survey)


@router.delete(
    "/{survey_id}",
    response_model=MessageResponse,
    summary="Delete a survey",
)
def delete_survey(
    survey_id: int,
    session: Session = Depends(get_session),
) -> MessageResponse:
    deleted = delete_survey_record(session, survey_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Survey with id {survey_id} not found.",
        )
    return MessageResponse(message=f"Survey {survey_id} deleted successfully.")
