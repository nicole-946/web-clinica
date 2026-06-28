---
name: clinical-sim-architect
description: Applies Senior Architect quality rules when building or modifying the clinical simulation EdTech platform (Next.js, FastAPI, LangGraph, PostgreSQL). Use when scaffolding clinical-sim, writing patient system prompts, evaluation agents, guardrails, API routes, DB schemas, or when the user mentions simulación clínica, pacientes virtuales, or Senior Architect Mode.
---

# Clinical Sim Architect

## Quick Start

Before generating or modifying any code, execute these steps in order:

1. **Impact analysis** — List affected files, dependencies, and backward-compatibility risks (DB schema, patient prompts).
2. **Security and validation** — Define Pydantic schemas; isolate LLM calls in dedicated services.
3. **Clean code** — Use dependency injection, static typing, functions ≤20 lines.
4. **EdTech safety** — Route every virtual-patient response through `output_guard` before display.
5. **Self-correction** — Ask whether a simpler or safer approach exists; revise before presenting.

## Reglas de Calidad y Prevención de Errores (Senior Architect Mode)

Antes de generar o modificar cualquier código, el agente debe seguir estos pasos:

1. **Análisis de Impacto (Chain of Thought):**
   - Antes de escribir, identifica los archivos afectados y posibles efectos secundarios en otras dependencias.
   - Si la sugerencia implica un cambio en el esquema de la DB o en el prompt de un paciente, evalúa si rompe la compatibilidad hacia atrás.

2. **Seguridad y Validación (Anti-Error):**
   - **Nunca** confíes en el input del usuario (frontend). Valida todo con `Pydantic` en el backend (FastAPI).
   - **Principio de Aislamiento:** Cualquier lógica de IA (LLM calls) debe estar aislada en servicios independientes. No mezcles lógica de negocio con llamadas a la API de OpenAI/Anthropic.
   - **Manejo de Errores:** Cada función que interactúe con el LLM debe tener bloques `try-except` robustos y logs claros para depuración.

3. **Criterios de Código Limpio:**
   - Prioriza la inyección de dependencias sobre el uso de globales.
   - Implementa tipado estático (Type Hinting) en todo el código Python.
   - Si una función tiene más de 20 líneas, debe ser refactorizada o modularizada.

4. **Regla de Oro (EdTech/Psychology Safety):**
   - Toda respuesta del 'Paciente Virtual' debe ser verificada antes de mostrarse para asegurar que no rompa el 'System Prompt' (ej: que el paciente no empiece a dar consejos médicos reales).
   - Siempre añade comentarios que expliquen el *porqué* (intención) y no solo el *qué* (implementación).

5. **Self-Correction:**
   - Después de generar el código, el agente debe revisar brevemente: "¿Es esta la forma más eficiente de realizar esta tarea?". Si hay una forma más sencilla o segura, auto-corrígete antes de presentar la respuesta.

## Pre-Code Checklist

```
Pre-Code Checklist:
- [ ] Archivos afectados listados
- [ ] Impacto en DB / system_prompts evaluado
- [ ] LLM logic va en apps/api/ai/ o evaluation/, no en routers
- [ ] Schemas Pydantic definidos antes del handler
```

## Post-Code Review

After generating code, perform a brief mandatory review:

1. Re-read each changed file against the five rules above.
2. Confirm virtual-patient outputs pass through `output_guard`.
3. Ask: "¿Es esta la forma más eficiente de realizar esta tarea?"
4. If a simpler or safer approach exists, revise before presenting the response.

## Anti-Patterns

- LLM calls in routers or React components
- Validation only on the frontend
- Modifying `system_prompts/_base/L0_platform_invariants.yaml` without a legal-review flag
- Monolithic functions exceeding 20 lines
- Virtual-patient responses shown without passing through `output_guard`
- Global singletons for LLM, DB, or Redis clients

## Additional Resources

- For stack, folder layout, LangGraph flow, and DB schema, see [reference.md](reference.md)
