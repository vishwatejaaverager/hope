import { InboxIcon } from './ui/icons';

// Shown in place of Studio when the sandbox account has nothing to report on.
export function EmptyData() {
  return (
    <div className="flex h-full flex-col items-center justify-center p-8 text-center">
      <span className="flex size-14 items-center justify-center rounded-full bg-pp-highlight text-pp-blue">
        <InboxIcon className="size-7" />
      </span>
      <h2 className="mt-4 text-xl font-semibold text-pp-navy">No Hope transactions yet</h2>
      <p className="mt-2 max-w-md text-[15px] text-pp-muted">
        No donations or payouts have been recorded yet. You can make a test donation on the donor page or issue a test payout to view live financial reports.
      </p>
      <div className="mt-6 flex items-center gap-4">
        <a
          href="http://127.0.0.1:8000/donate"
          target="_blank"
          rel="noreferrer"
          className="inline-flex h-10 items-center rounded-full bg-pp-blue px-5 font-semibold text-white hover:bg-pp-blue-dark"
        >
          Open Donation Page
        </a>
        <a
          href="http://127.0.0.1:8000/beneficiary"
          target="_blank"
          rel="noreferrer"
          className="inline-flex h-10 items-center rounded-full border border-pp-border bg-white px-5 font-semibold text-pp-navy hover:bg-slate-50"
        >
          Open Beneficiary Payouts
        </a>
      </div>
    </div>
  );
}
