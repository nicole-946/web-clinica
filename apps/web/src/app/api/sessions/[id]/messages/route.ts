import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return NextResponse.json(mockStore.getMessages(id));
}

export async function POST(req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const body = await req.json();
  try {
    const reply = mockStore.sendMessage(id, body.content);
    return NextResponse.json(reply);
  } catch {
    return NextResponse.json({ detail: "Session not found" }, { status: 404 });
  }
}
