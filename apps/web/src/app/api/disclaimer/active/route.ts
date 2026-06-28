import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function GET() {
  return NextResponse.json(mockStore.getDisclaimer());
}
