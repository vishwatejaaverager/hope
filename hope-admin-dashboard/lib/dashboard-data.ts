import {
  fetchCases,
  fetchDonations,
  fetchIncomingEmails,
  fetchOutgoingEmails,
  fetchPayouts,
  type CaseRecord,
  type DonationRecord,
  type IncomingEmailRecord,
  type OutgoingEmailRecord,
  type PayoutRecord,
} from "./hope-api";

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

export interface CaseRow {
  id: string;
  caseNumber: string;
  patientName: string;
  patientEmail: string;
  medicalCategory: string;
  hospitalName: string;
  treatmentDescription: string;
  estimatedCost: number;
  requestedAmount: number;
  currency: string;
  urgency: string;
  status: string;
  overallSummary: string;
  nextAction: string;
  pendingItemsText: string;
  incomingEmailCount: number;
  outgoingEmailCount: number;
  totalEmailCount: number;
  date: string | null;
  dateTime: string | null;
}

export interface EmailRow {
  id: string;
  direction: "Incoming" | "Outgoing";
  applicationId: string;
  caseId: string;
  sender: string;
  recipient: string;
  subject: string;
  bodySnippet: string;
  aiSummaryText: string;
  attachmentCount: number;
  status: string;
  messageId: string;
  date: string | null;
  dateTime: string | null;
  isIncoming: boolean;
  isOutgoing: boolean;
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

function formatAiSummary(val: unknown): string {
  if (!val) return "—";
  if (typeof val === "string") return val;
  if (typeof val === "object") {
    const obj = val as Record<string, unknown>;
    if (typeof obj.summary === "string") return obj.summary;
    try {
      return JSON.stringify(val);
    } catch {
      return String(val);
    }
  }
  return String(val);
}

function formatPendingItems(val: unknown): string {
  if (!val) return "—";
  if (Array.isArray(val)) return val.map(String).join(", ") || "—";
  if (typeof val === "string") return val;
  try {
    return JSON.stringify(val);
  } catch {
    return "—";
  }
}

function mapCases(records: CaseRecord[]): CaseRow[] {
  return records.map((c) => {
    const inc = Number(c.incoming_email_count) || 0;
    const out = Number(c.outgoing_email_count) || 0;
    return {
      id: c.id,
      caseNumber: c.case_number,
      patientName: c.patient_name || "Unknown Patient",
      patientEmail: c.patient_email || "—",
      medicalCategory: c.medical_category || "general",
      hospitalName: c.hospital_name || "—",
      treatmentDescription: c.treatment_description || "—",
      estimatedCost: Number(c.estimated_cost) || 0,
      requestedAmount: Number(c.requested_amount) || 0,
      currency: c.currency || "USD",
      urgency: (c.urgency || "medium").toUpperCase(),
      status: (c.status || "new").toUpperCase(),
      overallSummary: c.overall_summary || "No summary yet",
      nextAction: c.next_action || "—",
      pendingItemsText: formatPendingItems(c.pending_items),
      incomingEmailCount: inc,
      outgoingEmailCount: out,
      totalEmailCount: inc + out,
      date: c.created_at ? c.created_at.slice(0, 10) : null,
      dateTime: c.created_at || null,
    };
  });
}

function mapEmails(
  incoming: IncomingEmailRecord[],
  outgoing: OutgoingEmailRecord[],
): EmailRow[] {
  const incRows: EmailRow[] = incoming.map((em) => {
    const ts = em.received_at || em.created_at;
    return {
      id: `INC-${em.id}`,
      direction: "Incoming",
      applicationId: em.application_id || "—",
      caseId: em.case_id || "—",
      sender: em.sender,
      recipient: em.recipient,
      subject: em.subject || "(No subject)",
      bodySnippet: em.body_plain ? em.body_plain.slice(0, 160) : "—",
      aiSummaryText: formatAiSummary(em.ai_summary),
      attachmentCount: Number(em.attachment_count) || 0,
      status: "RECEIVED",
      messageId: em.message_id,
      date: ts ? ts.slice(0, 10) : null,
      dateTime: ts || null,
      isIncoming: true,
      isOutgoing: false,
    };
  });

  const outRows: EmailRow[] = outgoing.map((em) => {
    const ts = em.created_at;
    return {
      id: `OUT-${em.id}`,
      direction: "Outgoing",
      applicationId: em.application_id || "—",
      caseId: em.case_id || "—",
      sender: "Hope Verification",
      recipient: em.recipient_email,
      subject: em.subject || "(No subject)",
      bodySnippet: em.body_plain ? em.body_plain.slice(0, 160) : "—",
      aiSummaryText: "Outbound verification / follow-up email",
      attachmentCount: 0,
      status: (em.status || "pending").toUpperCase(),
      messageId: em.correlation_id || em.reply_to_message_id || "—",
      date: ts ? ts.slice(0, 10) : null,
      dateTime: ts || null,
      isIncoming: false,
      isOutgoing: true,
    };
  });

  return [...incRows, ...outRows].sort((a, b) => {
    const da = a.dateTime ? new Date(a.dateTime).getTime() : 0;
    const db = b.dateTime ? new Date(b.dateTime).getTime() : 0;
    return db - da;
  });
}

export async function getDashboardData(asOf = new Date()) {
  let donationsData = { count: 0, limit: 200, offset: 0, items: [] as DonationRecord[] };
  let payoutsData = { count: 0, limit: 200, offset: 0, items: [] as PayoutRecord[] };
  let casesData: CaseRecord[] = [];
  let incomingEmailsData: IncomingEmailRecord[] = [];
  let outgoingEmailsData: OutgoingEmailRecord[] = [];

  try {
    const [dRes, pRes, cRes, incRes, outRes] = await Promise.all([
      fetchDonations(200).catch((e) => {
        console.warn("Could not fetch donations from Hope backend:", e.message);
        return { count: 0, limit: 200, offset: 0, items: [] };
      }),
      fetchPayouts(200).catch((e) => {
        console.warn("Could not fetch payouts from Hope backend:", e.message);
        return { count: 0, limit: 200, offset: 0, items: [] };
      }),
      fetchCases(100).catch((e) => {
        console.warn("Could not fetch cases from Hope backend:", e.message);
        return [] as CaseRecord[];
      }),
      fetchIncomingEmails(100).catch((e) => {
        console.warn("Could not fetch incoming emails from Hope backend:", e.message);
        return [] as IncomingEmailRecord[];
      }),
      fetchOutgoingEmails(100).catch((e) => {
        console.warn("Could not fetch outgoing emails from Hope backend:", e.message);
        return [] as OutgoingEmailRecord[];
      }),
    ]);
    donationsData = dRes;
    payoutsData = pRes;
    casesData = cRes;
    incomingEmailsData = incRes;
    outgoingEmailsData = outRes;
  } catch (err) {
    console.error("Dashboard data fetch error:", err);
  }

  const donations = mapDonations(donationsData.items);
  const payouts = mapPayouts(payoutsData.items);
  const pooledFund = buildFundSummary(donations, payouts);
  const transactions = buildTransactions(donations, payouts);
  const statusBreakdown = buildStatusBreakdown(donations, payouts);
  const cases = mapCases(casesData);
  const emails = mapEmails(incomingEmailsData, outgoingEmailsData);

  return {
    asOf: asOf.toISOString(),
    donations,
    payouts,
    pooledFund,
    transactions,
    statusBreakdown,
    cases,
    emails,
  };
}

export type DashboardData = Awaited<ReturnType<typeof getDashboardData>>;
