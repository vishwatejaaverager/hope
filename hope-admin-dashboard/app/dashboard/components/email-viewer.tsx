'use client';

import { useState } from 'react';
import type { CaseRow, EmailRow } from '@/lib/dashboard-data';

export function EmailCommunicationsPanel({ emails }: { emails: EmailRow[] }) {
  const [filter, setFilter] = useState<'all' | 'Incoming' | 'Outgoing'>('all');
  const [search, setSearch] = useState('');
  const [selectedId, setSelectedId] = useState<string | null>(emails[0]?.id ?? null);

  const filtered = emails.filter((em) => {
    if (filter !== 'all' && em.direction !== filter) return false;
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        em.subject.toLowerCase().includes(q) ||
        em.sender.toLowerCase().includes(q) ||
        em.recipient.toLowerCase().includes(q) ||
        em.applicationId.toLowerCase().includes(q) ||
        em.bodyPlain.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const selected = filtered.find((e) => e.id === selectedId) ?? filtered[0] ?? null;

  return (
    <div className="flex h-full flex-col bg-slate-50/60">
      {/* Top KPI & Filter Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-pp-border bg-white px-6 py-3.5">
        <div className="flex items-center gap-3">
          <div className="flex items-center rounded-lg border border-slate-200 bg-slate-100 p-0.5 text-xs font-semibold">
            {(['all', 'Incoming', 'Outgoing'] as const).map((tab) => (
              <button
                key={tab}
                type="button"
                onClick={() => setFilter(tab)}
                className={`rounded-md px-3 py-1.5 transition-colors ${
                  filter === tab
                    ? 'bg-white text-pp-navy shadow-xs'
                    : 'text-slate-600 hover:text-pp-navy'
                }`}
              >
                {tab === 'all'
                  ? `All (${emails.length})`
                  : tab === 'Incoming'
                    ? `Incoming (${emails.filter((e) => e.isIncoming).length})`
                    : `Outgoing (${emails.filter((e) => e.isOutgoing).length})`}
              </button>
            ))}
          </div>
          <input
            type="search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search subject, sender, case ID..."
            className="w-64 rounded-lg border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-900 placeholder:text-slate-400 focus:border-pp-blue focus:outline-none"
          />
        </div>

        <div className="flex items-center gap-4 text-xs text-slate-500">
          <span>
            Total Attachments:{' '}
            <strong className="text-slate-800">
              {emails.reduce((acc, e) => acc + e.attachmentCount, 0)}
            </strong>
          </span>
        </div>
      </div>

      {/* Main Split View: Email List (Left) + Full Email Reader (Right) */}
      {filtered.length === 0 ? (
        <div className="flex flex-1 flex-col items-center justify-center p-12 text-center">
          <div className="rounded-full bg-slate-100 p-4 text-slate-400">
            <svg className="size-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
            </svg>
          </div>
          <h3 className="mt-3 text-base font-semibold text-pp-navy">No emails found</h3>
          <p className="mt-1 max-w-md text-xs text-slate-500">
            Incoming emails from Zapier (`POST /api/v1/emails/incoming`) and outgoing verification emails (`POST /api/v1/emails/send`) will appear here automatically.
          </p>
        </div>
      ) : (
        <div className="grid min-h-0 flex-1 grid-cols-12">
          {/* Left Column: Clickable Email List */}
          <div className="col-span-5 overflow-y-auto border-r border-pp-border bg-white">
            <ul className="divide-y divide-slate-100">
              {filtered.map((em) => {
                const isSelected = selected?.id === em.id;
                return (
                  <li key={em.id}>
                    <button
                      type="button"
                      onClick={() => setSelectedId(em.id)}
                      className={`w-full px-5 py-4 text-left transition-colors ${
                        isSelected
                          ? 'bg-blue-50/80 border-l-4 border-l-pp-blue'
                          : 'hover:bg-slate-50'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span
                            className={`inline-flex items-center rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide ${
                              em.isIncoming
                                ? 'bg-emerald-100 text-emerald-800'
                                : 'bg-indigo-100 text-indigo-800'
                            }`}
                          >
                            {em.direction}
                          </span>
                          {em.applicationId !== '—' && (
                            <span className="rounded bg-slate-100 px-1.5 py-0.5 font-mono text-[10px] font-medium text-slate-700">
                              {em.applicationId}
                            </span>
                          )}
                        </div>
                        <span className="text-[11px] text-slate-400">
                          {em.dateTime
                            ? new Date(em.dateTime).toLocaleString()
                            : em.date || ''}
                        </span>
                      </div>

                      <p className="mt-1.5 truncate text-sm font-semibold text-pp-navy">
                        {em.subject}
                      </p>

                      <p className="mt-0.5 truncate text-xs text-slate-600">
                        {em.isIncoming ? `From: ${em.sender}` : `To: ${em.recipient}`}
                      </p>

                      <p className="mt-1 line-clamp-2 text-xs text-slate-500">
                        {em.bodySnippet}
                      </p>

                      {em.attachmentCount > 0 && (
                        <div className="mt-2 flex items-center gap-1 text-[11px] font-medium text-pp-blue">
                          <span>📎 {em.attachmentCount} attachment(s)</span>
                        </div>
                      )}
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>

          {/* Right Column: Full Email Reader */}
          <div className="col-span-7 overflow-y-auto bg-white p-6">
            {selected && (
              <div className="mx-auto max-w-3xl space-y-6">
                {/* Email Header */}
                <div className="border-b border-slate-200 pb-4">
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold uppercase ${
                          selected.isIncoming
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-indigo-100 text-indigo-800'
                        }`}
                      >
                        {selected.direction}
                      </span>
                      <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-slate-700">
                        Status: {selected.status}
                      </span>
                      {selected.applicationId !== '—' && (
                        <span className="inline-flex items-center rounded-full bg-amber-100 px-2.5 py-0.5 font-mono text-xs font-semibold text-amber-900">
                          Case / App: {selected.applicationId}
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-slate-500">
                      {selected.dateTime
                        ? new Date(selected.dateTime).toLocaleString()
                        : selected.date}
                    </span>
                  </div>

                  <h2 className="mt-3 text-lg font-bold text-pp-navy">
                    {selected.subject}
                  </h2>

                  <div className="mt-3 grid grid-cols-1 gap-1.5 rounded-lg bg-slate-50 p-3 text-xs text-slate-700 border border-slate-200/80">
                    <div>
                      <span className="font-semibold text-slate-500">From: </span>
                      <span className="font-medium text-slate-900">{selected.sender}</span>
                    </div>
                    <div>
                      <span className="font-semibold text-slate-500">To: </span>
                      <span className="font-medium text-slate-900">{selected.recipient}</span>
                    </div>
                    {selected.messageId !== '—' && (
                      <div>
                        <span className="font-semibold text-slate-500">Message ID: </span>
                        <span className="font-mono text-[11px] text-slate-600">{selected.messageId}</span>
                      </div>
                    )}
                  </div>
                </div>

                {/* AI Summary Box (if available) */}
                {selected.aiSummaryText && selected.aiSummaryText !== '—' && (
                  <div className="rounded-lg border border-indigo-200 bg-indigo-50/60 p-4">
                    <div className="text-xs font-bold uppercase tracking-wider text-indigo-800">
                      AI Summary
                    </div>
                    <p className="mt-1 text-sm text-indigo-950 whitespace-pre-wrap">
                      {selected.aiSummaryText}
                    </p>
                  </div>
                )}

                {/* Attachments Section */}
                {selected.attachmentCount > 0 && (
                  <div className="rounded-lg border border-slate-200 bg-slate-50 p-4">
                    <div className="text-xs font-bold uppercase tracking-wider text-slate-700">
                      Attachments ({selected.attachmentCount})
                    </div>
                    {selected.attachments.length > 0 ? (
                      <ul className="mt-2 space-y-2">
                        {selected.attachments.map((att, idx) => (
                          <li
                            key={idx}
                            className="flex items-center justify-between rounded-md border border-slate-200 bg-white px-3 py-2 text-xs"
                          >
                            <div className="flex items-center gap-2 truncate">
                              <span>📎</span>
                              <span className="font-semibold text-slate-800">
                                {att.filename || `Attachment ${idx + 1}`}
                              </span>
                              {att.content_type && (
                                <span className="text-slate-400">({att.content_type})</span>
                              )}
                              {typeof att.size === 'number' && (
                                <span className="text-slate-400">
                                  {(att.size / 1024).toFixed(1)} KB
                                </span>
                              )}
                            </div>
                            {att.url && (
                              <a
                                href={att.url}
                                target="_blank"
                                rel="noreferrer"
                                className="font-semibold text-pp-blue hover:underline"
                              >
                                Open / Download
                              </a>
                            )}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="mt-1 text-xs text-slate-500">
                        {selected.attachmentCount} attachment(s) recorded on this message.
                      </p>
                    )}
                  </div>
                )}

                {/* Full Email Body */}
                <div>
                  <div className="mb-2 text-xs font-bold uppercase tracking-wider text-slate-500">
                    Email Message Body
                  </div>
                  <div className="rounded-xl border border-slate-200 bg-white p-5 text-sm leading-relaxed text-slate-800 shadow-2xs whitespace-pre-wrap">
                    {selected.bodyPlain}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export function MedicalCasesPanel({
  cases,
  emails,
}: {
  cases: CaseRow[];
  emails: EmailRow[];
}) {
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(cases[0]?.id ?? null);
  const selectedCase = cases.find((c) => c.id === selectedCaseId) ?? cases[0] ?? null;

  const caseEmails = selectedCase
    ? emails.filter(
        (e) =>
          e.caseId === selectedCase.id ||
          e.applicationId.toLowerCase() === selectedCase.caseNumber.toLowerCase(),
      )
    : [];

  if (cases.length === 0) {
    return (
      <div className="flex h-full flex-col items-center justify-center bg-slate-50/60 p-12 text-center">
        <h3 className="text-base font-semibold text-pp-navy">No medical cases created yet</h3>
        <p className="mt-1 max-w-md text-xs text-slate-500">
          Cases created via `POST /api/v1/cases` will appear here with their living AI summary, pending verification items, and linked email timeline.
        </p>
      </div>
    );
  }

  return (
    <div className="grid h-full min-h-0 grid-cols-12 bg-white">
      {/* Left: Cases List */}
      <div className="col-span-5 overflow-y-auto border-r border-pp-border">
        <ul className="divide-y divide-slate-100">
          {cases.map((c) => {
            const isSelected = selectedCase?.id === c.id;
            return (
              <li key={c.id}>
                <button
                  type="button"
                  onClick={() => setSelectedCaseId(c.id)}
                  className={`w-full px-5 py-4 text-left transition-colors ${
                    isSelected
                      ? 'bg-blue-50/80 border-l-4 border-l-pp-blue'
                      : 'hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-xs font-bold text-pp-blue">
                      {c.caseNumber}
                    </span>
                    <div className="flex items-center gap-1.5">
                      <span className="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-bold text-amber-900">
                        {c.urgency}
                      </span>
                      <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold text-slate-700">
                        {c.status}
                      </span>
                    </div>
                  </div>
                  <p className="mt-1 text-sm font-semibold text-pp-navy">{c.patientName}</p>
                  <p className="text-xs text-slate-500">
                    {c.medicalCategory} • {c.hospitalName}
                  </p>
                  <p className="mt-1 line-clamp-2 text-xs text-slate-600">
                    {c.overallSummary}
                  </p>
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      {/* Right: Case Details & Email Timeline */}
      <div className="col-span-7 overflow-y-auto p-6">
        {selectedCase && (
          <div className="space-y-6">
            <div className="border-b border-slate-200 pb-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm font-bold text-pp-blue">
                  {selectedCase.caseNumber}
                </span>
                <span className="text-xs text-slate-500">{selectedCase.date}</span>
              </div>
              <h2 className="mt-1 text-xl font-bold text-pp-navy">
                {selectedCase.patientName} ({selectedCase.patientEmail})
              </h2>
              <p className="mt-1 text-xs text-slate-600">
                Hospital: <strong>{selectedCase.hospitalName}</strong> • Category:{' '}
                <strong>{selectedCase.medicalCategory}</strong> • Requested:{' '}
                <strong>${selectedCase.requestedAmount.toLocaleString()}</strong> (Estimated: $
                {selectedCase.estimatedCost.toLocaleString()})
              </p>
            </div>

            <div className="rounded-xl border border-indigo-200 bg-indigo-50/60 p-4">
              <div className="text-xs font-bold uppercase tracking-wider text-indigo-900">
                Living Case Summary
              </div>
              <p className="mt-1 text-sm text-indigo-950 whitespace-pre-wrap">
                {selectedCase.overallSummary}
              </p>
              <div className="mt-3 grid grid-cols-2 gap-3 border-t border-indigo-200/60 pt-3 text-xs">
                <div>
                  <span className="font-semibold text-indigo-800">Next Action: </span>
                  <span className="text-indigo-950">{selectedCase.nextAction}</span>
                </div>
                <div>
                  <span className="font-semibold text-indigo-800">Pending Items: </span>
                  <span className="text-indigo-950">{selectedCase.pendingItemsText}</span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                Linked Emails ({caseEmails.length})
              </h3>
              {caseEmails.length === 0 ? (
                <p className="mt-2 text-xs text-slate-400">No emails linked to this case yet.</p>
              ) : (
                <div className="mt-3 space-y-3">
                  {caseEmails.map((em) => (
                    <div
                      key={em.id}
                      className="rounded-lg border border-slate-200 bg-slate-50 p-4 text-xs"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-pp-navy">
                          [{em.direction}] {em.subject}
                        </span>
                        <span className="text-slate-400">
                          {em.dateTime ? new Date(em.dateTime).toLocaleString() : em.date}
                        </span>
                      </div>
                      <p className="mt-1 text-slate-600">
                        From: {em.sender} → To: {em.recipient}
                      </p>
                      <p className="mt-2 rounded bg-white p-3 text-slate-800 whitespace-pre-wrap border border-slate-200/70">
                        {em.bodyPlain}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

