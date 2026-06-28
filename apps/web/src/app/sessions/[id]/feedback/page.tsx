"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { apiClient, type Feedback } from "@/lib/api-client";

export default function FeedbackPage() {
  const { id } = useParams<{ id: string }>();
  const [feedback, setFeedback] = useState<Feedback | null>(null);

  useEffect(() => {
    if (!id) return;
    apiClient.getFeedback(id).then(setFeedback).catch(() => {});
  }, [id]);

  if (!feedback) {
    return <div className="px-6 py-16 text-center text-slate-500">Cargando retroalimentación...</div>;
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="text-2xl font-bold">Retroalimentación pedagógica</h1>
      <p className="mt-1 text-sm text-slate-500">Rúbrica v{feedback.rubric_version}</p>
      <div className="mt-6 grid grid-cols-3 gap-4">
        {Object.entries(feedback.scores).map(([key, score]) => (
          <div key={key} className="rounded-lg border border-border bg-white p-4 text-center">
            <p className="text-xs text-slate-500 capitalize">{key.replace(/_/g, " ")}</p>
            <p className="text-2xl font-bold text-primary">{score}/5</p>
          </div>
        ))}
      </div>
      <div className="mt-8 rounded-lg border border-border bg-white p-6">
        <pre className="whitespace-pre-wrap font-sans text-sm">{feedback.narrative}</pre>
      </div>
      {feedback.highlights && feedback.highlights.length > 0 && (
        <div className="mt-6">
          <h2 className="font-semibold">Fragmentos destacados</h2>
          <ul className="mt-2 space-y-2">
            {feedback.highlights.map((h, i) => (
              <li key={i} className="rounded border border-border bg-muted p-3 text-sm italic">
                &ldquo;{h.quote}&rdquo;
              </li>
            ))}
          </ul>
        </div>
      )}
      <Link href="/scenarios" className="mt-8 inline-block text-primary hover:underline">
        Practicar otro escenario
      </Link>
    </div>
  );
}
