export interface PayPalButtonActions {
  resolve: () => Promise<void>;
  reject: () => Promise<void>;
}

export interface PayPalButtonsOptions {
  style?: {
    layout?: "vertical" | "horizontal";
    color?: "gold" | "blue" | "silver" | "white" | "black";
    shape?: "pill" | "rect";
    label?: "paypal" | "checkout" | "buynow" | "pay" | "donate";
    tagline?: boolean;
    height?: number;
  };
  onClick?: (data: Record<string, unknown>, actions: PayPalButtonActions) => Promise<void> | void;
  createOrder: (data: Record<string, unknown>, actions: Record<string, unknown>) => Promise<string>;
  onApprove: (data: { orderID: string; payerID?: string }, actions: Record<string, unknown>) => Promise<void>;
  onCancel?: (data: Record<string, unknown>) => void;
  onError?: (err: unknown) => void;
}

export interface PayPalSDK {
  Buttons: (options: PayPalButtonsOptions) => {
    render: (target: HTMLElement | string) => Promise<void>;
  };
}

declare global {
  interface Window {
    paypal?: PayPalSDK;
  }
}
