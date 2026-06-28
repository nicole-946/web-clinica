import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function GET(_req: Request, { params }: { params: Promise<{ userId: string }> }) {
  const { userId } = await params;
  const accepted = mockStore.isAccepted(userId);
  return NextResponse.json({ accepted, version: "2025.1" });
}
