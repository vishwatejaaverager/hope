import { NextResponse } from "next/server";

export async function GET() {
  const backendUrl =
    process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") || "https://hope-9dq5.onrender.com";

  return NextResponse.redirect(`${backendUrl}/api/auth/login`);
}

