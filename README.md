# Hope – Medical Crowdfunding Platform

Hope is a transparent medical crowdfunding platform providing direct donor-to-beneficiary support with verified payouts.

## Repository Structure

```text
hope/
├── hope-backend/                 # FastAPI backend (PayPal Orders & Payouts, PostgreSQL DB)
├── hope-donor-frontend/          # Donor-facing web application (React + TypeScript + Vite)
├── hope-admin-dashboard/         # AG Studio admin dashboard (React + TypeScript + Vite)
├── .gitignore                    # Global gitignore (Python, Node, OS)
└── README.md                     # Root project documentation
```

## Subprojects

- **`hope-backend/`**: FastAPI REST API handling PayPal Sandbox authentication, order creation, payment capture, and beneficiary payouts with Render PostgreSQL persistence.
- **`hope-donor-frontend/`**: Donor-facing application for discovering campaigns and making secure medical donations.
- **`hope-admin-dashboard/`**: Administration interface for campaign management and verification workflows.
