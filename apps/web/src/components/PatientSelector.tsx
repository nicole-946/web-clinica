"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient, type Case } from "@/lib/api-client";

export default function PatientSelector() {
  const router = useRouter();
  const [cases, setCases] = useState<Case[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [startingId, setStartingId] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .getCases()
      .then((data) => {
        setCases(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("No se pudieron cargar los casos. Verifica la conexión con el servidor.");
        setLoading(false);
      });
  }, []);

  async function handleSelect(caseId: string) {
    const userId = localStorage.getItem("clinical-sim-user-id");
    if (!userId) {
      router.push("/disclaimer");
      return;
    }
    setStartingId(caseId);
    try {
      const session = await apiClient.startSession(userId, caseId);
      router.push(`/sessions/${session.session_id}`);
    } catch (err) {
      console.error(err);
      alert("Error al iniciar la sesión de simulación.");
      setStartingId(null);
    }
  }

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-center text-red-700">
        <p className="font-semibold">{error}</p>
        <button
          onClick={() => {
            setLoading(true);
            setError(null);
            apiClient.getCases().then(setCases).then(() => setLoading(false)).catch(() => setError("No se pudieron cargar los casos."));
          }}
          className="mt-4 rounded-md bg-red-600 px-4 py-2 text-sm text-white hover:bg-red-700"
        >
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Catálogo de Casos */}
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {cases.map((c) => {
          let borderStyle = "border-slate-200 hover:border-slate-300";
          let bgGradient = "from-slate-50 to-white";
          let titleColor = "text-slate-800";
          let badgeText = "Dificultad";
          let badgeColor = "bg-slate-100 text-slate-700";
          let description = "";

          if (c.id.includes("depression")) {
            borderStyle = "hover:border-indigo-400 hover:shadow-indigo-50";
            bgGradient = "from-indigo-50/50 to-white";
            titleColor = "text-indigo-900";
            badgeText = "Intermedio";
            badgeColor = "bg-indigo-100 text-indigo-700";
            description = "Paciente presenta decaimiento generalizado, anhedonia y síntomas vegetativos.";
          } else if (c.id.includes("anxiety")) {
            borderStyle = "hover:border-emerald-400 hover:shadow-emerald-50";
            bgGradient = "from-emerald-50/50 to-white";
            titleColor = "text-emerald-950";
            badgeText = "Intermedio";
            badgeColor = "bg-emerald-100 text-emerald-800";
            description = "Paciente con rumiación constante, síntomas somáticos y tensión muscular.";
          } else if (c.id.includes("borderline")) {
            borderStyle = "hover:border-rose-400 hover:shadow-rose-50";
            bgGradient = "from-rose-50/50 to-white";
            titleColor = "text-rose-900";
            badgeText = "Avanzado";
            badgeColor = "bg-rose-100 text-rose-700";
            description = "Interacción compleja con alta reactividad afectiva e impulsividad.";
          }

          return (
            <div
              key={c.id}
              className={`flex flex-col justify-between rounded-xl border p-6 transition-all duration-300 bg-gradient-to-b shadow-sm ${borderStyle} ${bgGradient}`}
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${badgeColor}`}>
                    {badgeText}
                  </span>
                </div>
                <h3 className={`mt-4 text-lg font-bold tracking-tight ${titleColor}`}>
                  {c.patologia}
                </h3>
                <p className="mt-2 text-sm text-slate-500 line-clamp-3">
                  {description}
                </p>
              </div>
              <button
                onClick={() => handleSelect(c.id)}
                disabled={startingId !== null}
                className="mt-6 w-full rounded-lg bg-primary py-2 text-sm font-semibold text-primary-foreground shadow transition hover:opacity-90 disabled:opacity-50"
              >
                {startingId === c.id ? "Iniciando..." : "Iniciar Simulación"}
              </button>
            </div>
          );
        })}
      </div>

      {/* Tarjeta Destacada Blind Test */}
      <div className="relative overflow-hidden rounded-2xl border border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-8 shadow-md">
        <div className="absolute right-0 top-0 h-32 w-32 -translate-y-6 translate-x-6 rounded-full bg-amber-100 opacity-50 blur-3xl" />
        <div className="relative max-w-xl">
          <span className="inline-block rounded-full bg-amber-100 border border-amber-200 px-3 py-1 text-xs font-bold text-amber-800 uppercase tracking-wider">
            Evaluación Diagnóstica
          </span>
          <h3 className="mt-4 text-xl font-extrabold text-amber-950 tracking-tight">
            Paciente Aleatorio (Blind Test)
          </h3>
          <p className="mt-2 text-sm text-amber-800 leading-relaxed">
            Ponte a prueba en un entorno realista. Te asignaremos un paciente virtual de manera
            completamente oculta. Deberás aplicar técnicas de entrevista para identificar su patología
            y sintomatología sin pistas previas.
          </p>
          <button
            onClick={() => handleSelect("random")}
            disabled={startingId !== null}
            className="mt-6 rounded-xl bg-amber-800 px-6 py-2.5 text-sm font-bold text-white shadow-md hover:bg-amber-900 transition disabled:opacity-50"
          >
            {startingId === "random" ? "Asignando..." : "Iniciar Blind Test"}
          </button>
        </div>
      </div>
    </div>
  );
}
