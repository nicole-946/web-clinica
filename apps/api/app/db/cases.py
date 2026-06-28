"""Clinical cases catalog for simulation sessions."""

from typing import Any, TypedDict


class CaseProfile(TypedDict):
    id: str
    nombre_paciente: str
    edad: int
    patologia: str
    contexto: str
    nivel_resistencia: int
    initial_message: str
    persona_path: str


CLINICAL_CASES: dict[str, CaseProfile] = {
    "maria-depression": {
        "id": "maria-depression",
        "nombre_paciente": "María",
        "edad": 28,
        "patologia": "Episodio Depresivo Mayor",
        "contexto": "Empleada administrativa, vive sola, presenta desinterés generalizado y cansancio persistente.",
        "nivel_resistencia": 6,
        "initial_message": "Hola... gracias por recibirme. Siento que todo me da igual y no tengo fuerzas para nada...",
        "persona_path": "clinical/maria_depression_v1/persona.yaml",
    },
    "pedro-anxiety": {
        "id": "pedro-anxiety",
        "nombre_paciente": "Pedro",
        "edad": 34,
        "patologia": "Trastorno de Ansiedad Generalizada",
        "contexto": "Ingeniero de software, sufre de insomnio, taquicardia constante e inquietud persistente por el futuro.",
        "nivel_resistencia": 4,
        "initial_message": "Hola, buenas... la verdad es que he estado con mucha agitación en el pecho y me cuesta estar tranquilo.",
        "persona_path": "clinical/pedro_anxiety_v1/persona.yaml",
    },
    "lucia-borderline": {
        "id": "lucia-borderline",
        "nombre_paciente": "Lucía",
        "edad": 23,
        "patologia": "Trastorno Límite de la Personalidad",
        "contexto": "Estudiante universitaria, experimenta relaciones interpersonales inestables e hipersensibilidad al rechazo.",
        "nivel_resistencia": 8,
        "initial_message": "Hola. Vengo porque me obligaron... realmente no sé si esto sirva para algo, todo el mundo me termina abandonando...",
        "persona_path": "clinical/lucia_borderline_v1/persona.yaml",
    },
}
