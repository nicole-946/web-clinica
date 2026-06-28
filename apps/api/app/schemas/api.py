"""Pydantic schemas for API I/O."""

from datetime import datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str

    model_config = {"from_attributes": True}


class DisclaimerResponse(BaseModel):
    id: str
    version: str
    content_md: str


class DisclaimerAcceptRequest(BaseModel):
    user_id: str = Field(min_length=1)


class DisclaimerStatusResponse(BaseModel):
    accepted: bool
    version: str | None = None


class ScenarioResponse(BaseModel):
    id: str
    slug: str
    name: str
    difficulty: str
    max_duration_minutes: int
    patient_title: str | None = None

    model_config = {"from_attributes": True}


class SessionCreateRequest(BaseModel):
    user_id: str = Field(min_length=1)
    scenario_slug: str = Field(min_length=1)


class SessionResponse(BaseModel):
    id: str
    scenario_id: str
    status: str
    session_state: dict
    started_at: datetime

    model_config = {"from_attributes": True}


class ChatMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    metadata: dict | None = None


class MessageHistoryItem(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FeedbackResponse(BaseModel):
    session_id: str
    rubric_version: str
    scores: dict
    narrative: str
    highlights: list | None

    model_config = {"from_attributes": True}


class CaseResponse(BaseModel):
    id: str
    patologia: str


class SessionStartRequest(BaseModel):
    user_id: str = Field(min_length=1)
    case_id: str = Field(min_length=1)


class SessionStartResponse(BaseModel):
    session_id: str
    case_id: str
    patient_initial_message: str

