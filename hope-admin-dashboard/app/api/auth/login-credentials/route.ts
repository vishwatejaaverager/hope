import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const backendUrl =
      process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") || "http://127.0.0.1:8000";

    const res = await fetch(`${backendUrl}/api/auth/login-credentials`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return NextResponse.json(
        { detail: data.detail || "Invalid email or password" },
        { status: res.status }
      );
    }

    const response = NextResponse.json({ success: true });

    // Extract hope_admin_session token from backend response
    const setCookieHeader = res.headers.get("set-cookie");
    if (setCookieHeader) {
      const match = setCookieHeader.match(/hope_admin_session=([^;]+)/);
      if (match) {
        response.cookies.set("hope_admin_session", match[1], {
          httpOnly: true,
          sameSite: "lax",
          path: "/",
          maxAge: 86400 * 7,
        });
      }
    }

    return response;
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Failed to connect to backend";
    return NextResponse.json({ detail: message }, { status: 502 });
  }
}
