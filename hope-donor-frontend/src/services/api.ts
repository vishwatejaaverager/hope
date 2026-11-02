export interface PaymentConfig {
  client_id: string;
  currency: string;
}

export interface CreateOrderResponse {
  order_id: string;
  status: string;
}

export interface CaptureOrderResponse {
  order_id: string;
  order_status: string;
  capture_status?: string | null;
  transaction_id?: string | null;
  amount?: string | null;
  currency?: string | null;
  success: boolean;
  message: string;
}

export interface DonationSummary {
  total_raised: string;
  donation_count: number;
  currency: string;
}

export interface ApiError {
  detail?: string | Array<{ msg: string }>;
}

async function handleResponse<T>(res: Response): Promise<T> {
  let data: any = {};
  try {
    data = await res.json();
  } catch {
    // Non-JSON response
  }

  if (!res.ok) {
    const detail = data?.detail;
    let message = `Request failed (${res.status})`;
    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail)) {
      message = detail.map((x: any) => x.msg || JSON.stringify(x)).join("; ");
    }
    throw new Error(message);
  }

  return data as T;
}

export async function getDonationSummary(): Promise<DonationSummary> {
  const res = await fetch("/api/payments/summary");
  return handleResponse<DonationSummary>(res);
}

export async function getPaymentConfig(): Promise<PaymentConfig> {
  const res = await fetch("/api/payments/config");
  return handleResponse<PaymentConfig>(res);
}

export async function createOrder(amount: string, currency = "USD"): Promise<CreateOrderResponse> {
  const res = await fetch("/api/payments/create-order", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, currency }),
  });
  return handleResponse<CreateOrderResponse>(res);
}

export async function captureOrder(orderId: string): Promise<CaptureOrderResponse> {
  const res = await fetch(`/api/payments/capture-order/${encodeURIComponent(orderId)}`, {
    method: "POST",
  });
  return handleResponse<CaptureOrderResponse>(res);
}
