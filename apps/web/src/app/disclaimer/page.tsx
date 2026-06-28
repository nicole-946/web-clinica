"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient, type Disclaimer } from "@/lib/api-client";

export default function DisclaimerPage() {
  const router = useRouter();
  const [disclaimer, setDisclaimer] = useState<Disclaimer | null>(null);
  const [checked, setChecked] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiClient.getActiveDisclaimer().then(setDisclaimer).catch(() =>
      setError("No se pudo cargar el aviso legal. ¿Está el backend en ejecución?")
    );
  }, []);

  async function handleAccept() {
    if (!checked) return;
    setLoading(true);
    try {
      const user = await apiClient.getDemoUser();
      const status = await apiClient.getDisclaimerStatus(user.id);
      if (!status.accepted) {
        await apiClient.acceptDisclaimer(user.id);
      }
      localStorage.setItem("clinical-sim-user-id", user.id);
      router.push("/scenarios");
    } catch {
      setError("Error al registrar la aceptación.");
    } finally {
      setLoading(false);
    }
  }

  if (error) {
    return (
      <div className="mx-auto max-w-lg px-6 py-16 text-center text-destructive">
        {error}
      </div>
    );
  }

  if (!disclaimer) {
    return <div className="px-6 py-16 text-center text-slate-500">Cargando aviso legal...</div>;
  }

  return (
    <div className="mx-auto max-w-2xl px-6 py-10">
      <h1 className="text-2xl font-bold">Aviso Legal Obligatorio</h1>
      <p className="mt-1 text-sm text-slate-500">Versión {disclaimer.version}</p>
      <div className="mt-6 max-h-96 overflow-y-auto rounded-lg border border-border bg-white p-6 prose prose-sm">
        <pre className="whitespace-pre-wrap font-sans text-sm">{disclaimer.content_md}</pre>
      </div>
      <label className="mt-6 flex items-start gap-3 cursor-pointer">
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => setChecked(e.target.checked)}
          className="mt-1"
        />
        <span className="text-sm">
          He leído y comprendo que esta plataforma es exclusivamente una simulación educativa.
        </span>
      </label>
      <button
        onClick={handleAccept}
        disabled={!checked || loading}
        className="mt-6 w-full rounded-lg bg-primary px-6 py-3 text-primary-foreground font-medium disabled:opacity-50"
      >
        {loading ? "Procesando..." : "Aceptar y continuar"}
      </button>
    </div>
  );
}
