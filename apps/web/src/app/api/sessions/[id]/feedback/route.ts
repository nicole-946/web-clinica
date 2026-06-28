import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const report = mockStore.getFeedback(id);
  if (!report) return NextResponse.json({ detail: "Not found" }, { status: 404 });
  return NextResponse.json(report);
}
