import { cookies } from "next/headers";
import { NextResponse } from 'next/server';
import { getBackendUrl } from '@/lib/hope-api';

export async function POST(
  _request: Request,
  context: { params: Promise<{ caseId: string }> },
) {
  const { caseId } = await context.params;
  const backendUrl = getBackendUrl();
  const session = (await cookies()).get("hope_admin_session")?.value;
  if (!session) {
    return NextResponse.json({ detail: "Sign in to manage payouts." }, { status: 401 });
  }

  try {
    const res = await fetch(`${backendUrl}/api/v1/cases/${encodeURIComponent(caseId)}/disburse`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${session}`,
      },
      body: "{}",
      cache: 'no-store',
    });

    const data = await res.json().catch(() => ({ detail: 'Invalid response from backend' }));
    return NextResponse.json(data, { status: res.status });
  } catch (err) {
    return NextResponse.json(
      { detail: err instanceof Error ? err.message : 'Failed to connect to backend' },
      { status: 502 },
    );
  }
}

