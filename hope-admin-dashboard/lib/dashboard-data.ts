import { fetchDonations, fetchPayouts, type DonationRecord, type PayoutRecord } from "./hope-api";

const round2 = (n: number) => Math.round(n * 100) / 100;

export interface DonationRow {
  id: string;
  donorName: string;
  donorEmail: string;
  amount: number;
  currency: string;
  status: string;
  orderId: string;
  captureId: string;
  date: string | null;
  dateTime: string | null;
  isCompleted: boolean;
}

export interface PayoutRow {
  id: string;
  beneficiaryName: string;
  recipientEmail: string;
  amount: number;
  currency: string;
  batchStatus: string;
  itemStatus: string;
  status: string;
  batchId: string;
  itemId: string;
  date: string | null;
  dateTime: string | null;
  isSuccess: boolean;
}

export interface FundSummaryRow {
  id: string;
  name: string;
  totalDonations: number;
  totalPayouts: number;
  availableBalance: number;
  pendingDonations: number;
  pendingPayouts: number;
  totalTransactions: number;
  currency: string;
}

export interface TransactionRow {
  id: string;
  type: "Donation" | "Payout";
  direction: "Inflow" | "Outflow";
  counterparty: string;
  amount: number;
  signedAmount: number;
  currency: string;
  status: string;
  referenceId: string;
  date: string | null;
  dateTime: string | null;
}

export interface StatusBreakdownRow {
  id: string;
  category: "Donation" | "Payout";
  status: string;
  count: number;
  totalAmount: number;
}

function mapDonations(records: DonationRecord[]): DonationRow[] {
  return records.map((d) => {
    const isCompleted = d.payment_status === "COMPLETED";
    const amt = Number(d.amount) || 0;
    return {
      id: `DON-${d.id}`,
      donorName: d.donor_name || "Anonymous Donor",
      donorEmail: d.donor_email || "—",
      amount: amt,
      currency: d.currency || "USD",
      status: d.payment_status || "UNKNOWN",
      orderId: d.paypal_order_id,
      captureId: d.paypal_capture_id || "—",
      date: d.created_at ? d.created_at.slice(0, 10) : null,
      dateTime: d.created_at || null,
      isCompleted,
    };
  });
}

function mapPayouts(records: PayoutRecord[]): PayoutRow[] {
  return records.map((p) => {
    const isSuccess = p.item_status === "SUCCESS";
    const amt = Number(p.amount) || 0;
    return {
      id: p.id,
      beneficiaryName: p.beneficiary_name || "Unknown Beneficiary",
      recipientEmail: p.recipient_email,
      amount: amt,
      currency: p.currency || "USD",
      batchStatus: p.batch_status || "PENDING",
      itemStatus: p.item_status || "PENDING",
      status: p.item_status || p.batch_status || "PENDING",
      batchId: p.paypal_batch_id,
      itemId: p.paypal_item_id || "—",
      date: p.created_at ? p.created_at.slice(0, 10) : null,
      dateTime: p.created_at || null,
      isSuccess,
    };
  });
}

function buildFundSummary(donations: DonationRow[], payouts: PayoutRow[]): FundSummaryRow[] {
  const completedDonations = donations.filter((d) => d.isCompleted);
  const pendingDonations = donations.filter((d) => !d.isCompleted);
  const successPayouts = payouts.filter((p) => p.isSuccess);
  const pendingPayouts = payouts.filter((p) => !p.isSuccess);

  const totalDonations = round2(completedDonations.reduce((sum, d) => sum + d.amount, 0));
  const totalPayouts = round2(successPayouts.reduce((sum, p) => sum + p.amount, 0));
  const availableBalance = round2(totalDonations - totalPayouts);
  const pendingDonationsAmt = round2(pendingDonations.reduce((sum, d) => sum + d.amount, 0));
  const pendingPayoutsAmt = round2(pendingPayouts.reduce((sum, p) => sum + p.amount, 0));

  return [
    {
      id: "HOPE-POOL-1",
      name: "Hope Medical Treatment Pooled Fund",
      totalDonations,
      totalPayouts,
      availableBalance,
      pendingDonations: pendingDonationsAmt,
      pendingPayouts: pendingPayoutsAmt,
      totalTransactions: donations.length + payouts.length,
      currency: "USD",
    },
  ];
}

