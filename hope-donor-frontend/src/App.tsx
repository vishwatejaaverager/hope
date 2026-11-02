import { CampaignDetails } from "./components/CampaignDetails";
import { DonationForm } from "./components/DonationForm";

export default function App() {
  return (
    <>
      <header className="app-header">
        <a href="/" className="brand-lockup">
          <div className="brand-dot" />
          <span className="brand-name">Hope</span>
          <span className="brand-tag">Medical Relief</span>
        </a>

        <div className="header-meta">
          <div className="sandbox-pill">
            <span className="sandbox-dot" />
            <span>Sandbox Mode</span>
          </div>
        </div>
      </header>

      <main className="main-container">
        <CampaignDetails />
        <DonationForm />
      </main>

      <footer className="app-footer">
        <p>
          Hope Transparent Medical Crowdfunding Platform · All donations are settled directly via PayPal Sandbox
          without intermediary fee deduction.
        </p>
      </footer>
    </>
  );
}
