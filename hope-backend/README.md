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

On Render, the backend automatically runs `alembic upgrade head` against its own
database connection before accepting requests. No Shell access or start-command
change is needed. Locally, run `alembic upgrade head` before starting the backend,
or set `AUTO_MIGRATE=1`. The migration adds
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
- OpenRouter replies are conversational without internal status reports. If every
  configured model attempt fails (or no API key is configured), the applicant gets
  a review-failure notice through the normal email transport. Existing evidence
  and case decisions are preserved; that attempt cannot trigger a payout. The
  outgoing email records `analysis_status=failed` and an internal failure reason.
  No automatic retry job is implied; the notice asks for a later retry with the
  relevant documents. Heuristic analysis is retained only for explicit test mode.

Existing paid cases without a case-linked payout require manual reconciliation;
this migration intentionally does not infer historical payment links.

Startup logs `Database migrations committed successfully` after the transaction
commits. Connection attempts are bounded to 10 seconds, lock waits to 5 seconds,
and individual migration statements to 60 seconds. Migration failures stop startup
instead of serving requests with missing columns. Simultaneous migration runners
use a PostgreSQL advisory lock. Unknown database revisions fail explicitly; they
are never silently skipped or stamped.

## Automatic document approval checks

The required set is the patient's government-issued photo ID (`government_id`),
a hospital treatment estimate or bill (`cost_estimate`), and a current medical
report or doctor's treatment recommendation (`medical_record`). AI reads each
attachment and reviews the entire case for red flags, including issues not
listed in a fixed checklist. Each document gets a status, supporting excerpt,
reason and red flags. The backend records separate `approved`, `needs_review`,
or `missing` fields in `review_report.document_statuses`, exposed in the case
API and dashboard. Missing or incomplete review results cannot grant approval.

Case approval requires all three document fields to be approved, a complete AI
review, an approval recommendation, an evidence-based explanation, and no
unresolved red flags. Previously reviewed documents persist across replies;
a replacement of the same document type is reviewed again. An approved document
alone does not approve the entire case. The review report, model, findings and
email draft are stored; payment instructions reflect the backend payment state.
Existing legacy document-check approvals retain their evidence and validity
guards; explicit reviewer approvals remain supported.

These reviews assess completeness and consistency. External issuer/identity
verification is not implemented; AI cannot prove document authenticity.

## Paid analysis model routing

Document analysis now tries these paid vision models in order:

1. `google/gemini-3-flash-preview`
2. `openai/gpt-4.1-mini`
3. `google/gemini-3.1-flash-lite-preview`

`OPENROUTER_MODEL` can prioritize one of those three without duplicating attempts.
Old free-model or unsupported overrides are ignored with a warning. Each request
uses JSON output and a 4,096-token completion cap; Gemini uses minimal reasoning
effort. The existing OpenRouter API key and account credits are used. If all three
attempts fail, the applicant receives the existing analysis-failure notice.

The incoming-email handler runs in FastAPI's synchronous worker pool because it
uses blocking AI, payment, and SMTP clients. This leaves the event loop available
for vision providers to fetch attachment URLs from the same Uvicorn process while
analysis is in progress. Attachment downloads also keep blocking database reads
out of the event loop.

## Attachment delivery and dashboard visibility

Incoming email lists merge attachment metadata with files saved under the same
Message-ID, so the dashboard can display existing binary files even if an earlier
webhook omitted attachment metadata. A duplicate webhook enriches attachment data
without repeating analysis, emails, or payouts. IMAP also attaches missing files
to an email already created by Zapier instead of skipping the whole message, and
reuses previously saved files when retried.

This does not retrieve historical files that were never saved: IMAP still reads
unread mail, and a Zapier-only delivery must include attachment fields. Resend
missing documents in a new email if they are no longer available to the reader.

When IMAP is configured, a text-only external webhook is now saved with
`intake_status=awaiting_mailbox` and acknowledged with HTTP 202. It does not run
analysis or send a premature missing-attachment reply. The mailbox reader saves
the actual MIME files, resumes the queued email once, and records it as processed.
Pending Message-IDs are searched explicitly even if another mail client marked
them read. This targeted recovery does not scan or analyze the whole historical
mailbox. IMAP connection/read operations have a 20-second socket timeout.

Legacy automatic document evidence must explicitly record validity conditions.
The legacy evidence guard rechecks expiry before new payouts. New AI reviews
inspect dates and validity in context and store their findings in the review
report. No existing payout is repeated by either review path.

## Continued document-review conversations

`documents` stores one UUID primary key per attachment, with a foreign key to
its incoming email and case. The email ID is not the document primary key: one
email may contain several attachments. Rows retain file metadata, extracted
facts, verification status, explanation, and whether the version is current.
`case_reviews` stores an immutable report and draft for each reviewed email.
Cases and source documents are committed before contacting OpenRouter; an
interrupted `review_pending` intake can resume using the same IDs. Existing
email metadata and reports are materialized into these tables when their case
next receives a review. Previous snapshots are never rewritten by a follow-up.

Case references and RFC `In-Reply-To`/`References` identify conversations. Sender
email is used only when exactly one case matches; neither a name nor the latest
case for a shared contact silently joins two patients. IMAP forwards thread
headers. Zapier integrations should map `in_reply_to` and `references` when
available, or retain the case reference in the subject/body.

Every new analysis receives the case summary, stored document findings, prior
review and unresolved red flags, recent incoming/outgoing messages, and the new
email/attachments. Approved older files reuse their findings. The AI must check
new evidence for additional concerns as well as revisit earlier concerns.

Red flags have stable IDs. Omitting an old flag cannot resolve it. A
`resolved_red_flags` entry must name the flag ID, explain the resolution, and
reference a new readable attachment or an exact excerpt of the current email.
Quoted history is not new confirmation. The backend validates the reference;
the model assesses whether the evidence actually addresses the concern.
`previous_document_updates` can reopen an older document, or resolve its review
with supported new evidence. Contradictions can identify affected document
sources so previously approved documents become `needs_review`. Backend-computed
missing-document notices are refreshed as the current document set changes.
An expired estimate may therefore be resolved by a replacement while a new
patient-name mismatch keeps the case under review.

Only readable content actually supplied to the model can support a new document
approval. PDF text extraction uses `pypdf`; scanned PDFs without readable text
need a readable image or additional extraction. At most four image inputs are
sent per review; excess images cannot be silently marked reviewed. No new payout
is created while a linked submission is `review_pending`. A failed follow-up
suspends automatic approval without deleting prior document findings.

The authenticated case-detail API returns `documents` and chronological
`reviews`. Incoming-email lists expose each email's `review_report`. The admin
dashboard shows current open/resolved concerns and each email's review findings.

When all three required documents pass, no review concerns remain, and a USD
assistance amount is recorded, Hope asks the case contact for the beneficiary's
PayPal email. Reply in the same thread with just the address or
`PayPal email: beneficiary@example.com`. The hospital estimate alone does not
set the assistance amount. A payout is submitted at most once per case.
Pending PayPal batches are checked periodically when PayPal credentials are
configured. On confirmed success, Hope emails the amount, recipient, and
available PayPal batch, item, and transaction IDs. No success email is sent for
an unconfirmed payment. Render requires a configured `EMAIL_WEBHOOK_SECRET`
matching the inbound integration.
