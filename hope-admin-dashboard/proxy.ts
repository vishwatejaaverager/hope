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

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/dashboard", "/login"],
};
