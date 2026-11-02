import { Suspense } from "react";
import Link from "next/link";
import { AgStudioLogo } from "../dashboard/components/ui/logo";
import { LoginForm } from "./login-form";

export const metadata = {
  title: "Merchant Sign In — Hope Admin",
};


function ErrorBanner({ error, merchantId }: { error?: string; merchantId?: string }) {
  if (!error) return null;

  let title = "Sign-in error";
  let message = "An error occurred during authentication. Please try again.";

  if (error === "unauthorized_merchant") {
    title = "Access Denied: Unauthorized Merchant";
    message = merchantId
      ? `The authenticated PayPal account (${merchantId}) is not authorized to access the Hope Admin Dashboard. Please sign in with the authorized Hope Merchant account.`
      : "Your PayPal account is not authorized to access the Hope Admin Dashboard.";
  } else if (error === "csrf_validation_failed") {
    title = "Security Validation Failed";
    message = "Your session state could not be validated. Please click sign in again.";
  } else if (error === "missing_code_or_state") {
    title = "Incomplete Authorization";
    message = "PayPal did not return the expected authorization code.";
  } else {
    message = decodeURIComponent(error);
  }

  return (
    <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-800 animate-in fade-in">
      <div className="flex items-start gap-3">
        <svg
          className="mt-0.5 size-5 shrink-0 text-red-600"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z"
          />
        </svg>
        <div>
          <h3 className="font-semibold text-red-900">{title}</h3>
          <p className="mt-1 text-xs text-red-700 leading-relaxed">{message}</p>
        </div>
      </div>
    </div>
  );
}

async function LoginContent({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; merchant_id?: string }>;
}) {
  const params = await searchParams;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        {/* Brand Lockup */}
        <div className="flex items-center justify-center gap-3 mb-4">
          <span className="size-4 rounded-full bg-gradient-to-br from-teal-500 to-indigo-600 inline-block" />
          <span className="text-2xl font-black tracking-tight text-slate-900">Hope</span>
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-indigo-100 text-indigo-700">Admin</span>
          <span className="h-6 w-px bg-slate-300 mx-1" aria-hidden />
          <AgStudioLogo className="h-8 w-auto" />
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-slate-900">
          Executive Admin Dashboard
        </h2>
        <p className="mt-2 text-sm text-slate-600">
          Sign in with your verified PayPal Merchant account to manage pooled medical funds and beneficiary payouts.
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-white py-8 px-6 shadow-sm border border-slate-200 rounded-xl sm:px-10">
          <ErrorBanner error={params.error} merchantId={params.merchant_id} />
          <LoginForm />
        </div>

        <p className="mt-6 text-center text-xs text-slate-500">
          Looking to make a donation? Visit the{" "}
          <Link href="/donate" className="font-semibold text-indigo-600 hover:text-indigo-500 underline">
            Public Donation Portal
          </Link>
        </p>
      </div>
    </div>
  );
}

export default function LoginPage(props: {
  searchParams: Promise<{ error?: string; merchant_id?: string }>;
}) {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-50" />}>
      <LoginContent searchParams={props.searchParams} />
    </Suspense>
  );
}