function buildTransactions(donations: DonationRow[], payouts: PayoutRow[]): TransactionRow[] {
  const donationTxs: TransactionRow[] = donations.map((d) => ({
    id: d.id,
    type: "Donation",
    direction: "Inflow",
    counterparty: d.donorName,
    amount: d.amount,
    signedAmount: d.amount,
    currency: d.currency,
    status: d.status,
    referenceId: d.orderId,
    date: d.date,
    dateTime: d.dateTime,
  }));

  const payoutTxs: TransactionRow[] = payouts.map((p) => ({
    id: `PAY-${p.id.slice(0, 8)}`,
    type: "Payout",
    direction: "Outflow",
    counterparty: p.beneficiaryName,
    amount: p.amount,
    signedAmount: -p.amount,
    currency: p.currency,
    status: p.status,
    referenceId: p.batchId,
    date: p.date,
    dateTime: p.dateTime,
  }));

  return [...donationTxs, ...payoutTxs].sort((a, b) => {
    const da = a.dateTime ? new Date(a.dateTime).getTime() : 0;
    const db = b.dateTime ? new Date(b.dateTime).getTime() : 0;
    return db - da;
  });
}

function buildStatusBreakdown(donations: DonationRow[], payouts: PayoutRow[]): StatusBreakdownRow[] {
  const map = new Map<string, StatusBreakdownRow>();

  for (const d of donations) {
    const key = `Donation-${d.status}`;
    const existing = map.get(key) || {
      id: key,
      category: "Donation",
      status: d.status,
      count: 0,
      totalAmount: 0,
    };
    existing.count += 1;
    existing.totalAmount = round2(existing.totalAmount + d.amount);
    map.set(key, existing);
  }

  for (const p of payouts) {
    const key = `Payout-${p.status}`;
    const existing = map.get(key) || {
      id: key,
      category: "Payout",
      status: p.status,
      count: 0,
      totalAmount: 0,
    };
    existing.count += 1;
    existing.totalAmount = round2(existing.totalAmount + p.amount);
    map.set(key, existing);
  }

  return [...map.values()];
}

export async function getDashboardData(asOf = new Date()) {
  let donationsData = { count: 0, limit: 200, offset: 0, items: [] as DonationRecord[] };
  let payoutsData = { count: 0, limit: 200, offset: 0, items: [] as PayoutRecord[] };

  try {
    const [dRes, pRes] = await Promise.all([
      fetchDonations(200).catch((e) => {
        console.warn("Could not fetch donations from Hope backend:", e.message);
        return { count: 0, limit: 200, offset: 0, items: [] };
      }),
      fetchPayouts(200).catch((e) => {
        console.warn("Could not fetch payouts from Hope backend:", e.message);
        return { count: 0, limit: 200, offset: 0, items: [] };
      }),
    ]);
    donationsData = dRes;
    payoutsData = pRes;
  } catch (err) {
    console.error("Dashboard data fetch error:", err);
  }

  const donations = mapDonations(donationsData.items);
  const payouts = mapPayouts(payoutsData.items);
  const pooledFund = buildFundSummary(donations, payouts);
  const transactions = buildTransactions(donations, payouts);
  const statusBreakdown = buildStatusBreakdown(donations, payouts);

  return {
    asOf: asOf.toISOString(),
    donations,
    payouts,
    pooledFund,
    transactions,
    statusBreakdown,
  };
}

export type DashboardData = Awaited<ReturnType<typeof getDashboardData>>;
