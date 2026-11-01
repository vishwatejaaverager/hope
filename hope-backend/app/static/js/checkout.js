(function () {
  const amountInput = document.getElementById("amount");
  const amountError = document.getElementById("amount-error");
  const presets = document.querySelectorAll(".preset");
  const statusBox = document.getElementById("status");
  const statusTitle = document.getElementById("status-title");
  const statusBody = document.getElementById("status-body");
  const spinner = document.getElementById("status-spinner");

  function showStatus(kind, title, body, loading) {
    statusBox.hidden = false;
    statusBox.className = "status " + kind;
    statusTitle.textContent = title;
    statusBody.textContent = body || "";
    spinner.hidden = !loading;
  }

  function syncPresets() {
    presets.forEach((p) => p.classList.toggle("active", p.dataset.amount === amountInput.value));
  }

  function validAmount() {
    const raw = amountInput.value.trim();
    const n = Number(raw);
    let msg = "";
    if (!raw || !isFinite(n) || n <= 0) msg = "Enter an amount greater than $0.";
    else if (!/^\d+(\.\d{1,2})?$/.test(raw)) msg = "Use at most 2 decimal places.";
    else if (n < 1) msg = "Minimum donation is $1.";
    else if (n > 10000) msg = "Maximum donation is $10,000.";
    amountError.hidden = !msg;
    amountError.textContent = msg;
    return msg ? null : raw;
  }

  presets.forEach((p) =>
    p.addEventListener("click", () => {
      amountInput.value = p.dataset.amount;
      amountError.hidden = true;
      syncPresets();
    })
  );
  amountInput.addEventListener("input", syncPresets);
  syncPresets();

  async function api(path, options) {
    const res = await fetch(path, options);
    let data = {};
    try { data = await res.json(); } catch (_) {}
    if (!res.ok) {
      const d = data.detail;
      const msg = typeof d === "string" ? d
        : Array.isArray(d) ? d.map((x) => x.msg).join("; ")
        : "Request failed (" + res.status + ")";
      throw new Error(msg);
    }
    return data;
  }

  function loadSdk(clientId) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = "https://www.paypal.com/sdk/js?client-id=" + encodeURIComponent(clientId) +
        "&currency=USD&intent=capture";
      s.onload = resolve;
      s.onerror = () => reject(new Error("Could not load the PayPal SDK."));
      document.head.appendChild(s);
    });
  }

  function renderButtons() {
    paypal.Buttons({
      style: { layout: "vertical", shape: "pill", label: "donate" },

      onClick: function (data, actions) {
        if (!validAmount()) return actions.reject();
        return actions.resolve();
      },

      createOrder: async function () {
        const amount = validAmount();
        showStatus("info", "Creating your order…", "", true);
        try {
          const data = await api("/api/payments/create-order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ amount: amount, currency: "USD" }),
          });
          statusBox.hidden = true;
          return data.order_id;
        } catch (err) {
          showStatus("failure", "Could not start payment", err.message);
          throw err;
        }
      },

      onApprove: async function (data) {
        showStatus("info", "Processing payment…", "Please don't close this page.", true);
        try {
          const r = await api("/api/payments/capture-order/" + encodeURIComponent(data.orderID), {
            method: "POST",
          });
          if (r.success) {
            showStatus(
              "success",
              "Payment successful 🎉",
              "Status: " + r.capture_status + " · " + r.amount + " " + r.currency +
                " · Transaction ID: " + r.transaction_id
            );
          } else {
            showStatus("failure", "Payment not completed", r.message);
          }
        } catch (err) {
          showStatus("failure", "Payment failed", err.message);
        }
      },

      onCancel: function () {
        showStatus("info", "Payment cancelled", "You closed PayPal before approving. You have not been charged.");
      },

      onError: function (err) {
        console.error("PayPal error", err);
        showStatus("failure", "Payment error", "Something went wrong with PayPal. Please try again.");
      },
    }).render("#paypal-button-container");
  }

  (async function init() {
    try {
      const cfg = await api("/api/payments/config");
      await loadSdk(cfg.client_id);
      renderButtons();
    } catch (err) {
      showStatus("failure", "Checkout unavailable", err.message);
    }
  })();
})();
