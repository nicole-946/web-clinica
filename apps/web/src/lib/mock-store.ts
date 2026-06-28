/** In-memory mock store for local demo when FastAPI is unavailable. */

export type MockUser = { id: string; email: string; full_name: string; role: string };
export type MockMessage = { id: string; role: string; content: string; created_at: string };

const DISCLAIMER = {
  id: "disc-1",
  version: "2025.1",
  content_md: `# Aviso Legal — Simulación Educativa

Esta plataforma es una **herramienta exclusivamente educativa** para la práctica de entrevistas clínicas simuladas.

**No es atención clínica real.** Los pacientes virtuales son personajes ficticios generados por IA.

- No utilices esta plataforma para auto-diagnóstico ni emergencias de salud mental.
- Los escenarios no sustituyen supervisión clínica profesional.

Al continuar, confirmas que comprendes que se trata de una simulación con fines formativos.`,
};

const DEMO_USER: MockUser = {
  id: "user-demo-1",
  email: "estudiante@demo.edu",
  full_name: "Estudiante Demo",
  role: "student",
};

const SCENARIOS = [
  {
    id: "sc-1",
    slug: "maria-intake",
    name: "Entrevista inicial con María",
    difficulty: "intermediate",
    max_duration_minutes: 30,
    patient_title: "María — Episodio depresivo simulado",
  },
];

const MOCK_RESPONSES = [
  "Hola... gracias por recibirme. No sé muy bien por dónde empezar.",
  "Últimamente duermo mal. Me cuesta mucho conciliar el sueño.",
  "Siento que nada me ilusiona como antes. Todo me da igual.",
  "A veces pienso que es culpa mía, que debería poder salir de esto sola.",
  "No quiero preocupar a mi familia... por eso no les he contado cómo me siento.",
];

const acceptances = new Set<string>();
const sessions = new Map<string, { state: { trust_level: number; turn_count: number; case_id?: string }; messages: MockMessage[] }>();
const feedback = new Map<string, Record<string, unknown>>();

const MOCK_CASES = [
  { id: "maria-depression", patologia: "Episodio Depresivo Mayor" },
  { id: "pedro-anxiety", patologia: "Trastorno de Ansiedad Generalizada" },
  { id: "lucia-borderline", patologia: "Trastorno Límite de la Personalidad" }
];

let turnCounter = 0;

export const mockStore = {
  getDemoUser: () => DEMO_USER,
  getDisclaimer: () => DISCLAIMER,
  isAccepted: (userId: string) => acceptances.has(userId),
  accept: (userId: string) => {
    acceptances.add(userId);
  },
  listScenarios: () => SCENARIOS,
  getCases: () => MOCK_CASES,
  createSession: () => {
    const id = `sess-${Date.now()}`;
    sessions.set(id, { state: { trust_level: 0, turn_count: 0 }, messages: [] });
    return { id, scenario_id: "sc-1", status: "active", session_state: {}, started_at: new Date().toISOString() };
  },
  startSession: (userId: string, caseId: string) => {
    let selectedId = caseId;
    if (caseId === "random") {
      const ids = ["maria-depression", "pedro-anxiety", "lucia-borderline"];
      selectedId = ids[Math.floor(Math.random() * ids.length)];
    }
    const id = `sess-${Date.now()}`;
    let initialMsg = "Hola... gracias por recibirme. Siento que todo me da igual y no tengo fuerzas para nada...";
    if (selectedId === "pedro-anxiety") {
      initialMsg = "Hola, buenas... la verdad es que he estado con mucha agitación en el pecho y me cuesta estar tranquilo.";
    } else if (selectedId === "lucia-borderline") {
      initialMsg = "Hola. Vengo porque me obligaron... realmente no sé si esto sirva para algo, todo el mundo me termina abandonando...";
    }
    
    const messages = [{
      id: `m-p-${++turnCounter}`,
      role: "patient",
      content: initialMsg,
      created_at: new Date().toISOString(),
    }];

    sessions.set(id, { state: { trust_level: 0, turn_count: 1, case_id: selectedId }, messages });
    return { session_id: id, case_id: selectedId, patient_initial_message: initialMsg };
  },
  getMessages: (id: string) => sessions.get(id)?.messages ?? [],
  sendMessage: (id: string, content: string) => {
    const session = sessions.get(id);
    if (!session) throw new Error("Session not found");
    session.messages.push({
      id: `m-s-${++turnCounter}`,
      role: "student",
      content,
      created_at: new Date().toISOString(),
    });
    const turn = session.state.turn_count ?? 0;
    session.state.turn_count = turn + 1;
    let reply = MOCK_RESPONSES[Math.min(turn, MOCK_RESPONSES.length - 1)];
    if (/cómo te sientes|cómo estás/i.test(content)) reply = MOCK_RESPONSES[1];
    if (/entiendo|debe ser difícil/i.test(content)) reply = MOCK_RESPONSES[4];
    session.messages.push({
      id: `m-p-${++turnCounter}`,
      role: "patient",
      content: reply,
      created_at: new Date().toISOString(),
    });
    return { role: "patient", content: reply };
  },
  completeSession: (id: string) => {
    const session = sessions.get(id);
    const caseId = session?.state?.case_id;
    const studentMsgs = (session?.messages ?? []).filter((m) => m.role === "student");
    const openQ = studentMsgs.filter((m) => m.content.includes("?")).length;
    const validation = studentMsgs.filter((m) => /entiendo|difícil|gracias/i.test(m.content)).length;
    
    let apaRef = "Asociación Americana de Psiquiatría. (2014). *Manual diagnóstico y estadístico de los trastornos mentales* (5ª ed.; DSM-5). Editorial Médica Panamericana.";
    if (caseId === "pedro-anxiety") {
      apaRef += "\n\nBeck, A. T., Emery, G., & Greenberg, R. L. (2005). *Anxiety disorders and phobias: A cognitive perspective*. Basic Books.";
    } else if (caseId === "lucia-borderline") {
      apaRef += "\n\nLinehan, M. M. (1993). *Cognitive-behavioral treatment of borderline personality disorder*. Guilford Press.";
    } else {
      apaRef += "\n\nBeck, A. T., Rush, A. J., Shaw, B. F., & Emery, G. (1979). *Cognitive therapy of depression*. Guilford Press.";
    }

    const report = {
      session_id: id,
      rubric_version: "1.0",
      scores: {
        active_listening: validation >= 2 ? 4 : validation >= 1 ? 3 : 2,
        validation: validation >= 2 ? 4 : 2,
        question_quality: openQ >= 2 ? 4 : openQ >= 1 ? 3 : 2,
      },
      narrative: `## Retroalimentación pedagógica\n\nEvaluación formativa basada en técnicas de entrevista simulada.\n\n- Preguntas abiertas: ${openQ}\n- Validaciones detectadas: ${validation}\n\n**Sugerencia:** Practica parafrasear lo emocional antes de la siguiente pregunta.\n\n### Lecturas recomendadas (Referencias APA 7ma edición):\n\n${apaRef}`,
      highlights: studentMsgs.slice(0, 3).map((m) => ({ role: "student", quote: m.content.slice(0, 200) })),
    };
    feedback.set(id, report);
    return report;
  },
  getFeedback: (id: string) => feedback.get(id) ?? null,
};
