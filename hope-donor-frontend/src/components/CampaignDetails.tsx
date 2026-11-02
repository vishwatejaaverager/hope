import { useEffect, useState } from "react";
import { getDonationSummary, type DonationSummary } from "../services/api";

interface CampaignDetailsProps {
  refreshTrigger?: number;
}

export function CampaignDetails({ refreshTrigger = 0 }: CampaignDetailsProps) {
  const [summary, setSummary] = useState<DonationSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let active = true;
    getDonationSummary()
      .then((s) => active && setSummary(s))
      .catch(() => active && setFailed(true))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, [refreshTrigger]);

  const rawRaised = summary ? Number(summary.total_raised) : null;
  const raised = rawRaised !== null && !isNaN(rawRaised) ? rawRaised : null;

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

      <div className="progress-section" aria-busy={loading}>
        {loading ? (
          <div className="skeleton-wrap" role="status" aria-label="Loading donation totals">
            <div className="skeleton skeleton-amount" />
            <div className="skeleton skeleton-line" />
            <span className="skeleton-caption">
              <span className="spinner-ring" /> Fetching live totals…
            </span>
          </div>
        ) : (
          <>
            <div className="progress-header">
              <div className="amount-raised">
                {raised === null
                  ? "—"
                  : `$${raised.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
              </div>
              <div className="amount-goal">raised so far</div>
            </div>

            <div className="progress-stats">
              <span className="stat-item">
                <strong>{summary ? summary.donation_count : "—"}</strong>{" "}
                {summary?.donation_count === 1 ? "donation" : "donations"} received
              </span>
            </div>
            {failed && <p className="status-detail-text">Live totals are unavailable right now.</p>}
          </>
        )}
      </div>
    </div>
  );
}
