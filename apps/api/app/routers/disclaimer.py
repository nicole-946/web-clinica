"""Disclaimer router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.disclaimer import DisclaimerAcceptance, DisclaimerVersion
from app.schemas.api import (
    DisclaimerAcceptRequest,
    DisclaimerResponse,
    DisclaimerStatusResponse,
)

router = APIRouter(prefix="/disclaimer", tags=["disclaimer"])


@router.get("/active", response_model=DisclaimerResponse)
async def get_active_disclaimer(db: AsyncSession = Depends(get_db)) -> DisclaimerVersion:
    result = await db.execute(
        select(DisclaimerVersion).where(DisclaimerVersion.active.is_(True)).limit(1)
    )
    disclaimer = result.scalar_one_or_none()
    if not disclaimer:
        raise HTTPException(status_code=404, detail="No active disclaimer")
    return disclaimer


@router.get("/status/{user_id}", response_model=DisclaimerStatusResponse)
async def disclaimer_status(user_id: str, db: AsyncSession = Depends(get_db)) -> DisclaimerStatusResponse:
    active = await db.execute(
        select(DisclaimerVersion).where(DisclaimerVersion.active.is_(True)).limit(1)
    )
    version = active.scalar_one_or_none()
    if not version:
        return DisclaimerStatusResponse(accepted=False)
    result = await db.execute(
        select(DisclaimerAcceptance).where(
            DisclaimerAcceptance.user_id == user_id,
            DisclaimerAcceptance.disclaimer_version_id == version.id,
        )
    )
    accepted = result.scalar_one_or_none() is not None
    return DisclaimerStatusResponse(accepted=accepted, version=version.version if accepted else version.version)


@router.post("/accept", response_model=DisclaimerStatusResponse)
async def accept_disclaimer(
    body: DisclaimerAcceptRequest, db: AsyncSession = Depends(get_db)
) -> DisclaimerStatusResponse:
    result = await db.execute(
        select(DisclaimerVersion).where(DisclaimerVersion.active.is_(True)).limit(1)
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(status_code=404, detail="No active disclaimer")
    acceptance = DisclaimerAcceptance(user_id=body.user_id, disclaimer_version_id=version.id)
    db.add(acceptance)
    await db.commit()
    return DisclaimerStatusResponse(accepted=True, version=version.version)
