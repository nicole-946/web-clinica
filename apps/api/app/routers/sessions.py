"""Training session and chat router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_session_service
from app.schemas.api import (
    ChatMessageRequest,
    ChatMessageResponse,
    FeedbackResponse,
    MessageHistoryItem,
    SessionCreateRequest,
    SessionResponse,
)
from app.services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionResponse)
async def create_session(
    body: SessionCreateRequest,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> SessionResponse:
    try:
        session = await service.create_session(db, body.user_id, body.scenario_slug)
        return SessionResponse.model_validate(session)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/{session_id}/messages", response_model=list[MessageHistoryItem])
async def get_messages(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> list[MessageHistoryItem]:
    messages = await service.list_messages(db, session_id)
    return [MessageHistoryItem.model_validate(m) for m in messages]


@router.post("/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    body: ChatMessageRequest,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> ChatMessageResponse:
    try:
        _, patient = await service.process_message(db, session_id, body.content)
        if not patient:
            raise HTTPException(status_code=500, detail="No patient response")
        return ChatMessageResponse(
            role=patient.role,
            content=patient.content,
            metadata=patient.metadata_,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/{session_id}/feedback", response_model=FeedbackResponse)
async def get_feedback(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> FeedbackResponse:
    report = await service.get_feedback(db, session_id)
    if not report:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return FeedbackResponse(
        session_id=report.session_id,
        rubric_version=report.rubric_version,
        scores=report.scores,
        narrative=report.narrative,
        highlights=report.highlights,
    )


@router.post("/{session_id}/complete", response_model=FeedbackResponse)
async def complete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> FeedbackResponse:
    try:
        report = await service.complete_session(db, session_id)
        return FeedbackResponse(
            session_id=report.session_id,
            rubric_version=report.rubric_version,
            scores=report.scores,
            narrative=report.narrative,
            highlights=report.highlights,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
