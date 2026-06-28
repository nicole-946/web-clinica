"""Cases and start session router."""

import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.dependencies import get_session_service
from app.schemas.api import CaseResponse, SessionStartRequest, SessionStartResponse
from app.services.session_service import SessionService
from app.db.cases import CLINICAL_CASES

router = APIRouter(tags=["cases"])


@router.get("/cases", response_model=list[CaseResponse])
async def list_cases() -> list[CaseResponse]:
    try:
        return [
            CaseResponse(id=case_id, patologia=case["patologia"])
            for case_id, case in CLINICAL_CASES.items()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing cases: {str(e)}") from e


@router.post("/sessions/start", response_model=SessionStartResponse)
async def start_session(
    body: SessionStartRequest,
    db: AsyncSession = Depends(get_db),
    service: SessionService = Depends(get_session_service),
) -> SessionStartResponse:
    try:
        session, initial_msg, case_id = await service.start_session_by_case(
            db, body.user_id, body.case_id
        )
        return SessionStartResponse(
            session_id=session.id,
            case_id=case_id,
            patient_initial_message=initial_msg.content,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting session: {str(e)}") from e
