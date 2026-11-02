import { useEffect, useRef, useState } from "react";
import { getPaymentConfig, createOrder, captureOrder, CaptureOrderResponse } from "../services/api";

interface PayPalButtonProps {
  amount: string;
  currency?: string;
  isValid: boolean;
  onStatusChange: (
    kind: "info" | "success" | "failure",
    title: string,
    body?: string,
    loading?: boolean
  ) => void;
  onSuccess: (result: CaptureOrderResponse) => void;
}

// Global promise so multiple re-renders don't inject multiple script tags
let sdkLoadPromise: Promise<string> | null = null;

function loadPayPalSdk(clientId: string, currency = "USD"): Promise<string> {
  if (window.paypal) {
    return Promise.resolve(clientId);
  }

  if (!sdkLoadPromise) {
    sdkLoadPromise = new Promise((resolve, reject) => {
      const existingScript = document.querySelector('script[src*="paypal.com/sdk/js"]');
      if (existingScript) {
        existingScript.addEventListener("load", () => resolve(clientId));
        existingScript.addEventListener("error", () => reject(new Error("Failed to load PayPal SDK")));
        return;
      }

      const script = document.createElement("script");
      script.src = `https://www.paypal.com/sdk/js?client-id=${encodeURIComponent(
        clientId
      )}&currency=${encodeURIComponent(currency)}&intent=capture`;
      script.async = true;

      script.onload = () => {
        resolve(clientId);
      };

      script.onerror = () => {
        sdkLoadPromise = null;
        reject(new Error("Could not load the PayPal SDK. Check your network or credentials."));
      };

      document.head.appendChild(script);
    });
  }

  return sdkLoadPromise;
}

export function PayPalButton({
  amount,
  currency = "USD",
  isValid,
  onStatusChange,
  onSuccess,
}: PayPalButtonProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [sdkReady, setSdkReady] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  // Keep latest refs for callbacks to avoid re-rendering buttons constantly
  const amountRef = useRef(amount);
  const isValidRef = useRef(isValid);
  const currencyRef = useRef(currency);
  const onSuccessRef = useRef(onSuccess);
  const onStatusChangeRef = useRef(onStatusChange);

  useEffect(() => {
    amountRef.current = amount;
    isValidRef.current = isValid;
    currencyRef.current = currency;
    onSuccessRef.current = onSuccess;
    onStatusChangeRef.current = onStatusChange;
  });

  // Step 1: Initialize PayPal SDK
  useEffect(() => {
    let isMounted = true;

    async function initSdk() {
      try {
        const config = await getPaymentConfig();
        if (!isMounted) return;

        await loadPayPalSdk(config.client_id, config.currency || currency);
        if (!isMounted) return;

        setSdkReady(true);
      } catch (err: unknown) {
        if (!isMounted) return;
        const msg = err instanceof Error ? err.message : "Failed to initialize PayPal";
        setLoadError(msg);
        onStatusChangeRef.current("failure", "Checkout unavailable", msg, false);
      }
    }

    initSdk();

    return () => {
      isMounted = false;
    };
  }, [currency]);

  // Step 2: Render PayPal Buttons when SDK is ready
  useEffect(() => {
    if (!sdkReady || !containerRef.current || !window.paypal) return;

    // Clear previous rendered button iframe/container
    containerRef.current.innerHTML = "";

    try {
      window.paypal
        .Buttons({
          style: {
            layout: "vertical",
            shape: "pill",
            color: "gold",
            label: "donate",
            height: 48,
          },

          onClick: (_data, actions) => {
            if (!isValidRef.current) {
              onStatusChangeRef.current(
                "failure",
                "Invalid Amount",
                "Please enter a valid donation amount ($1 - $10,000).",
                false
              );
              return actions.reject();
            }
            return actions.resolve();
          },

          createOrder: async () => {
            onStatusChangeRef.current("info", "Creating your order…", "Contacting PayPal...", true);
            try {
              const res = await createOrder(amountRef.current, currencyRef.current);
              // Hide status box while user interacts with PayPal popup
              onStatusChangeRef.current("info", "", "", false);
              return res.order_id;
            } catch (err: unknown) {
              const msg = err instanceof Error ? err.message : "Order creation failed";
              onStatusChangeRef.current("failure", "Could not start payment", msg, false);
              throw err;
            }
          },

          onApprove: async (data) => {
            onStatusChangeRef.current(
              "info",
              "Processing payment…",
              "Please do not close this window while we finalize your donation.",
              true
            );

            try {
              const result = await captureOrder(data.orderID);
              if (result.success) {
                onStatusChangeRef.current(
                  "success",
                  "Payment successful 🎉",
                  `Status: ${result.capture_status} · ${result.amount} ${result.currency} · Transaction ID: ${result.transaction_id}`,
                  false
                );
                onSuccessRef.current(result);
              } else {
                onStatusChangeRef.current("failure", "Payment not completed", result.message, false);
              }
            } catch (err: unknown) {
              const msg = err instanceof Error ? err.message : "Payment capture failed";
              onStatusChangeRef.current("failure", "Payment failed", msg, false);
            }
          },

          onCancel: () => {
            onStatusChangeRef.current(
              "info",
              "Payment cancelled",
              "You closed PayPal before completing the donation. You have not been charged.",
              false
            );
          },

          onError: (err: unknown) => {
            console.error("PayPal error", err);
            onStatusChangeRef.current(
              "failure",
              "Payment error",
              "Something went wrong with PayPal. Please try again.",
              false
            );
          },
        })
        .render(containerRef.current);
    } catch (err: unknown) {
      console.error("Error rendering PayPal buttons:", err);
    }
  }, [sdkReady]);

  if (loadError) {
    return (
      <div className="status-box failure">
        <div className="status-header-row">
          <span>Checkout Unavailable</span>
        </div>
        <p className="status-detail-text">{loadError}</p>
      </div>
    );
  }

  return (
    <div className="paypal-section">
      {!sdkReady && (
        <div className="paypal-sdk-loader">
          <div className="spinner-ring" />
          <span>Connecting to PayPal Sandbox…</span>
        </div>
      )}
      <div ref={containerRef} id="paypal-button-container" />
    </div>
  );
}
