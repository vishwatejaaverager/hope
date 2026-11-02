/**
 * Client for Hope FastAPI backend.
 * All data access is mediated through our backend; PayPal credentials never reach the client.
 */

export interface DonationRecord {
  id: number;
  donor_name: string | null;
  donor_email: string | null;
  amount: string;
  currency: string;
  payment_provider: string;
  paypal_order_id: string;
  paypal_capture_id: string | null;
  payment_status: string;
  created_at: string;
  updated_at: string;
}

export interface DonationHistoryResponse {
  count: number;
  limit: number;
  offset: number;
  items: DonationRecord[];
}

export interface PayoutRecord {
  id: string;
  beneficiary_name: string | null;
  recipient_email: string;
  amount: string;
  currency: string;
  payment_provider: string;
  paypal_batch_id: string;
  paypal_item_id: string | null;
  paypal_transaction_id: string | null;
  batch_status: string;
  item_status: string | null;
  created_at: string;
  updated_at: string;
}

export interface PayoutHistoryResponse {
  count: number;
  limit: number;
  offset: number;
  items: PayoutRecord[];
}

const BACKEND_URL =
  process.env.HOPE_BACKEND_URL?.replace(/\/$/, "") ||
  "https://hope-9dq5.onrender.com";

async function fetchFromBackend<T>(path: string): Promise<T> {
  const url = `${BACKEND_URL}${path}`;
  try {
    const res = await fetch(url, {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    });
    if (!res.ok) {
      const errText = await res.text().catch(() => "");
      throw new Error(`Hope API ${res.status} on ${path}: ${errText}`);
    }
    return (await res.json()) as T;
  } catch (error) {
    // If remote render is cold or unreachable, try localhost if not already on localhost
    if (!BACKEND_URL.includes("127.0.0.1") && !BACKEND_URL.includes("localhost")) {
      try {
        const localRes = await fetch(`http://127.0.0.1:8000${path}`, {
          cache: "no-store",
          headers: { Accept: "application/json" },
        });
        if (localRes.ok) {
          return (await localRes.json()) as T;
        }
      } catch {
        // fallback to original error
      }
    }
    throw error;
  }
}

export async function fetchDonations(limit = 200, offset = 0): Promise<DonationHistoryResponse> {
  return fetchFromBackend<DonationHistoryResponse>(`/api/payments/history?limit=${limit}&offset=${offset}`);
}

export async function fetchPayouts(limit = 200, offset = 0): Promise<PayoutHistoryResponse> {
  return fetchFromBackend<PayoutHistoryResponse>(`/api/payouts/history?limit=${limit}&offset=${offset}`);
}
