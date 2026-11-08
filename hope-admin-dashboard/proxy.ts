import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const { pathname, searchParams } = request.nextUrl;
  const tokenParam = searchParams.get("token");

  // If returning from PayPal OAuth callback with ?token=..., persist session cookie on dashboard origin
  if (pathname.startsWith("/dashboard") && tokenParam) {
    const cleanUrl = new URL(pathname, request.url);
    const response = NextResponse.redirect(cleanUrl);
    response.cookies.set("hope_admin_session", tokenParam, {
      httpOnly: true,
      sameSite: "lax",
      path: "/",
      maxAge: 86400 * 7,
    });
    return response;
  }

  const sessionCookie = request.cookies.get("hope_admin_session");

  // Protect dashboard routes: require session cookie
  if (pathname.startsWith("/dashboard")) {
    if (!sessionCookie?.value) {
      const loginUrl = new URL("/login", request.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  // If already logged in, redirect /login to /dashboard
  if (pathname === "/login") {
    if (sessionCookie?.value) {
      const dashboardUrl = new URL("/dashboard", request.url);
      return NextResponse.redirect(dashboardUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/dashboard", "/login"],
};
