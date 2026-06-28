import Link from "next/link";

export default function HomePage() {
  return (
    <div className="mx-auto max-w-2xl px-6 py-16 text-center">
      <h1 className="text-4xl font-bold tracking-tight">Clinical Sim</h1>
      <p className="mt-4 text-lg text-slate-600">
        Plataforma de simulación clínica para estudiantes de psicología.
        Practica entrevistas con pacientes virtuales en un entorno seguro y educativo.
      </p>
      <Link
        href="/disclaimer"
        className="mt-8 inline-block rounded-lg bg-primary px-6 py-3 text-primary-foreground font-medium hover:opacity-90"
      >
        Comenzar
      </Link>
    </div>
  );
}
