import { NextResponse } from 'next/server';
import { getBackendUrl } from '@/lib/hope-api';

export async function POST(request: Request) {
  const backendUrl = getBackendUrl();
  const webhookSecret = process.env.EMAIL_WEBHOOK_SECRET || 'hope@0926';
  const { searchParams } = new URL(request.url);
  const targetUrl = searchParams.get('target_webhook_url');

  const query = targetUrl ? `?target_webhook_url=${encodeURIComponent(targetUrl)}` : '';

  try {
    const res = await fetch(`${backendUrl}/api/v1/emails/dispatch-pending${query}`, {
      method: 'POST',
      headers: {
        'X-Webhook-Secret': webhookSecret,
      },
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

