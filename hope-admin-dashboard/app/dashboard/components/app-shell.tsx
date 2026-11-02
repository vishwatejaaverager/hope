'use client';

import { useEffect, useState, type ReactNode } from 'react';
import { BellIcon, HelpIcon } from './ui/icons';
import { AgStudioLogo } from './ui/logo';

function HopeWordmark({ className = '' }: { className?: string }) {
  return (
    <span className={`flex items-center gap-2 text-lg tracking-tight ${className}`}>
      <span className="size-3 rounded-full bg-gradient-to-br from-teal-500 to-indigo-600 inline-block" />
      <span className="text-slate-900 font-extrabold">Hope</span>
      <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700">Admin</span>
    </span>
  );
}

function PayPalWordmark({ className = '' }: { className?: string }) {
  return (
    <span className={`font-bold italic tracking-tight ${className}`}>
      <span className="text-pp-blue-dark">Pay</span>
      <span className="text-pp-sky">Pal</span>
    </span>
  );
}

function BrandLockup() {
  return (
    <div className="flex items-center gap-3">
      <HopeWordmark />
      <span className="h-6 w-px bg-pp-border" aria-hidden />
      <AgStudioLogo className="-ml-1 h-9 w-auto" />
      <span className="h-6 w-px bg-pp-border" aria-hidden />
      <span className="hidden sm:flex items-baseline gap-1 text-xs text-pp-muted">
        powered by <PayPalWordmark className="text-sm" />
      </span>
    </div>
  );
}

function TopBar() {
  const [merchant, setMerchant] = useState<{ email?: string; name?: string; merchant_id?: string } | null>(null);

  useEffect(() => {
    // Fetch merchant details from session
    fetch("/api/auth/me")
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data?.authenticated) setMerchant(data);
      })
      .catch(() => {});
  }, []);

  async function handleLogout() {
    try {
      await fetch("/api/auth/logout", {
        method: "POST",
      });
    } catch {}
    window.location.href = "/login";
  }

  const initials = merchant?.name
    ? merchant.name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "HA";

  return (
    <header className="flex h-16 shrink-0 items-center gap-6 border-b border-pp-border bg-white px-6">
      <BrandLockup />
      <div className="ml-auto flex items-center gap-3 text-pp-navy">
        <span className="inline-flex size-9 items-center justify-center rounded-full text-slate-400 hover:text-slate-600 cursor-pointer" title="Help">
          <HelpIcon />
        </span>
        <span className="inline-flex size-9 items-center justify-center rounded-full text-slate-400 hover:text-slate-600 cursor-pointer" title="Notifications">
          <BellIcon />
        </span>

        {/* Merchant Identity Profile */}
        <div className="ml-2 flex items-center gap-3 pl-3 border-l border-slate-200">
          <div className="flex items-center gap-2">
            <span className="flex size-9 items-center justify-center rounded-full bg-gradient-to-tr from-indigo-600 to-indigo-800 text-xs font-bold text-white shadow-sm">
              {initials}
            </span>
            <div className="hidden sm:flex flex-col text-left">
              <span className="text-xs font-bold text-slate-800 leading-tight">
                {merchant?.name || "Hope Merchant"}
              </span>
              <span className="text-[10px] text-slate-500 leading-tight font-mono">
                {merchant?.merchant_id ? `ID: ${merchant.merchant_id}` : merchant?.email || "Authorized"}
              </span>
            </div>
          </div>

          {/* Logout Button */}
          <button
            id="admin-logout-btn"
            onClick={handleLogout}
            className="rounded-lg border border-slate-200 bg-white px-2.5 py-1 text-xs font-semibold text-slate-700 shadow-xs hover:bg-slate-50 hover:text-red-600 hover:border-red-200 transition-colors cursor-pointer"
            title="Sign out of Admin Dashboard"
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>
  );
}

export function AppShell({
  sidebar,
  children,
}: {
  sidebar: ReactNode;
  children: ReactNode;
}) {
  return (
    <div className="flex h-dvh flex-col bg-pp-canvas font-paypal text-pp-ink">
      <TopBar />
      <div className="flex min-h-0 flex-1">
        <nav className="flex w-64 shrink-0 flex-col border-r border-pp-border bg-white" aria-label="Reports">
          {sidebar}
        </nav>
        <main className="flex min-w-0 flex-1 flex-col">{children}</main>
      </div>
    </div>
  );
}
