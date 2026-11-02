export function CampaignDetails() {
  const goalAmount = 25000;
  const currentRaised = 16840;
  const donorCount = 214;
  const percent = Math.min(Math.round((currentRaised / goalAmount) * 100), 100);

  return (
    <div className="campaign-card">
      <div className="badge-row">
        <span className="category-badge">Emergency Medical Care</span>
        <span className="verified-badge">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          Hospital Verified
        </span>
      </div>

      <h1 className="campaign-title">Critical Pediatric Surgery & Intensive Care</h1>

      <p className="campaign-desc">
        Every contribution directly funds specialized surgical interventions, pediatric intensive care,
        and post-operative medication for children from underserved families. All disbursements are verified
        and paid directly to healthcare providers.
      </p>

      <div className="progress-section">
        <div className="progress-header">
          <div className="amount-raised">${currentRaised.toLocaleString()}</div>
          <div className="amount-goal">pledged of ${goalAmount.toLocaleString()} goal</div>
        </div>

        <div className="progress-bar-track">
          <div className="progress-bar-fill" style={{ width: `${percent}%` }} />
        </div>

        <div className="progress-stats">
          <span className="stat-item">
            <strong>{percent}%</strong> funded
          </span>
          <span className="stat-item">
            <strong>{donorCount}</strong> verified donors
          </span>
          <span className="stat-item">
            <strong>12 days</strong> remaining
          </span>
        </div>
      </div>

      <div className="features-list">
        <div className="feature-item">
          <div className="feature-icon-wrap">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div className="feature-content">
            <h4>100% Direct Medical Payouts</h4>
            <p>Funds never route through intermediary accounts. Verified hospital invoices are settled directly via PayPal.</p>
          </div>
        </div>

        <div className="feature-item">
          <div className="feature-icon-wrap">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
          </div>
          <div className="feature-content">
            <h4>Instant Donation Confirmation</h4>
            <p>Immediate transaction receipt and real-time ledger tracking on the Hope platform.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
