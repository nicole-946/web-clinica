"""Scenarios and demo user router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.scenario import PatientProfile, Scenario
from app.models.user import User
from app.schemas.api import ScenarioResponse, UserResponse

router = APIRouter(tags=["scenarios"])


@router.get("/users/demo", response_model=UserResponse)
async def get_demo_user(db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Demo user not seeded")
    return user


@router.get("/scenarios", response_model=list[ScenarioResponse])
async def list_scenarios(db: AsyncSession = Depends(get_db)) -> list[ScenarioResponse]:
    result = await db.execute(select(Scenario))
    scenarios = result.scalars().all()
    out: list[ScenarioResponse] = []
    for s in scenarios:
        profile = await db.get(PatientProfile, s.profile_id)
        out.append(
            ScenarioResponse(
                id=s.id,
                slug=s.slug,
                name=s.name,
                difficulty=s.difficulty,
                max_duration_minutes=s.max_duration_minutes,
                patient_title=profile.title if profile else None,
            )
        )
    return out
