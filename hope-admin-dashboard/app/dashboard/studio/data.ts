// AG Studio data sources definition for Hope Medical Crowdfunding
import type {
  AgDataSourcesDefinition,
  AgFieldDefinition,
  AgFormat,
  AgRelationDefinition,
} from "ag-studio";
import type { DashboardData } from "@/lib/dashboard-data";

const CALENDAR_ID = "calendar";

type FieldSpec = [id: string, name: string, format: AgFormat, hide?: boolean];

const fields = (specs: FieldSpec[]): AgFieldDefinition[] =>
  specs.map(([id, name, format, hide]) => ({ id, name, format, ...(hide && { hide }) }));

const onCalendar = (tableId: string, fieldId: string, truncate?: "day"): AgRelationDefinition => ({
  id: `${tableId}-${fieldId}-calendar`,
  source: { tableId, fieldId },
  target: { calendarId: CALENDAR_ID },
  ...(truncate && { truncate }),
});

export const hasData = (data: DashboardData) =>
  data.donations.length > 0 || data.payouts.length > 0 || data.transactions.length > 0;

export function buildStudioData(data: DashboardData): AgDataSourcesDefinition {
  const dates = [
    ...data.donations.map((d) => d.date),
    ...data.payouts.map((p) => p.date),
    ...data.transactions.map((t) => t.date),
  ]
    .filter((d): d is string => !!d)
    .sort();

  const today = data.asOf.slice(0, 10);

  return {
    description:
      "Hope medical crowdfunding platform financial analytics: donations, beneficiary payouts, and pooled fund balance.",
    sources: [
      {
        id: "pooledFund",
        name: "Pooled Fund Summary",
        description: "High-level summary of total donations, total payouts, and available pooled balance.",
        data: data.pooledFund,
        fields: fields([
          ["id", "Fund ID", "textFormat", true],
          ["name", "Fund Name", "textFormat"],
          ["totalDonations", "Total Donations", "currencyFormat"],
          ["totalPayouts", "Total Payouts", "currencyFormat"],
          ["availableBalance", "Available Pooled Balance", "currencyFormat"],
          ["pendingDonations", "Pending Donations", "currencyFormat"],
          ["pendingPayouts", "Pending Payouts", "currencyFormat"],
          ["totalTransactions", "Total Transactions", "integerFormat"],
        ]),
      },
      {
        id: "donations",
        name: "Donation Transactions",
        description: "Inbound donor contributions received through PayPal Orders API.",
        data: data.donations,
        fields: fields([
          ["id", "ID", "textFormat", true],
          ["donorName", "Donor Name", "textFormat"],
          ["donorEmail", "Donor Email", "textFormat"],
          ["amount", "Donation Amount", "currencyFormat"],
          ["currency", "Currency", "textFormat", true],
          ["status", "Payment Status", "textFormat"],
          ["orderId", "PayPal Order ID", "textFormat"],
          ["captureId", "PayPal Capture ID", "textFormat"],
          ["date", "Date", "dateFormat"],
          ["dateTime", "Timestamp", "dateTimeFormat", true],
          ["isCompleted", "Is Completed", "booleanFormat"],
        ]),
      },
      {
        id: "payouts",
        name: "Beneficiary Payouts",
        description: "Outbound payouts sent from Hope merchant account to verified medical beneficiaries.",
        data: data.payouts,
        fields: fields([
          ["id", "Payout ID", "textFormat", true],
          ["beneficiaryName", "Beneficiary", "textFormat"],
          ["recipientEmail", "PayPal Recipient Email", "textFormat"],
          ["amount", "Payout Amount", "currencyFormat"],
          ["currency", "Currency", "textFormat", true],
          ["batchStatus", "Batch Status", "textFormat"],
          ["itemStatus", "Item Status", "textFormat"],
          ["status", "Payout Status", "textFormat"],
          ["batchId", "PayPal Batch ID", "textFormat"],
          ["itemId", "PayPal Item ID", "textFormat"],
          ["date", "Date", "dateFormat"],
          ["dateTime", "Timestamp", "dateTimeFormat", true],
          ["isSuccess", "Is Success", "booleanFormat"],
        ]),
      },
      {
        id: "transactions",
        name: "Cash Flow Ledger",
        description: "Combined ledger of all inflows (donations) and outflows (payouts).",
        data: data.transactions,
        fields: fields([
          ["id", "Transaction ID", "textFormat"],
          ["type", "Transaction Type", "textFormat"],
          ["direction", "Direction", "textFormat"],
          ["counterparty", "Donor / Beneficiary", "textFormat"],
          ["amount", "Gross Amount", "currencyFormat"],
          ["signedAmount", "Net Cash Flow", "currencyFormat"],
          ["currency", "Currency", "textFormat", true],
          ["status", "Status", "textFormat"],
          ["referenceId", "Reference ID", "textFormat"],
          ["date", "Date", "dateFormat"],
          ["dateTime", "Timestamp", "dateTimeFormat", true],
        ]),
      },
      {
        id: "statusBreakdown",
        name: "Status Breakdown",
        description: "Aggregated counts and amounts by transaction status.",
        data: data.statusBreakdown,
        fields: fields([
          ["id", "ID", "textFormat", true],
          ["category", "Category", "textFormat"],
          ["status", "Status", "textFormat"],
          ["count", "Transaction Count", "integerFormat"],
          ["totalAmount", "Total Amount", "currencyFormat"],
        ]),
      },
    ],
    relationships: [
      onCalendar("donations", "date"),
      onCalendar("payouts", "date"),
      onCalendar("transactions", "date", "day"),
    ],
    calendars: [
      {
        id: CALENDAR_ID,
        label: "Calendar",
        range: {
          from: { type: "date", value: dates[0] ?? today },
          to: { type: "date", value: dates.at(-1) ?? today },
        },
        fragments: ["year", "quarter", "month", "week", "day", "dayOfWeek"],
      },
    ],
    expressions: [
      {
        id: "payoutRate",
        name: "Payout Distribution Rate",
        description: "Percentage of received donations distributed as payouts.",
        format: "percentageFormat",
        isMeasure: true,
        expression: {
          operator: "divide",
          inputs: [
            { id: "payouts.amount", aggregation: "sum" },
            { id: "donations.amount", aggregation: "sum" },
          ],
        },
      },
    ],
  };
}
