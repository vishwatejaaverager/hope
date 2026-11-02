import { useState, type ChangeEvent } from "react";
import { PayPalButton } from "./PayPalButton";
import { CaptureOrderResponse } from "../services/api";

const PRESET_AMOUNTS = ["5", "10", "25", "50"];

interface StatusState {
  visible: boolean;
  kind: "info" | "success" | "failure";
  title: string;
  body?: string;
  loading?: boolean;
}

interface DonationFormProps {
  onPaymentSuccess?: (result: CaptureOrderResponse) => void;
}

export function DonationForm({ onPaymentSuccess }: DonationFormProps) {
  const [amount, setAmount] = useState<string>("5");
  const [completedPayment, setCompletedPayment] = useState<CaptureOrderResponse | null>(null);
  const [status, setStatus] = useState<StatusState>({
    visible: false,
    kind: "info",
    title: "",
  });

  // Validation function matching checkout.js
  function validateAmount(val: string): string | null {
    const raw = val.trim();
    const n = Number(raw);
    if (!raw || !isFinite(n) || n <= 0) {
      return "Enter an amount greater than $0.";
    }
    if (!/^\d+(\.\d{1,2})?$/.test(raw)) {
      return "Use at most 2 decimal places.";
    }
    if (n < 1) {
      return "Minimum donation is $1.";
    }
    if (n > 10000) {
      return "Maximum donation is $10,000.";
    }
    return null;
  }

  const validationError = validateAmount(amount);
  const isValid = validationError === null;

  function handlePresetClick(preset: string) {
    setAmount(preset);
    if (status.visible && status.kind === "failure") {
      setStatus({ visible: false, kind: "info", title: "" });
    }
  }

  function handleCustomChange(e: ChangeEvent<HTMLInputElement>) {
    setAmount(e.target.value);
    if (status.visible && status.kind === "failure") {
      setStatus({ visible: false, kind: "info", title: "" });
    }
  }

  function handleStatusChange(
    kind: "info" | "success" | "failure",
    title: string,
    body?: string,
    loading?: boolean
  ) {
    if (!title && !body) {
      setStatus({ visible: false, kind: "info", title: "" });
    } else {
      setStatus({ visible: true, kind, title, body, loading });
    }
  }

  function handleSuccess(result: CaptureOrderResponse) {
    setCompletedPayment(result);
    onPaymentSuccess?.(result);
  }

  function handleReset() {
    setCompletedPayment(null);
    setAmount("5");
    setStatus({ visible: false, kind: "info", title: "" });
  }

  // Once payment is completed, display the verified receipt view
  if (completedPayment) {
    return (
      <div className="donation-card">
        <div className="receipt-card">
          <div className="receipt-icon-circle">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>

          <h2 className="receipt-title">Thank You for Your Donation!</h2>
          <p className="receipt-subtitle">
            Your generous contribution has been securely processed and recorded on the Hope ledger.
          </p>

          <div className="receipt-details-table">
            <div className="receipt-row">
              <span className="receipt-row-label">Amount Donated</span>
              <span className="receipt-row-value">
                ${completedPayment.amount} {completedPayment.currency}
              </span>
            </div>

            <div className="receipt-row">
              <span className="receipt-row-label">Payment Status</span>
              <span className="receipt-row-value" style={{ color: "#34d399" }}>
                {completedPayment.capture_status || "COMPLETED"}
              </span>
            </div>

            <div className="receipt-row">
              <span className="receipt-row-label">PayPal Transaction ID</span>
              <span className="receipt-row-value mono">
                {completedPayment.transaction_id || completedPayment.order_id}
              </span>
            </div>

            <div className="receipt-row">
              <span className="receipt-row-label">Order Reference</span>
              <span className="receipt-row-value mono">{completedPayment.order_id}</span>
            </div>
          </div>

          <button type="button" className="btn-reset" onClick={handleReset}>
            Make Another Donation
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="donation-card">
      <div className="donation-card-header">
        <h2 className="donation-card-title">Choose Donation Amount</h2>
        <p className="donation-card-sub">Secure checkout powered by PayPal Sandbox.</p>
      </div>

      {/* Preset Buttons */}
      <div className="presets-group">
        <label className="section-label">Select Amount (USD)</label>
        <div className="presets-grid" role="group" aria-label="Preset donation amounts">
          {PRESET_AMOUNTS.map((preset) => (
            <button
              key={preset}
              type="button"
              className={`preset-chip ${amount === preset ? "active" : ""}`}
              onClick={() => handlePresetClick(preset)}
            >
              ${preset}
            </button>
          ))}
        </div>
      </div>

      {/* Custom Amount Input */}
      <div className="amount-input-wrapper">
        <label htmlFor="custom-amount" className="section-label">
          Or Enter Custom Amount
        </label>
        <div className={`amount-input-box ${validationError ? "has-error" : ""}`}>
          <span className="currency-symbol">$</span>
          <input
            id="custom-amount"
            type="number"
            inputMode="decimal"
            min="1"
            max="10000"
            step="0.01"
            placeholder="5.00"
            value={amount}
            onChange={handleCustomChange}
            className="amount-input"
          />
          <span className="currency-tag">USD</span>
        </div>
        {validationError && (
          <p className="error-message" role="alert">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="12" y1="8" x2="12" y2="12" />
              <line x1="12" y1="16" x2="12.01" y2="16" />
            </svg>
            {validationError}
          </p>
        )}
      </div>

      {/* PayPal Smart Buttons Container */}
      <PayPalButton
        amount={amount}
        currency="USD"
        isValid={isValid}
        onStatusChange={handleStatusChange}
        onSuccess={handleSuccess}
      />

      {/* Real-time Status Card */}
      {status.visible && (
        <div className={`status-box ${status.kind}`} role="alert" aria-live="polite">
          <div className="status-header-row">
            {status.loading && <div className="spinner-ring" />}
            <span>{status.title}</span>
          </div>
          {status.body && <p className="status-detail-text">{status.body}</p>}
        </div>
      )}
    </div>
  );
}
