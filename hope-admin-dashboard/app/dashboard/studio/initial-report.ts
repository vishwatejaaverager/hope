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

export const dashboardReport: AgReportState = {
  selectedPageId: overview.id,
  pages: [overview, donations, payouts],
};

export const initialReport = dashboardReport;
