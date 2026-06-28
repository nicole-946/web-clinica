"""Database initialization and seed data."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.models.disclaimer import DisclaimerVersion
from app.models.scenario import PatientProfile, Scenario
from app.models.user import User
from app.db.session import engine


DISCLAIMER_MD = """# Aviso Legal — Simulación Educativa

Esta plataforma es una **herramienta exclusivamente educativa** para la práctica de entrevistas clínicas simuladas.

**No es atención clínica real.** Los pacientes virtuales son personajes ficticios generados por IA.

- No utilices esta plataforma para auto-diagnóstico ni emergencias de salud mental.
- Los escenarios no sustituyen supervisión clínica profesional.
- En caso de crisis real, contacta servicios de emergencia locales.

Al continuar, confirmas que comprendes que se trata de una simulación con fines formativos.
"""


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_if_empty(session: AsyncSession) -> None:
    if (await session.execute(select(User))).first():
        return
    user = User(email="estudiante@demo.edu", full_name="Estudiante Demo")
    session.add(user)
    disclaimer = DisclaimerVersion(version="2025.1", content_md=DISCLAIMER_MD, active=True)
    session.add(disclaimer)
    profile_maria = PatientProfile(
        slug="maria_depression_v1",
        title="María — Episodio depresivo simulado",
        specialty="clinical",
    )
    profile_pedro = PatientProfile(
        slug="pedro_anxiety_v1",
        title="Pedro — Ansiedad generalizada simulada",
        specialty="clinical",
    )
    profile_lucia = PatientProfile(
        slug="lucia_borderline_v1",
        title="Lucía — Trastorno límite de la personalidad simulado",
        specialty="clinical",
    )
    session.add_all([profile_maria, profile_pedro, profile_lucia])
    await session.flush()

    scenario_maria = Scenario(
        profile_id=profile_maria.id,
        slug="maria-depression",
        name="Entrevista inicial con María",
        persona_path="clinical/maria_depression_v1/persona.yaml",
        difficulty="intermediate",
    )
    scenario_pedro = Scenario(
        profile_id=profile_pedro.id,
        slug="pedro-anxiety",
        name="Entrevista inicial con Pedro",
        persona_path="clinical/pedro_anxiety_v1/persona.yaml",
        difficulty="intermediate",
    )
    scenario_lucia = Scenario(
        profile_id=profile_lucia.id,
        slug="lucia-borderline",
        name="Entrevista inicial con Lucía",
        persona_path="clinical/lucia_borderline_v1/persona.yaml",
        difficulty="advanced",
    )
    session.add_all([scenario_maria, scenario_pedro, scenario_lucia])
    await session.commit()
