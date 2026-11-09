import { NextResponse } from 'next/server';
import { getBackendUrl } from '@/lib/hope-api';

export async function POST(request: Request) {
  const backendUrl = getBackendUrl();
  const webhookSecret = process.env.EMAIL_WEBHOOK_SECRET || 'hope@0926';

  let bodyJson: Record<string, unknown> = {};
  try {
    bodyJson = await request.json();
  } catch {
    bodyJson = {};
  }

  try {
    const res = await fetch(`${backendUrl}/api/v1/emails/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': webhookSecret,
      },
      body: JSON.stringify(bodyJson),
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

