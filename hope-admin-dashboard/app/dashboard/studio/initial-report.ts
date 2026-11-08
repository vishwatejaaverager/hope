// The built-in "Hope Financial Overview" report: pages for overview, donations, and payouts.
import type { AgPageState, AgReportState, AgWidgetLayoutState } from "ag-studio";

const at = (xTrack: number, yTrack: number, xSpan: number, ySpan: number): AgWidgetLayoutState => ({
  xTrack,
  yTrack,
  xSpan,
  ySpan,
});

const title = (text: string) => ({ title: { enabled: true, text } });
const sum = (id: string) => ({ id, aggregation: "sum" as const });
const avg = (id: string) => ({ id, aggregation: "avg" as const });
const countd = (id: string) => ({ id, aggregation: "countd" as const });

const HOPE_FONT = 'Outfit, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';

const typography = (fontSize: number, fontWeight: "normal" | "bold" = "normal") => ({
  fontFamily: HOPE_FONT,
  fontSize,
  fontWeight,
  fontStyle: "normal" as const,
});

const kpi = (text: string, value: { id: string; aggregation?: "sum" | "avg" | "countd" }) => ({
  type: "value" as const,
  dataMapping: {
    value: [value],
  },
  format: {
    title: { enabled: true, text, typography: typography(14, "bold") },
    caption: { enabled: true, text: "", typography: typography(0) },
    style: { typography: typography(22, "bold") },
  },
});

// --- Overview Page -------------------------------------------------------------
const overview: AgPageState = {
  id: "overview",
  widgets: {
    "kpi-donations": kpi("Total Donations Received", sum("pooledFund.totalDonations")),
    "kpi-payouts": kpi("Total Payouts Made", sum("pooledFund.totalPayouts")),
    "kpi-balance": kpi("Available Pooled Fund", sum("pooledFund.availableBalance")),
    "kpi-pending": kpi("Pending Payouts", sum("pooledFund.pendingPayouts")),
    "status-breakdown-chart": {
      type: "pie-chart",
      dataMapping: {
        categoryKey: [{ id: "statusBreakdown.status" }],
        valueKey: [sum("statusBreakdown.totalAmount")],
      },
      format: {
        ...title("Volume by Transaction Status"),
        style: { theme: { common: { legend: { enabled: true } } } },
      },
    },
    "cashflow-grid": {
      type: "grid",
      dataMapping: {
        cols: [
          { id: "transactions.date" },
          { id: "transactions.type" },
          { id: "transactions.direction" },
          { id: "transactions.counterparty" },
          { id: "transactions.status" },
          { id: "transactions.amount" },
          { id: "transactions.signedAmount" },
          { id: "transactions.referenceId" },
        ],
      },
      format: title("Recent Cash Flow Activity"),
    },
  },
  widgetLayout: {
    "kpi-donations": at(0, 0, 6, 7),
    "kpi-payouts": at(6, 0, 6, 7),
    "kpi-balance": at(12, 0, 6, 7),
    "kpi-pending": at(18, 0, 6, 7),
    "status-breakdown-chart": at(0, 7, 8, 20),
    "cashflow-grid": at(8, 7, 16, 20),
  },
};

// --- Donations Page ------------------------------------------------------------
const donations: AgPageState = {
  id: "donations",
  widgets: {
    "kpi-donations-total": kpi("Total Donations Received", sum("donations.amount")),
    "kpi-donations-count": kpi("Donation Transactions", countd("donations.id")),
    "kpi-donations-avg": kpi("Average Donation", avg("donations.amount")),
    "donations-grid": {
      type: "grid",
      dataMapping: {
        cols: [
          { id: "donations.date" },
          { id: "donations.donorName" },
          { id: "donations.donorEmail" },
          { id: "donations.amount" },
          { id: "donations.status" },
          { id: "donations.orderId" },
          { id: "donations.captureId" },
        ],
      },
      format: title("Inbound Donations (PayPal Orders API)"),
    },
  },
  widgetLayout: {
    "kpi-donations-total": at(0, 0, 8, 7),
    "kpi-donations-count": at(8, 0, 8, 7),
    "kpi-donations-avg": at(16, 0, 8, 7),
    "donations-grid": at(0, 7, 24, 22),
  },
};

