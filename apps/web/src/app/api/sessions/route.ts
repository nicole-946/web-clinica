import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function POST(req: Request) {
  await req.json();
  return NextResponse.json(mockStore.createSession());
}
