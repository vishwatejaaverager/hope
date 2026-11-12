# Hope

Hope helps people apply for medical financial assistance by email. It gives reviewers one place to see the application, supporting documents, and follow-up conversation. The donor portal uses PayPal Sandbox for test donations, and the backend integrates sandbox payouts for approved cases.

## Inspiration

I went to the hospital with a friend, and we couldn’t arrange the money we needed. I knew of NGOs that could help, but finding out what they required, gathering documents, and following up took time while we were already worried about treatment. That experience inspired Hope. An applicant can start with an ordinary email and get a reply that tells them what to do next.

## How Hope works

1. **Apply by email.** An applicant describes their request and sends supporting documents such as a medical report, a hospital estimate, and an ID.
2. **Review the evidence.** Hope uses AI to help identify missing information and inconsistencies and draft a follow-up. Replies and attachments stay with the case so reviewers can follow what changed.
3. **Send corrections in the same thread.** An applicant can submit a corrected estimate or another missing document without starting over. Reviewers can inspect the case and its document history in the admin dashboard.
4. **Collect the payout address after approval.** Hope asks for the beneficiary’s PayPal email when needed. The payout uses the approved assistance amount, which can differ from the hospital estimate.
5. **Track the payout.** The backend stores the PayPal reference and checks the payout item status. The case is marked disbursed when PayPal confirms success.

Donors use a separate checkout flow. The backend creates the order, captures it after buyer approval, and records the confirmed transaction.

## Hackathon technology requirement

Hope integrates the **free PayPal Sandbox** with **AI models through OpenRouter**.

| Tool | Role in Hope |
| --- | --- |
| PayPal Sandbox | Supplies test buyer and business accounts for development and demonstrations. |
| PayPal JavaScript SDK | Presents PayPal Checkout to the donor. |
| PayPal Orders v2 API | Creates, retrieves, and captures donation orders. |
| PayPal Payouts API | Submits beneficiary payouts and retrieves their status. |
| PayPal OAuth 2.0 | Authenticates backend API requests using the configured sandbox credentials. |
| OpenRouter | Gives the backend one API for calling the configured AI models. |
| Google Gemini 3 Flash Preview | Primary model for reviewing application emails and supporting documents. AI also helps draft applicant follow-ups. |
| OpenAI GPT-4.1 mini and Google Gemini 3.1 Flash Lite Preview | Configured fallback models for document analysis when the primary model is unavailable. |

## Repository layout

| Directory | Stack and purpose |
| --- | --- |
| [hope-backend](hope-backend/) | Python, FastAPI, SQLAlchemy, PostgreSQL, and Alembic. Handles email intake, case tracking, AI review, checkout, and payouts. |
| [hope-donor-frontend](hope-donor-frontend/) | React, TypeScript, and Vite. Donor portal. |
| [hope-admin-dashboard](hope-admin-dashboard/) | Next.js, React, TypeScript, Tailwind CSS, and AG Grid / AG Studio. Reviewer dashboard. |

## Run locally

You’ll need Python, Node.js with npm, a PostgreSQL database, PayPal Sandbox app credentials, and an OpenRouter API key for AI review. Use synthetic documents for demos.

### Backend

```bash
cd hope-backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
```

Fill in the database URL and the PayPal and OpenRouter settings in `.env`. Keep `PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com` and use credentials from your sandbox app. Configure email intake and delivery if you want to test through a mailbox. See the [backend guide](hope-backend/README.md) for configuration and API details.

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The backend exposes interactive API docs at `http://127.0.0.1:8000/docs` and a standalone donation page at `http://127.0.0.1:8000/donate`.

### Donor portal and dashboard

Run each frontend in its own terminal from the repository root.

```bash
cd hope-donor-frontend
npm ci
VITE_API_URL=http://127.0.0.1:8000 npm run dev
```

```bash
cd hope-admin-dashboard
npm ci
cp -n .env.example .env.local
npm run dev
```

Set `HOPE_BACKEND_URL=http://127.0.0.1:8000` in the dashboard’s `.env.local` and fill in the dashboard settings described in its [setup guide](hope-admin-dashboard/README.md).

### Streamlit review interface

From `hope-backend`, with the virtual environment active:

```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_review.py
```

## Suggested judging walkthrough

1. Submit a sample application with an incomplete set of documents. Show the follow-up asking for the missing evidence.
2. Reply with the missing documents or a corrected estimate. Open the dashboard to show how the same case retains the conversation and review history.
3. Show an approved sandbox case receiving a request for the beneficiary’s PayPal email. Follow the payout status through to the status PayPal reports.
4. Open the donor portal, approve a small test donation using a personal PayPal Sandbox account, and show the capture status and transaction ID.

Run the backend test suite from `hope-backend` with `python -m pytest -q`.

## What we learned

Applications rarely arrive complete. Someone might send a report first, an ID later, and a corrected estimate after that. Keeping those submissions attached to the same case makes it easier to ask for the right next document and explain what changed. AI helps surface discrepancies, and the case history gives reviewers the context to evaluate them.

Next, we want to pilot Hope with NGOs, support more languages, and improve how it handles unclear documents and communicates case progress.
