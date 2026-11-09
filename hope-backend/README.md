# Hope Backend – PayPal Sandbox Checkout

FastAPI backend + static donation page using the official PayPal JS SDK (USD, Sandbox).

## Setup

```bash
cd hope-backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in Sandbox credentials (skip if .env exists)
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000/donate**. Health check: `GET /`. API docs: `/docs`.

## Payment flow

1. Page fetches `GET /api/payments/config` (public client ID) and loads the PayPal SDK.
2. Button click → `createOrder` → `POST /api/payments/create-order` → backend creates an order via PayPal Orders v2 → returns order ID.
3. Buyer approves in the PayPal popup → `onApprove` → `POST /api/payments/capture-order/{id}`.
4. Backend captures and returns the real capture status, transaction ID and amount. The UI shows success only if `success: true` (order and capture both `COMPLETED`).

Duplicate captures use a deterministic `PayPal-Request-Id`; an `ORDER_ALREADY_CAPTURED` error triggers a `GET` of the order's real state instead of a blind retry.

## Testing

1. Start the server, open `/donate`.
2. Click **$5**, then the PayPal button.
3. Log in with your **Personal** Sandbox buyer account and approve.
4. Page shows `Status: COMPLETED` with a transaction ID. Verify in the Business sandbox account at https://www.sandbox.paypal.com.
5. Cancel: close the PayPal popup → "Payment cancelled".
6. Failure: enter `0` or `-5` (blocked with an error); use a wrong `.env` secret and restart (checkout shows an error); or use the Sandbox "Negative testing" tools in the PayPal developer dashboard.

## Notes

- Sandbox and Live are separated purely by `.env` (`PAYPAL_BASE_URL`, credentials). Use HTTPS in production.
- Only USD is accepted (INR returned `CURRENCY_NOT_SUPPORTED`).
- No database, campaigns, payouts, or webhooks yet; the in-memory token cache is per-process.

## Database (Render PostgreSQL)

SQLAlchemy 2.0 + Psycopg 3 + Alembic. Local dev uses `DATABASE_URL_EXTERNAL`; on Render (where the `RENDER` env var is set) `DATABASE_URL_INTERNAL` is used. A plain `DATABASE_URL` is accepted as a fallback.

```bash
alembic upgrade head   # run all database migrations (donations, payouts)
```

- **Donations (`donations` table):** `create-order` creates the order; `capture-order` captures via PayPal and persists the confirmed transaction.
- **Payouts (`payouts` table):**
  - `POST /api/payouts/create`: initiates an outbound PayPal Sandbox payout and stores the initial record (batch status, item id, amount, recipient).
  - `GET /api/payouts/{batch_id}`: queries PayPal and updates the stored record. Only marked `paid: true` when PayPal confirms item status is `SUCCESS`.
  - `GET /api/payouts/{id}`: when passed a UUID, returns the persisted payout record from the database.
  - `GET /api/payouts/history`: lists all persisted payouts, newest first (supports `limit` and `offset` pagination).

## Running Tests

```bash
pytest -v tests/
```


## Approved-case email and payout workflow

Run `alembic upgrade head` before starting the updated backend. The migration adds
`cases.paypal_email` and a unique case link on payouts; contact email remains separate.

- Approval (email triage or the case API) asks the contact for the beneficiary's
  PayPal email if it has not been explicitly supplied.
- A reply such as `My PayPal email is beneficiary@example.com` saves it. A bare
  email address is accepted when replying to the request for PayPal details.
- With approval, a confirmed PayPal email and a positive USD `requested_amount`,
  the workflow automatically submits that amount. It never substitutes the total
  hospital estimate for the assistance amount.
- Each case reserves one payout with frozen recipient/amount and a stable PayPal
  request ID. Retries reuse it. Pending payments remain `payout_processing`;
  only PayPal item `SUCCESS` marks the case `disbursed`.
- Follow-up emails or the case disbursement endpoint reconcile the existing payout.
  This does not add a scheduled payment-status poller.
- Approval updates use SMTP when configured, otherwise the configured Zapier hook;
  undelivered messages remain in the outgoing queue.
- OpenRouter replies are conversational without internal status reports. Missing
  keys/provider failures use a labelled heuristic fallback in the outgoing email's
  metadata. The fallback cannot verify documents or automatically approve a case.

Existing paid cases without a case-linked payout require manual reconciliation;
this migration intentionally does not infer historical payment links.
