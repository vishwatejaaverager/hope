import { cookies } from "next/headers";
import { NextResponse } from "next/server";

export async function GET() {
  const cookieStore = await cookies();
  const session = cookieStore.get("hope_admin_session");

  if (!session?.value) {
    return NextResponse.json({ authenticated: false }, { status: 401 });
  }

  const backendUrl =
    process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

  try {
    const res = await fetch(`${backendUrl}/api/auth/me`, {
      headers: {
        Authorization: `Bearer ${session.value}`,
        Cookie: `hope_admin_session=${session.value}`,
      },
      cache: "no-store",
    });

    if (!res.ok) {
      return NextResponse.json({ authenticated: false }, { status: res.status });
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ authenticated: false }, { status: 500 });
  }
}
