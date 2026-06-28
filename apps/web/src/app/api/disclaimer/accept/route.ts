import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function POST(req: Request) {
  const body = await req.json();
  mockStore.accept(body.user_id);
  return NextResponse.json({ accepted: true, version: "2025.1" });
}
