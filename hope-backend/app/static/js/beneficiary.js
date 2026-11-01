(function () {
  const form = document.getElementById("payout-form");
  const nameInput = document.getElementById("name");
  const emailInput = document.getElementById("email");
  const amountInput = document.getElementById("amount");
  const formError = document.getElementById("form-error");
  const submitBtn = document.getElementById("submit-btn");
  const statusBox = document.getElementById("status");
  const statusTitle = document.getElementById("status-title");
  const statusBody = document.getElementById("status-body");
  const spinner = document.getElementById("status-spinner");

  const POLL_MS = 3000;
  const MAX_POLLS = 20; // ~1 minute

  function showStatus(kind, title, body, loading) {
    statusBox.hidden = false;
    statusBox.className = "status " + kind;
    statusTitle.textContent = title;
    statusBody.textContent = body || "";
    spinner.hidden = !loading;
  }

  async function api(path, options) {
    const res = await fetch(path, options);
    let data = {};
    try { data = await res.json(); } catch (_) {}
    if (!res.ok) {
      const d = data.detail;
      const msg = typeof d === "string" ? d
        : Array.isArray(d) ? d.map((x) => x.msg.replace(/^Value error, /, "")).join("; ")
        : "Request failed (" + res.status + ")";
      throw new Error(msg);
    }
    return data;
  }

  function describe(r) {
    return "Batch ID: " + r.batch_id + " · Batch status: " + r.batch_status +
      " · Item status: " + (r.item_status || "—") +
      (r.amount ? " · " + r.amount + " " + r.currency : "") +
      (r.error ? " · " + r.error : "");
  }

  function render(r) {
    if (r.paid) showStatus("success", "Payout successful 🎉", r.message + "\n" + describe(r), false);
    else if (r.final) showStatus("failure", "Payout not completed", r.message + "\n" + describe(r), false);
    else showStatus("info", "Payout processing…", describe(r), true);
  }

  async function poll(batchId) {
    for (let i = 0; i < MAX_POLLS; i++) {
      await new Promise((r) => setTimeout(r, POLL_MS));
      try {
        const r = await api("/api/payouts/" + encodeURIComponent(batchId));
        render(r);
        if (r.final) return;
      } catch (err) {
        showStatus("failure", "Could not check payout status", err.message + " (Batch ID: " + batchId + ")");
        return;
      }
    }
    showStatus("info", "Still processing", "PayPal has not given a final status yet. Batch ID: " + batchId);
  }

  function validate() {
    let msg = "";
    const amount = amountInput.value.trim();
    if (!nameInput.value.trim()) msg = "Enter the beneficiary's name.";
    else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(emailInput.value.trim())) msg = "Enter a valid PayPal recipient email.";
    else if (!/^\d+(\.\d{1,2})?$/.test(amount) || Number(amount) <= 0) msg = "Enter a valid amount (up to 2 decimals).";
    formError.hidden = !msg;
    formError.textContent = msg;
    return !msg;
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    if (!validate()) return;
    submitBtn.disabled = true;
    showStatus("info", "Requesting payout…", "", true);
    try {
      const r = await api("/api/payouts/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          beneficiary_name: nameInput.value.trim(),
          email: emailInput.value.trim(),
          amount: amountInput.value.trim(),
        }),
      });
      render(r);
      if (!r.final) await poll(r.batch_id);
    } catch (err) {
      showStatus("failure", "Payout request failed", err.message);
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
