import { NextResponse } from "next/server";
import { mockStore } from "@/lib/mock-store";

export async function POST(req: Request) {
  try {
    const { user_id, case_id } = await req.json();
    if (!user_id || !case_id) {
      return NextResponse.json({ error: "Missing required fields" }, { status: 400 });
    }
    const result = mockStore.startSession(user_id, case_id);
    return NextResponse.json(result);
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