// --- Payouts Page --------------------------------------------------------------
const payouts: AgPageState = {
  id: "payouts",
  widgets: {
    "kpi-payouts-total": kpi("Total Beneficiary Payouts", sum("payouts.amount")),
    "kpi-payouts-count": kpi("Payout Disbursals", countd("payouts.id")),
    "kpi-payouts-avg": kpi("Average Payout", avg("payouts.amount")),
    "payouts-grid": {
      type: "grid",
      dataMapping: {
        cols: [
          { id: "payouts.date" },
          { id: "payouts.beneficiaryName" },
          { id: "payouts.recipientEmail" },
          { id: "payouts.amount" },
          { id: "payouts.status" },
          { id: "payouts.batchId" },
          { id: "payouts.itemId" },
        ],
      },
      format: title("Outbound Beneficiary Transfers (PayPal Payouts API)"),
    },
  },
  widgetLayout: {
    "kpi-payouts-total": at(0, 0, 8, 7),
    "kpi-payouts-count": at(8, 0, 8, 7),
    "kpi-payouts-avg": at(16, 0, 8, 7),
    "payouts-grid": at(0, 7, 24, 22),
  },
};

// --- Medical Cases Page --------------------------------------------------------
const cases: AgPageState = {
  id: "cases",
  widgets: {
    "kpi-cases-count": kpi("Total Medical Cases", countd("cases.id")),
    "kpi-cases-requested": kpi("Total Requested Support", sum("cases.requestedAmount")),
    "kpi-cases-estimated": kpi("Total Estimated Treatment Cost", sum("cases.estimatedCost")),
    "cases-grid": {
      type: "grid",
      dataMapping: {
        cols: [
          { id: "cases.caseNumber" },
          { id: "cases.patientName" },
          { id: "cases.patientEmail" },
          { id: "cases.medicalCategory" },
          { id: "cases.hospitalName" },
          { id: "cases.urgency" },
          { id: "cases.status" },
          { id: "cases.requestedAmount" },
          { id: "cases.estimatedCost" },
          { id: "cases.overallSummary" },
          { id: "cases.nextAction" },
          { id: "cases.pendingItemsText" },
          { id: "cases.totalEmailCount" },
          { id: "cases.date" },
        ],
      },
      format: title("Medical Assistance Cases & Living AI Summaries"),
    },
  },
  widgetLayout: {
    "kpi-cases-count": at(0, 0, 8, 7),
    "kpi-cases-requested": at(8, 0, 8, 7),
    "kpi-cases-estimated": at(16, 0, 8, 7),
    "cases-grid": at(0, 7, 24, 22),
  },
};

// --- Email Communications Page -------------------------------------------------
const emails: AgPageState = {
  id: "emails",
  widgets: {
    "kpi-emails-total": kpi("Total Emails Logged", countd("emails.id")),
    "kpi-emails-attachments": kpi("Total Attachments Received", sum("emails.attachmentCount")),
    "emails-by-direction-chart": {
      type: "pie-chart",
      dataMapping: {
        categoryKey: [{ id: "emails.direction" }],
        valueKey: [countd("emails.id")],
      },
      format: {
        ...title("Emails by Direction"),
        style: { theme: { common: { legend: { enabled: true } } } },
      },
    },
    "emails-grid": {
      type: "grid",
      dataMapping: {
        cols: [
          { id: "emails.date" },
          { id: "emails.direction" },
          { id: "emails.applicationId" },
          { id: "emails.sender" },
          { id: "emails.recipient" },
          { id: "emails.subject" },
          { id: "emails.bodySnippet" },
          { id: "emails.aiSummaryText" },
          { id: "emails.attachmentCount" },
          { id: "emails.status" },
        ],
      },
      format: title("Inbound & Outbound Email Communications (Zapier / Hostinger)"),
    },
  },
  widgetLayout: {
    "kpi-emails-total": at(0, 0, 8, 7),
    "kpi-emails-attachments": at(8, 0, 8, 7),
    "emails-by-direction-chart": at(16, 0, 8, 7),
    "emails-grid": at(0, 7, 24, 22),
  },
};

export const dashboardReport: AgReportState = {
  selectedPageId: overview.id,
  pages: [overview, donations, payouts, cases, emails],
};

export const initialReport = dashboardReport;
