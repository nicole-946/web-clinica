"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import PatientSelector from "@/components/PatientSelector";

export default function ScenariosPage() {
  const router = useRouter();

  useEffect(() => {
    const userId = localStorage.getItem("clinical-sim-user-id");
    if (!userId) {
      router.replace("/disclaimer");
    }
  }, [router]);

  return (
    <div className="mx-auto max-w-4xl px-6 py-12">
      <div className="border-b border-slate-100 pb-6">
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Selección de Paciente
        </h1>
        <p className="mt-2 text-base text-slate-500">
          Elige una patología específica para practicar tu entrevista clínica o selecciona un caso aleatorio para evaluar tus habilidades de diagnóstico.
        </p>
      </div>

      <div className="mt-10">
        <PatientSelector />
      </div>

      <div className="mt-12 border-t border-slate-100 pt-6">
        <Link href="/" className="text-sm font-semibold text-primary hover:underline">
          &larr; Volver al inicio
        </Link>
      </div>
    </div>
  );
}
