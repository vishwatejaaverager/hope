import { useEffect, useState } from "react";
import { getDonationSummary, type DonationSummary } from "../services/api";

export function CampaignDetails() {
  const [summary, setSummary] = useState<DonationSummary | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let active = true;
    getDonationSummary()
      .then((s) => active && setSummary(s))
      .catch(() => active && setFailed(true));
    return () => {
      active = false;
    };
  }, []);

  const raised = summary ? Number(summary.total_raised) : null;

  return (
    <div className="campaign-card">
      <div className="badge-row">
        <span className="category-badge">Medical Support</span>
      </div>

      <h1 className="campaign-title">Support a Medical Treatment</h1>

      <p className="campaign-desc">
        Every contribution helps a patient get the care they need. Donations are processed securely
        by PayPal and recorded on the Hope ledger. This is a sandbox environment, so no real money
        is moved.
      </p>

      <div className="progress-section">
        <div className="progress-header">
          <div className="amount-raised">
            {raised === null ? (failed ? "—" : "…") : `$${raised.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
          </div>
          <div className="amount-goal">raised so far</div>
        </div>

        <div className="progress-stats">
          <span className="stat-item">
            <strong>{summary ? summary.donation_count : failed ? "—" : "…"}</strong>{" "}
            {summary?.donation_count === 1 ? "donation" : "donations"} received
          </span>
        </div>
        {failed && <p className="status-detail-text">Live totals are unavailable right now.</p>}
      </div>
    </div>
  );
}
