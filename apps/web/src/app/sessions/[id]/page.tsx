"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { apiClient, type MessageHistory } from "@/lib/api-client";
import { cn } from "@/lib/utils";

export default function SessionChatPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [messages, setMessages] = useState<MessageHistory[]>([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [completing, setCompleting] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!id) return;
    apiClient.getMessages(id).then(setMessages).catch(() => {});
  }, [id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || !id) return;
    setSending(true);
    const studentText = input.trim();
    setInput("");
    try {
      const patient = await apiClient.sendMessage(id, studentText);
      setMessages((prev) => [
        ...prev,
        {
          id: `local-s-${Date.now()}`,
          role: "student",
          content: studentText,
          created_at: new Date().toISOString(),
        },
        {
          id: `local-p-${Date.now()}`,
          role: patient.role,
          content: patient.content,
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setSending(false);
    }
  }

  async function handleComplete() {
    if (!id) return;
    setCompleting(true);
    try {
      await apiClient.completeSession(id);
      router.push(`/sessions/${id}/feedback`);
    } finally {
      setCompleting(false);
    }
  }

  return (
    <div className="mx-auto flex h-[calc(100vh-40px)] max-w-3xl flex-col px-4 py-4">
      <div className="flex items-center justify-between border-b border-border pb-3">
        <h1 className="text-lg font-semibold">Entrevista en curso</h1>
        <button
          onClick={handleComplete}
          disabled={completing || messages.length === 0}
          className="rounded-md border border-border px-3 py-1.5 text-sm hover:bg-muted disabled:opacity-50"
        >
          {completing ? "Generando feedback..." : "Finalizar sesión"}
        </button>
      </div>
      <div className="flex-1 overflow-y-auto py-4 space-y-3">
        {messages.length === 0 && (
          <p className="text-center text-slate-500 text-sm">
            Comienza la entrevista. El paciente virtual espera tu primer mensaje.
          </p>
        )}
        {messages.map((m) => (
          <div
            key={m.id}
            className={cn(
              "max-w-[85%] rounded-lg px-4 py-2 text-sm",
              m.role === "student"
                ? "ml-auto bg-primary text-primary-foreground"
                : "mr-auto bg-white border border-border"
            )}
          >
            <span className="text-xs opacity-70 block mb-1">
              {m.role === "student" ? "Tú" : "Paciente"}
            </span>
            {m.content}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <form onSubmit={handleSend} className="flex gap-2 border-t border-border pt-3">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Escribe tu intervención clínica..."
          className="flex-1 rounded-lg border border-border px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          disabled={sending}
        />
        <button
          type="submit"
          disabled={sending || !input.trim()}
          className="rounded-lg bg-primary px-4 py-2 text-sm text-primary-foreground disabled:opacity-50"
        >
          Enviar
        </button>
      </form>
      <Link href="/scenarios" className="mt-2 text-xs text-slate-400 hover:underline">
        Volver a escenarios
      </Link>
    </div>
  );
}
