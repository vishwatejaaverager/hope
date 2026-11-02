import { useState } from "react";
import type { CaptureOrderResponse } from "../services/api";

interface PaymentSuccessModalProps {
  payment: CaptureOrderResponse;
  onClose: () => void;
}

export function PaymentSuccessModal({ payment, onClose }: PaymentSuccessModalProps) {
  const [copied, setCopied] = useState(false);

  const txId = payment.transaction_id || payment.order_id;

  function copyTransactionId() {
    if (!txId) return;
    navigator.clipboard.writeText(txId).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  }

  // Pre-generate confetti pieces with deterministic styles
  const confettiPieces = Array.from({ length: 32 }, (_, i) => {
    const left = (i * 3.125) % 100;
    const delay = ((i * 137) % 2000) / 1000;
    const duration = 2.5 + ((i * 73) % 1500) / 1000;
    const colors = ["#14b8a6", "#6366f1", "#10b981", "#fbbf24", "#38bdf8", "#f43f5e", "#a855f7"];
    const color = colors[i % colors.length];
    const size = 6 + (i % 8);
    const isCircle = i % 2 === 0;

    return {
      id: i,
      style: {
        left: `${left}%`,
        animationDelay: `${delay}s`,
        animationDuration: `${duration}s`,
        backgroundColor: color,
        width: `${size}px`,
        height: isCircle ? `${size}px` : `${size * 1.8}px`,
        borderRadius: isCircle ? "50%" : "2px",
      },
    };
  });

  return (
    <div className="modal-backdrop" onClick={onClose} role="dialog" aria-modal="true" aria-labelledby="modal-title">
      {/* Confetti Celebration Shower */}
      <div className="confetti-container" aria-hidden="true">
        {confettiPieces.map((piece) => (
          <div key={piece.id} className="confetti-piece" style={piece.style} />
        ))}
      </div>

      <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
        {/* Close Button */}
        <button type="button" className="modal-close-btn" onClick={onClose} aria-label="Close dialog">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>

        {/* Animated Checkmark Badge with Pulse Aura */}
        <div className="modal-badge-wrapper">
          <div className="modal-pulse-ring" />
          <div className="modal-pulse-ring delay" />
          <div className="modal-badge-icon">
            <svg
              className="checkmark-svg"
              width="40"
              height="40"
              viewBox="0 0 48 48"
              fill="none"
              stroke="currentColor"
              strokeWidth="4"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <polyline className="checkmark-path" points="14 25 21 32 34 17" />
            </svg>
          </div>
        </div>

        {/* Header Texts */}
        <div className="modal-header-section">
          <span className="modal-pill-tag">Verified Medical Contribution</span>
          <h2 id="modal-title" className="modal-headline">
            Donation Confirmed! 🎉
          </h2>
          <p className="modal-subtext">
            Thank you! Your donation was securely captured by PayPal and recorded on the Hope transparent ledger.
          </p>
        </div>

        {/* Amount Card */}
        <div className="modal-amount-banner">
          <span className="modal-amount-label">Contributed Amount</span>
          <div className="modal-amount-number">
            ${payment.amount || "0.00"}{" "}
            <span className="modal-amount-currency">{payment.currency || "USD"}</span>
          </div>
        </div>

        {/* Detailed Receipt Card */}
        <div className="modal-receipt-box">
          <div className="modal-receipt-row">
            <span className="receipt-col-label">Status</span>
            <span className="receipt-status-pill">
              <span className="status-dot-pulse" />
              {payment.capture_status || "COMPLETED"}
            </span>
          </div>

          <div className="modal-receipt-row">
            <span className="receipt-col-label">PayPal Tx ID</span>
            <div className="receipt-copy-wrapper">
              <span className="receipt-code mono">{txId}</span>
              <button
                type="button"
                className="copy-btn"
                onClick={copyTransactionId}
                title="Copy Transaction ID"
              >
                {copied ? (
                  <span className="copied-text">Copied!</span>
                ) : (
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                  </svg>
                )}
              </button>
            </div>
          </div>

          <div className="modal-receipt-row">
            <span className="receipt-col-label">Order Ref</span>
            <span className="receipt-code mono">{payment.order_id}</span>
          </div>

          <div className="modal-receipt-row">
            <span className="receipt-col-label">Allocation</span>
            <span className="receipt-value-highlight">Direct to Beneficiary Fund</span>
          </div>
        </div>

        {/* Actions */}
        <div className="modal-actions-group">
          <button type="button" className="btn-modal-primary" onClick={onClose}>
            Make Another Donation
          </button>
        </div>
      </div>
    </div>
  );
}
