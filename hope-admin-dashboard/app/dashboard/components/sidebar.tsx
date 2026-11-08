'use client';

import { useState } from 'react';
import { CloseIcon, MoreIcon, PlusIcon, ReportIcon } from './ui/icons';
import { pagesFor, type ReportPage } from '../page-titles';
import type { SavedReport } from '../reports-store';
import { Button, Menu, MenuItem } from './ui/ui';

export type ActiveViewSection = 'reports' | 'cases' | 'emails';

// Reports, each listing its pages. The open report shows its live pages (including unsaved
// ones); the others show their saved pages. Double-click a report or page to rename it.
export function ReportsSidebar({
  reports,
  activeId,
  activePages,
  selectedPageId,
  activeSection = 'reports',
  casesCount = 0,
  emailsCount = 0,
  editing,
  ready,
  onSelectSection,
  onSelectReport,
  onSelectPage,
  onAddPage,
  onRemovePage,
  onRenamePage,
  onRenameReport,
  onCreate,
  onDuplicate,
  onDelete,
  onReset,
}: {
  reports: SavedReport[];
  activeId: string;
  activePages: ReportPage[];
  selectedPageId: string;
  activeSection?: ActiveViewSection;
  casesCount?: number;
  emailsCount?: number;
  editing: boolean;
  ready: boolean;
  onSelectSection?: (section: ActiveViewSection) => void;
  onSelectReport: (id: string) => void;
  onSelectPage: (reportId: string, pageId: string) => void;
  onAddPage: () => string | undefined;
  onRemovePage: (pageId: string) => void;
  onRenamePage: (pageId: string, title: string) => void;
  onRenameReport: (reportId: string, name: string) => void;
  onCreate: () => void;
  onDuplicate: (id: string) => void;
  onDelete: (id: string) => void;
  onReset: () => void;
}) {
  const [menuFor, setMenuFor] = useState<string | null>(null);
  const [renaming, setRenaming] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<string, boolean>>({});

  const finishRename = (value: string, commit: (title: string) => void) => {
    setRenaming(null);
    if (value.trim()) commit(value.trim());
  };

  return (
    <>
      <p className="px-6 pb-2 pt-6 text-xs font-semibold uppercase tracking-wider text-pp-muted">Reports</p>
      <ul className="flex-1 space-y-1 overflow-y-auto px-3 pb-4">
        {reports.map((report) => {
          const active = report.id === activeId;
          const open = expanded[report.id] ?? active;
          const pages = active ? activePages : pagesFor(report);

          return (
            <li key={report.id}>
              <div className="group relative">
                {renaming === report.id ? (
                  <RenameInput
                    value={report.name}
                    label="Report name"
                    className="ml-1 w-[calc(100%-8px)] py-2 text-[15px]"
                    onDone={(value) => finishRename(value, (name) => onRenameReport(report.id, name))}
                    onCancel={() => setRenaming(null)}
                  />
                ) : (
                  <button
                    type="button"
                    disabled={!ready}
                    onClick={() => {
                      onSelectSection?.('reports');
                      if (active && activeSection === 'reports') {
                        setExpanded((current) => ({ ...current, [report.id]: !open }));
                      } else {
                        setExpanded((current) => ({ ...current, [report.id]: true }));
                        onSelectReport(report.id);
                      }
                    }}
                    onDoubleClick={() => setRenaming(report.id)}
                    aria-expanded={open}
                    className={`flex w-full items-center gap-3 rounded-full py-2.5 pl-4 pr-10 text-left text-[15px] transition-colors ${
                      active && activeSection === 'reports'
                        ? 'font-semibold text-pp-navy'
                        : 'text-pp-ink hover:bg-pp-canvas'
                    }`}
                  >
                    <ReportIcon className={`size-5 shrink-0 ${active && activeSection === 'reports' ? 'text-pp-blue' : ''}`} />
                    <span className="truncate">{report.name}</span>
                  </button>
                )}
                <div className="absolute right-1 top-1/2 -translate-y-1/2">
                  <button
                    type="button"
                    aria-label={`Actions for ${report.name}`}
                    aria-haspopup="menu"
                    aria-expanded={menuFor === report.id}
                    onClick={() => setMenuFor(menuFor === report.id ? null : report.id)}
                    className={`flex size-8 items-center justify-center rounded-full text-pp-muted hover:bg-white hover:text-pp-navy ${
                      menuFor === report.id ? 'opacity-100' : 'opacity-0 focus-visible:opacity-100 group-hover:opacity-100'
                    }`}
                  >
                    <MoreIcon />
                  </button>
                  <Menu open={menuFor === report.id} onClose={() => setMenuFor(null)}>
                    <MenuItem
                      onClick={() => {
                        setMenuFor(null);
                        setRenaming(report.id);
                      }}
                    >
                      Rename
                    </MenuItem>
                    <MenuItem
                      onClick={() => {
                        setMenuFor(null);
                        onDuplicate(report.id);
                      }}
                    >
                      Duplicate
                    </MenuItem>
                    <MenuItem
                      danger
                      onClick={() => {
                        setMenuFor(null);
                        onDelete(report.id);
                      }}
                    >
                      {report.builtIn ? 'Reset to default' : 'Delete'}
                    </MenuItem>
                  </Menu>
                </div>
              </div>

              {open && (
                <ul className="mb-2 ml-[26px] mt-1 space-y-0.5 border-l border-pp-border pl-3" aria-label={`${report.name} pages`}>
                  {pages.map((page) => {
                    const selected = active && activeSection === 'reports' && page.id === selectedPageId;
                    return (
                      <li key={page.id} className="group relative">
                        {renaming === page.id ? (
                          <RenameInput
                            value={page.title}
                            label="Page name"
                            className="w-full py-1.5 text-sm"
                            onDone={(value) => finishRename(value, (title) => onRenamePage(page.id, title))}
                            onCancel={() => setRenaming(null)}
                          />
                        ) : (
                          <button
                            type="button"
                            disabled={!ready}
                            onClick={() => {
                              onSelectSection?.('reports');
                              onSelectPage(report.id, page.id);
                            }}
                            onDoubleClick={() => active && editing && setRenaming(page.id)}
                            aria-current={selected ? 'page' : undefined}
                            title={active && editing ? 'Double-click to rename' : undefined}
                            className={`block w-full truncate rounded-full py-2 pl-4 pr-8 text-left text-sm transition-colors ${
                              selected ? 'bg-pp-highlight font-semibold text-pp-blue' : 'text-pp-muted hover:bg-pp-canvas hover:text-pp-navy'
                            }`}
                          >
                            {page.title}
                          </button>
                        )}
                        {active && editing && pages.length > 1 && renaming !== page.id && (
                          <button
                            type="button"
                            aria-label={`Remove page ${page.title}`}
                            title="Remove page"
                            onClick={() => onRemovePage(page.id)}
                            className="absolute right-1.5 top-1/2 flex size-6 -translate-y-1/2 items-center justify-center rounded-full text-pp-muted opacity-0 hover:bg-white hover:text-pp-danger focus-visible:opacity-100 group-hover:opacity-100"
                          >
                            <CloseIcon className="size-3.5" />
                          </button>
                        )}
                      </li>
                    );
                  })}
                  {active && (
                    <li>
                      <button
                        type="button"
                        disabled={!ready}
                        onClick={() => {
                          const id = onAddPage();
                          if (id) setRenaming(id);
                        }}
                        className="flex w-full items-center gap-1.5 rounded-full py-2 pl-4 text-left text-sm font-semibold text-pp-blue hover:bg-pp-highlight"
                      >
                        <PlusIcon className="size-4" /> Add page
                      </button>
                    </li>
                  )}
                </ul>
              )}
            </li>
          );
        })}

        {/* Separate Operations / Verification Category */}
        <li className="pt-4">
          <div className="mb-1.5 border-t border-pp-border pt-4 px-3 text-xs font-semibold uppercase tracking-wider text-pp-muted">
            Verification &amp; Inbox
          </div>
          <div className="space-y-1">
            <button
              type="button"
              onClick={() => onSelectSection?.('cases')}
              className={`flex w-full items-center justify-between rounded-full py-2.5 px-4 text-left text-[15px] transition-colors ${
                activeSection === 'cases'
                  ? 'bg-pp-highlight font-semibold text-pp-blue'
                  : 'text-pp-ink hover:bg-pp-canvas'
              }`}
            >
              <span className="flex items-center gap-3 truncate">
                <svg className="size-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="truncate">Medical Cases</span>
              </span>
              <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600">
                {casesCount}
              </span>
            </button>

            <button
              type="button"
              onClick={() => onSelectSection?.('emails')}
              className={`flex w-full items-center justify-between rounded-full py-2.5 px-4 text-left text-[15px] transition-colors ${
                activeSection === 'emails'
                  ? 'bg-pp-highlight font-semibold text-pp-blue'
                  : 'text-pp-ink hover:bg-pp-canvas'
              }`}
            >
              <span className="flex items-center gap-3 truncate">
                <svg className="size-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
                </svg>
                <span className="truncate">Email Communications</span>
              </span>
              <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-xs font-semibold text-slate-600">
                {emailsCount}
              </span>
            </button>
          </div>
        </li>
      </ul>
      <div className="border-t border-pp-border p-4">
        <Button variant="primary" className="w-full" onClick={onCreate}>
          <PlusIcon /> New report
        </Button>
        <p className="mt-3 text-center text-xs text-pp-muted">
          Reports are saved in this browser.{' '}
          <button type="button" onClick={onReset} disabled={!ready} className="font-semibold text-pp-blue hover:underline">
            Reset demo
          </button>
        </p>
      </div>
    </>
  );
}

// Studio moves focus when the selected page changes, so focus on the next frame.
const focusAndSelect = (input: HTMLInputElement | null) => {
  if (!input) return;
  requestAnimationFrame(() => {
    input.focus();
    input.select();
  });
};

function RenameInput({
  value,
  label,
  className,
  onDone,
  onCancel,
}: {
  value: string;
  label: string;
  className: string;
  onDone: (value: string) => void;
  onCancel: () => void;
}) {
  return (
    <input
      ref={focusAndSelect}
      defaultValue={value}
      aria-label={label}
      onBlur={(e) => onDone(e.currentTarget.value)}
      onKeyDown={(e) => {
        if (e.key === 'Enter') e.currentTarget.blur();
        if (e.key === 'Escape') onCancel();
      }}
      className={`rounded-full border border-pp-blue bg-white px-4 font-semibold text-pp-navy outline-none ${className}`}
    />
  );
}
