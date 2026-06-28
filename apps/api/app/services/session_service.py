"""Session business logic."""

from datetime import datetime, timezone
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.graphs.interview_graph import InterviewGraph
from app.ai.llm.patient_service import PatientLLMService
from app.ai.memory.state_helpers import initial_state
from app.ai.prompts.loader import load_persona
from app.config import Settings
from app.db.cases import CLINICAL_CASES
from app.models.scenario import Scenario
from app.models.session import FeedbackReport, SessionMessage, TrainingSession
from app.services.feedback_service import FeedbackEvaluator


class SessionService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._graph = InterviewGraph(settings, PatientLLMService(settings))
        self._evaluator = FeedbackEvaluator(settings)

    async def create_session(
        self, db: AsyncSession, user_id: str, scenario_slug: str
    ) -> TrainingSession:
        scenario = await self._get_scenario(db, scenario_slug)
        session = TrainingSession(
            user_id=user_id,
            scenario_id=scenario.id,
            session_state=initial_state(),
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    async def process_message(
        self, db: AsyncSession, session_id: str, content: str
    ) -> tuple[SessionMessage, SessionMessage | None]:
        session = await self._get_session(db, session_id)
        scenario = await db.get(Scenario, session.scenario_id)
        if not scenario:
            raise ValueError("Scenario not found")
        persona = load_persona(self._settings, scenario.persona_path)
        student_msg = SessionMessage(session_id=session_id, role="student", content=content)
        db.add(student_msg)
        result = await self._graph.run_turn(persona, session.session_state, content)
        session.session_state = result["session_state"]
        patient_msg = SessionMessage(
            session_id=session_id,
            role="patient",
            content=result["patient_content"],
            metadata_=result.get("patient_metadata"),
        )
        db.add(patient_msg)
        await db.commit()
        await db.refresh(student_msg)
        await db.refresh(patient_msg)
        return student_msg, patient_msg

    async def complete_session(self, db: AsyncSession, session_id: str) -> FeedbackReport:
        existing = await self.get_feedback(db, session_id)
        if existing:
            return existing
        session = await self._get_session(db, session_id)
        session.status = "completed"
        session.ended_at = datetime.now(timezone.utc)
        messages = await self._get_messages(db, session_id)
        payload = [{"role": m.role, "content": m.content} for m in messages]
        evaluation = self._evaluator.evaluate(payload, session.session_state.get("case_id"))
        report = FeedbackReport(
            session_id=session_id,
            rubric_version=evaluation["rubric_version"],
            scores=evaluation["scores"],
            narrative=evaluation["narrative"],
            highlights=evaluation.get("highlights"),
        )
        db.add(report)
        await db.commit()
        await db.refresh(report)
        return report

    async def get_feedback(self, db: AsyncSession, session_id: str) -> FeedbackReport | None:
        result = await db.execute(
            select(FeedbackReport).where(FeedbackReport.session_id == session_id)
        )
        return result.scalar_one_or_none()

    async def list_messages(self, db: AsyncSession, session_id: str) -> list[SessionMessage]:
        return await self._get_messages(db, session_id)

    async def _get_scenario(self, db: AsyncSession, slug: str) -> Scenario:
        result = await db.execute(select(Scenario).where(Scenario.slug == slug))
        scenario = result.scalar_one_or_none()
        if not scenario:
            raise ValueError(f"Scenario not found: {slug}")
        return scenario

    async def _get_session(self, db: AsyncSession, session_id: str) -> TrainingSession:
        session = await db.get(TrainingSession, session_id)
        if not session:
            raise ValueError("Session not found")
        return session

    async def _get_messages(self, db: AsyncSession, session_id: str) -> list[SessionMessage]:
        result = await db.execute(
            select(SessionMessage)
            .where(SessionMessage.session_id == session_id)
            .order_by(SessionMessage.created_at)
        )
        return list(result.scalars().all())

    async def start_session_by_case(
        self, db: AsyncSession, user_id: str, case_id: str
    ) -> tuple[TrainingSession, SessionMessage, str]:
        actual_case_id = case_id
        if case_id == "random":
            actual_case_id = random.choice(list(CLINICAL_CASES.keys()))

        if actual_case_id not in CLINICAL_CASES:
            raise ValueError(f"Case ID not found: {actual_case_id}")

        case = CLINICAL_CASES[actual_case_id]
        scenario = await self._get_scenario(db, actual_case_id)

        system_prompt = (
            f"Eres {case['nombre_paciente']}, un paciente virtual de {case['edad']} años. "
            f"Tu patología subyacente (que no debes nombrar directamente) es: {case['patologia']}. "
            f"Contexto clínico: {case['contexto']}. "
            f"Nivel de resistencia a la terapia: {case['nivel_resistencia']}/10. "
            "Asegúrate de responder en personaje de manera realista y segura para la simulación educativa."
        )

        state = {
            "trust_level": 0.0,
            "turn_count": 0,
            "topics_disclosed": [],
            "system_prompt": system_prompt,
            "case_id": actual_case_id,
            "nombre_paciente": case["nombre_paciente"],
            "patologia": case["patologia"],
        }

        session = TrainingSession(
            user_id=user_id,
            scenario_id=scenario.id,
            session_state=state,
        )
        db.add(session)
        await db.flush()

        initial_msg = SessionMessage(
            session_id=session.id,
            role="patient",
            content=case["initial_message"],
            metadata_={"initial_message": True},
        )
        db.add(initial_msg)
        await db.commit()
        await db.refresh(session)
        await db.refresh(initial_msg)

        return session, initial_msg, actual_case_id

