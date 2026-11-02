import { NextResponse } from "next/server";

export async function POST() {
  const backendUrl =
    process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

  try {
    await fetch(`${backendUrl}/api/auth/logout`, { method: "POST" });
  } catch {}

  const response = NextResponse.json({ success: true });
  response.cookies.set("hope_admin_session", "", {
    path: "/",
    maxAge: 0,
  });
  return response;
}
