import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const backendUrl =
      process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") || "https://hope-9dq5.onrender.com";

    let res: Response;
    try {
      res = await fetch(`${backendUrl}/api/auth/login-credentials`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
    } catch (fetchErr) {
      if (!backendUrl.includes("127.0.0.1") && !backendUrl.includes("localhost")) {
        res = await fetch("http://127.0.0.1:8000/api/auth/login-credentials", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
      } else {
        throw fetchErr;
      }
    }

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return NextResponse.json(
        { detail: data.detail || "Invalid email or password" },
        { status: res.status }
      );
    }

    const response = NextResponse.json({ success: true });

    // Extract hope_admin_session token from JSON token or backend set-cookie header
    const setCookieHeader = res.headers.get("set-cookie");
    const cookieMatch = setCookieHeader?.match(/hope_admin_session=([^;]+)/);
    const tokenValue = data.token || (cookieMatch ? cookieMatch[1] : null);

    if (tokenValue) {
      response.cookies.set("hope_admin_session", tokenValue, {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        maxAge: 86400 * 7,
      });
    }

    return response;
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : "Failed to connect to backend";
    return NextResponse.json({ detail: message }, { status: 502 });
  }
}
