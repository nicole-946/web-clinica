const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK_API === "true";
const API_URL = USE_MOCK ? "" : (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000");

async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const base = USE_MOCK ? "/api" : API_URL;
  const res = await fetch(`${base}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(err || res.statusText);
  }
  return res.json() as Promise<T>;
}

export type User = { id: string; email: string; full_name: string; role: string };
export type Disclaimer = { id: string; version: string; content_md: string };
export type DisclaimerStatus = { accepted: boolean; version: string | null };
export type Scenario = {
  id: string;
  slug: string;
  name: string;
  difficulty: string;
  max_duration_minutes: number;
  patient_title: string | null;
};
export type Session = {
  id: string;
  scenario_id: string;
  status: string;
  session_state: Record<string, unknown>;
  started_at: string;
};
export type ChatMessage = { role: string; content: string; metadata?: Record<string, unknown> };
export type MessageHistory = { id: string; role: string; content: string; created_at: string };
export type Feedback = {
  session_id: string;
  rubric_version: string;
  scores: Record<string, number>;
  narrative: string;
  highlights: { role: string; quote: string }[] | null;
};
export type Case = { id: string; patologia: string };
export type SessionStartResponse = { session_id: string; case_id: string; patient_initial_message: string };

export const apiClient = {
  getDemoUser: () => api<User>("/users/demo"),
  getActiveDisclaimer: () => api<Disclaimer>("/disclaimer/active"),
  getDisclaimerStatus: (userId: string) =>
    api<DisclaimerStatus>(`/disclaimer/status/${userId}`),
  acceptDisclaimer: (userId: string) =>
    api<DisclaimerStatus>("/disclaimer/accept", {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }),
  listScenarios: () => api<Scenario[]>("/scenarios"),
  createSession: (userId: string, scenarioSlug: string) =>
    api<Session>("/sessions", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, scenario_slug: scenarioSlug }),
    }),
  getMessages: (sessionId: string) =>
    api<MessageHistory[]>(`/sessions/${sessionId}/messages`),
  sendMessage: (sessionId: string, content: string) =>
    api<ChatMessage>(`/sessions/${sessionId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }),
  completeSession: (sessionId: string) =>
    api<Feedback>(`/sessions/${sessionId}/complete`, { method: "POST" }),
  getFeedback: (sessionId: string) => api<Feedback>(`/sessions/${sessionId}/feedback`),
  getCases: () => api<Case[]>("/cases"),
  startSession: (userId: string, caseId: string) =>
    api<SessionStartResponse>("/sessions/start", {
      method: "POST",
      body: JSON.stringify({ user_id: userId, case_id: caseId }),
    }),
};
