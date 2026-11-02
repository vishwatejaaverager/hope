import { useState } from "react";
import { CampaignDetails } from "./components/CampaignDetails";
import { DonationForm } from "./components/DonationForm";
import { PaymentSuccessModal } from "./components/PaymentSuccessModal";
import type { CaptureOrderResponse } from "./services/api";

export default function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [successPayment, setSuccessPayment] = useState<CaptureOrderResponse | null>(null);

  function handlePaymentSuccess(result: CaptureOrderResponse) {
    // 1. Immediately increment trigger so CampaignDetails re-fetches the live donation count
    setRefreshTrigger((prev) => prev + 1);
    // 2. Open the celebratory success dialog with animations
    setSuccessPayment(result);
  }

  function handleCloseModal() {
    setSuccessPayment(null);
  }

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
        <CampaignDetails refreshTrigger={refreshTrigger} />
        <DonationForm onPaymentSuccess={handlePaymentSuccess} />
      </main>

      {/* Cool Celebration Payment Status Dialog */}
      {successPayment && (
        <PaymentSuccessModal payment={successPayment} onClose={handleCloseModal} />
      )}

      <footer className="app-footer">
        <p>
          Hope Transparent Medical Crowdfunding Platform · All donations are settled directly via PayPal Sandbox
          without intermediary fee deduction.
        </p>
      </footer>
    </>
  );
}
