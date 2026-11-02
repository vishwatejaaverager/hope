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

declare const __BACKEND_URL__: string | undefined;

function getApiBaseUrl(): string {
  if (import.meta.env.DEV) {
    return "";
  }
  if (typeof __BACKEND_URL__ !== "undefined" && __BACKEND_URL__) {
    return __BACKEND_URL__.replace(/\/$/, "");
  }
  const viteUrl = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, "");
  if (viteUrl) {
    return viteUrl;
  }
  return "https://hope-9dq5.onrender.com";
}

const API_BASE_URL = getApiBaseUrl();

async function handleResponse<T>(res: Response): Promise<T> {
  const contentType = res.headers.get("content-type");

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const errorData = await res.json();
      const detail = errorData?.detail;
      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail.map((x: any) => x.msg || JSON.stringify(x)).join("; ");
      }
    } catch {
      // Non-JSON error response
    }
    throw new Error(message);
  }

  if (!contentType || !contentType.includes("application/json")) {
    throw new Error(`Expected JSON response from backend, received ${contentType || "HTML"}`);
  }

  return (await res.json()) as T;
}

export async function getDonationSummary(): Promise<DonationSummary> {
  const res = await fetch(`${API_BASE_URL}/api/payments/summary`);
  return handleResponse<DonationSummary>(res);
}

export async function getPaymentConfig(): Promise<PaymentConfig> {
  const res = await fetch(`${API_BASE_URL}/api/payments/config`);
  return handleResponse<PaymentConfig>(res);
}

export async function createOrder(amount: string, currency = "USD"): Promise<CreateOrderResponse> {
  const res = await fetch(`${API_BASE_URL}/api/payments/create-order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount, currency }),
  });
  return handleResponse<CreateOrderResponse>(res);
}

export async function captureOrder(orderId: string): Promise<CaptureOrderResponse> {
  const res = await fetch(`${API_BASE_URL}/api/payments/capture-order/${encodeURIComponent(orderId)}`, {
    method: "POST",
  });
  return handleResponse<CaptureOrderResponse>(res);
}
