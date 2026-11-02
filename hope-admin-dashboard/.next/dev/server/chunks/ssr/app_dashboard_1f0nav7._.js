module.exports = [
"[project]/app/dashboard/components/app-shell.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AppShell",
    ()=>AppShell
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/icons.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$logo$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/logo.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
// The app frame, laid out like the PayPal Developer Dashboard: a white top bar, a left sidebar
// and a light canvas. Shared by the dashboard, its loading skeleton and its error page.
function HopeWordmark({ className = '' }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: `flex items-center gap-2 text-lg tracking-tight ${className}`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "size-3 rounded-full bg-gradient-to-br from-teal-500 to-indigo-600 inline-block"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 13,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "text-slate-900 font-extrabold",
                children: "Hope"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "text-xs font-semibold px-2 py-0.5 rounded bg-indigo-50 text-indigo-700",
                children: "Admin"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 15,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/app-shell.tsx",
        lineNumber: 12,
        columnNumber: 5
    }, this);
}
function PayPalWordmark({ className = '' }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: `font-bold italic tracking-tight ${className}`,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "text-pp-blue-dark",
                children: "Pay"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 23,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "text-pp-sky",
                children: "Pal"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 24,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/app-shell.tsx",
        lineNumber: 22,
        columnNumber: 5
    }, this);
}
function BrandLockup() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex items-center gap-3",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(HopeWordmark, {}, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 32,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "h-6 w-px bg-pp-border",
                "aria-hidden": true
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 33,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$logo$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AgStudioLogo"], {
                className: "-ml-1 h-9 w-auto"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 34,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "h-6 w-px bg-pp-border",
                "aria-hidden": true
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 35,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "hidden sm:flex items-baseline gap-1 text-xs text-pp-muted",
                children: [
                    "powered by ",
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(PayPalWordmark, {
                        className: "text-sm"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 37,
                        columnNumber: 20
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 36,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/app-shell.tsx",
        lineNumber: 31,
        columnNumber: 5
    }, this);
}
function TopBar() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
        className: "flex h-16 shrink-0 items-center gap-6 border-b border-pp-border bg-white px-6",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(BrandLockup, {}, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 46,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "ml-auto flex items-center gap-1 text-pp-navy",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "inline-flex size-9 items-center justify-center rounded-full",
                        title: "Help",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["HelpIcon"], {}, void 0, false, {
                            fileName: "[project]/app/dashboard/components/app-shell.tsx",
                            lineNumber: 49,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 48,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "inline-flex size-9 items-center justify-center rounded-full",
                        title: "Notifications",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["BellIcon"], {}, void 0, false, {
                            fileName: "[project]/app/dashboard/components/app-shell.tsx",
                            lineNumber: 52,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 51,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "ml-2 flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "flex size-9 items-center justify-center rounded-full bg-indigo-600 text-sm font-semibold text-white",
                                children: "HA"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                                lineNumber: 55,
                                columnNumber: 11
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "hidden text-sm font-semibold sm:inline",
                                children: "Hope Admin"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                                lineNumber: 58,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 54,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 47,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/app-shell.tsx",
        lineNumber: 45,
        columnNumber: 5
    }, this);
}
function AppShell({ sidebar, children }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex h-dvh flex-col bg-pp-canvas font-paypal text-pp-ink",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(TopBar, {}, void 0, false, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 74,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex min-h-0 flex-1",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("nav", {
                        className: "flex w-64 shrink-0 flex-col border-r border-pp-border bg-white",
                        "aria-label": "Reports",
                        children: sidebar
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 76,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
                        className: "flex min-w-0 flex-1 flex-col",
                        children: children
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/app-shell.tsx",
                        lineNumber: 79,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/app-shell.tsx",
                lineNumber: 75,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/app-shell.tsx",
        lineNumber: 73,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/dialogs.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "CreateReportDialog",
    ()=>CreateReportDialog,
    "DeleteReportDialog",
    ()=>DeleteReportDialog,
    "ResetDemoDialog",
    ()=>ResetDemoDialog,
    "UnsavedChangesDialog",
    ()=>UnsavedChangesDialog
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/ui.tsx [app-ssr] (ecmascript)");
'use client';
;
;
function UnsavedChangesDialog({ open, reportName, onCancel, onDiscard, onSave }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Dialog"], {
        open: open,
        title: `Save changes to “${reportName}”?`,
        onClose: onCancel,
        actions: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "ghost",
                    onClick: onCancel,
                    children: "Cancel"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 37,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    onClick: onDiscard,
                    children: "Discard changes"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 40,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "primary",
                    onClick: onSave,
                    children: "Save"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 41,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/dialogs.tsx",
            lineNumber: 36,
            columnNumber: 9
        }, this),
        children: "Your changes to this report haven't been saved yet."
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/dialogs.tsx",
        lineNumber: 31,
        columnNumber: 5
    }, this);
}
function CreateReportDialog({ open, onClose, onCreate }) {
    const formId = 'create-report';
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Dialog"], {
        open: open,
        title: "New report",
        onClose: onClose,
        actions: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "ghost",
                    onClick: onClose,
                    children: "Cancel"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 69,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "primary",
                    type: "submit",
                    form: formId,
                    children: "Create report"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 72,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/dialogs.tsx",
            lineNumber: 68,
            columnNumber: 9
        }, this),
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
            id: formId,
            onSubmit: (e)=>{
                e.preventDefault();
                const name = String(new FormData(e.currentTarget).get('name') ?? '').trim();
                onCreate(name || 'Untitled report');
            },
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    children: "Start from a blank page and build it with the widgets in Compose."
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 86,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                    className: "mt-4 block text-sm font-semibold text-pp-navy",
                    htmlFor: "report-name",
                    children: "Report name"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 87,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                    id: "report-name",
                    name: "name",
                    autoFocus: true,
                    defaultValue: "Untitled report",
                    onFocus: (e)=>e.currentTarget.select(),
                    className: "mt-1 h-11 w-full rounded border border-pp-border px-3 text-[15px] text-pp-ink outline-none focus:border-pp-blue focus:ring-2 focus:ring-pp-highlight"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 90,
                    columnNumber: 9
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/dialogs.tsx",
            lineNumber: 78,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/dialogs.tsx",
        lineNumber: 63,
        columnNumber: 5
    }, this);
}
function DeleteReportDialog({ report, onCancel, onConfirm }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Dialog"], {
        open: report !== null,
        title: report?.builtIn ? 'Reset to default?' : 'Delete report?',
        onClose: onCancel,
        actions: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "ghost",
                    onClick: onCancel,
                    children: "Cancel"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 120,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "danger",
                    onClick: ()=>report && onConfirm(report),
                    children: report?.builtIn ? 'Reset' : 'Delete'
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 123,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/dialogs.tsx",
            lineNumber: 119,
            columnNumber: 9
        }, this),
        children: report && (report.builtIn ? `“${report.name}” will go back to the report shipped with the app. Your saved changes to it will be lost.` : `“${report.name}” will be removed from this browser. This can't be undone.`)
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/dialogs.tsx",
        lineNumber: 114,
        columnNumber: 5
    }, this);
}
function ResetDemoDialog({ open, builtInName, onCancel, onConfirm }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Dialog"], {
        open: open,
        title: "Reset the demo?",
        onClose: onCancel,
        actions: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "ghost",
                    onClick: onCancel,
                    children: "Cancel"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 155,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                    variant: "danger",
                    onClick: onConfirm,
                    children: "Reset demo"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/dialogs.tsx",
                    lineNumber: 158,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/dialogs.tsx",
            lineNumber: 154,
            columnNumber: 9
        }, this),
        children: [
            "All reports you've created will be deleted and “",
            builtInName,
            "” will go back to its original state, including any unsaved changes. This can't be undone."
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/dialogs.tsx",
        lineNumber: 149,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/empty-data.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "EmptyData",
    ()=>EmptyData
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/icons.tsx [app-ssr] (ecmascript)");
;
;
function EmptyData() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex h-full flex-col items-center justify-center p-8 text-center",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "flex size-14 items-center justify-center rounded-full bg-pp-highlight text-pp-blue",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["InboxIcon"], {
                    className: "size-7"
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/empty-data.tsx",
                    lineNumber: 8,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/empty-data.tsx",
                lineNumber: 7,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                className: "mt-4 text-xl font-semibold text-pp-navy",
                children: "No Hope transactions yet"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/empty-data.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "mt-2 max-w-md text-[15px] text-pp-muted",
                children: "No donations or payouts have been recorded yet. You can make a test donation on the donor page or issue a test payout to view live financial reports."
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/empty-data.tsx",
                lineNumber: 11,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "mt-6 flex items-center gap-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "http://127.0.0.1:8000/donate",
                        target: "_blank",
                        rel: "noreferrer",
                        className: "inline-flex h-10 items-center rounded-full bg-pp-blue px-5 font-semibold text-white hover:bg-pp-blue-dark",
                        children: "Open Donation Page"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/empty-data.tsx",
                        lineNumber: 15,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("a", {
                        href: "http://127.0.0.1:8000/beneficiary",
                        target: "_blank",
                        rel: "noreferrer",
                        className: "inline-flex h-10 items-center rounded-full border border-pp-border bg-white px-5 font-semibold text-pp-navy hover:bg-slate-50",
                        children: "Open Beneficiary Payouts"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/empty-data.tsx",
                        lineNumber: 23,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/empty-data.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/empty-data.tsx",
        lineNumber: 6,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/report-header.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ReportHeader",
    ()=>ReportHeader
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/navigation.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/icons.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/ui.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
;
;
function ReportHeader({ reportName, pageTitle, asOf, editing, pageIsEmpty, canUndo, canRedo, onUndo, onRedo, onSave, onDiscard, onEditingChange }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "flex flex-wrap items-start gap-x-6 gap-y-3 border-b border-pp-border bg-white px-8 py-5",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "min-w-0 flex-1",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "truncate text-sm font-semibold text-pp-muted",
                        children: reportName
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 40,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h1", {
                        className: "truncate text-[28px] font-semibold leading-tight text-pp-navy",
                        children: pageTitle
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 41,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(DataFreshness, {
                        asOf: asOf
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 42,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 39,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex items-center gap-2",
                children: [
                    editing && pageIsEmpty && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mr-2 text-sm text-pp-muted",
                        children: [
                            "Drag a widget from ",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "font-semibold text-pp-navy",
                                children: "Compose"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 47,
                                columnNumber: 32
                            }, this),
                            " to get started."
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 46,
                        columnNumber: 11
                    }, this),
                    editing && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["IconButton"], {
                                label: "Undo",
                                disabled: !canUndo,
                                onClick: onUndo,
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["UndoIcon"], {}, void 0, false, {
                                    fileName: "[project]/app/dashboard/components/report-header.tsx",
                                    lineNumber: 53,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 52,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["IconButton"], {
                                label: "Redo",
                                disabled: !canRedo,
                                onClick: onRedo,
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["RedoIcon"], {}, void 0, false, {
                                    fileName: "[project]/app/dashboard/components/report-header.tsx",
                                    lineNumber: 56,
                                    columnNumber: 15
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 55,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "mx-2 h-6 w-px bg-pp-border",
                                "aria-hidden": true
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 58,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                                onClick: onDiscard,
                                size: "sm",
                                children: "Discard"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 59,
                                columnNumber: 13
                            }, this),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                                variant: "primary",
                                size: "sm",
                                onClick: onSave,
                                children: "Save"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 62,
                                columnNumber: 13
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 51,
                        columnNumber: 11
                    }, this),
                    editing ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        variant: "ghost",
                        size: "sm",
                        onClick: ()=>onEditingChange(false),
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["EyeIcon"], {
                                className: "size-4"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 69,
                                columnNumber: 13
                            }, this),
                            " View"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 68,
                        columnNumber: 11
                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        variant: "ghost",
                        size: "sm",
                        onClick: ()=>onEditingChange(true),
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["EditIcon"], {
                                className: "size-4"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/report-header.tsx",
                                lineNumber: 73,
                                columnNumber: 13
                            }, this),
                            " Edit"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 72,
                        columnNumber: 11
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 44,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/report-header.tsx",
        lineNumber: 38,
        columnNumber: 5
    }, this);
}
// --- Data freshness -----------------------------------------------------------------
const MINUTE_MS = 60_000;
let now = 0;
const subscribeNow = (listener)=>{
    now = Date.now();
    const id = setInterval(()=>{
        now = Date.now();
        listener();
    }, 30_000);
    return ()=>clearInterval(id);
};
function relativeTime(iso, at) {
    const minutes = Math.floor((at - Date.parse(iso)) / MINUTE_MS);
    if (minutes < 1) return 'just now';
    if (minutes < 60) return `${minutes} min ago`;
    const hours = Math.floor(minutes / 60);
    return hours < 24 ? `${hours} h ago` : new Date(iso).toLocaleDateString('en-GB');
}
function DataFreshness({ asOf }) {
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRouter"])();
    const [refreshing, startRefresh] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useTransition"])();
    const at = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useSyncExternalStore"])(subscribeNow, ()=>now, ()=>0);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        className: "mt-1 flex items-center gap-2 text-sm text-pp-muted",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "inline-flex items-center gap-1.5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                        className: "size-2 rounded-full bg-pp-success",
                        "aria-hidden": true
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/report-header.tsx",
                        lineNumber: 110,
                        columnNumber: 9
                    }, this),
                    "PayPal sandbox"
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 109,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                "aria-hidden": true,
                children: "·"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 113,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                title: new Date(asOf).toLocaleString('en-GB'),
                children: refreshing ? 'Refreshing…' : `Updated ${at ? relativeTime(asOf, at) : new Date(asOf).toLocaleTimeString('en-GB')}`
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 114,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                type: "button",
                onClick: ()=>startRefresh(()=>router.refresh()),
                disabled: refreshing,
                "aria-label": "Refresh data",
                title: "Refresh data",
                className: "inline-flex size-7 items-center justify-center rounded-full text-pp-blue hover:bg-pp-highlight disabled:text-pp-muted",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["RefreshIcon"], {
                    className: `size-4 ${refreshing ? 'animate-spin' : ''}`
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/report-header.tsx",
                    lineNumber: 125,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/report-header.tsx",
                lineNumber: 117,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/report-header.tsx",
        lineNumber: 108,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/sidebar.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ReportsSidebar",
    ()=>ReportsSidebar
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/icons.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$page$2d$titles$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/page-titles.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/ui/ui.tsx [app-ssr] (ecmascript)");
'use client';
;
;
;
;
;
function ReportsSidebar({ reports, activeId, activePages, selectedPageId, editing, ready, onSelectReport, onSelectPage, onAddPage, onRemovePage, onRenamePage, onRenameReport, onCreate, onDuplicate, onDelete, onReset }) {
    const [menuFor, setMenuFor] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [renaming, setRenaming] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [expanded, setExpanded] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])({});
    const finishRename = (value, commit)=>{
        setRenaming(null);
        if (value.trim()) commit(value.trim());
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "px-6 pb-2 pt-6 text-xs font-semibold uppercase tracking-wider text-pp-muted",
                children: "Reports"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                lineNumber: 57,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                className: "flex-1 space-y-1 overflow-y-auto px-3 pb-4",
                children: reports.map((report)=>{
                    const active = report.id === activeId;
                    const open = expanded[report.id] ?? active;
                    const pages = active ? activePages : (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$page$2d$titles$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["pagesFor"])(report);
                    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: "group relative",
                                children: [
                                    renaming === report.id ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(RenameInput, {
                                        value: report.name,
                                        label: "Report name",
                                        className: "ml-1 w-[calc(100%-8px)] py-2 text-[15px]",
                                        onDone: (value)=>finishRename(value, (name)=>onRenameReport(report.id, name)),
                                        onCancel: ()=>setRenaming(null)
                                    }, void 0, false, {
                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                        lineNumber: 68,
                                        columnNumber: 19
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                        type: "button",
                                        disabled: !ready,
                                        onClick: ()=>{
                                            if (active) setExpanded((current)=>({
                                                    ...current,
                                                    [report.id]: !open
                                                }));
                                            else {
                                                setExpanded((current)=>({
                                                        ...current,
                                                        [report.id]: true
                                                    }));
                                                onSelectReport(report.id);
                                            }
                                        },
                                        onDoubleClick: ()=>setRenaming(report.id),
                                        "aria-expanded": open,
                                        className: `flex w-full items-center gap-3 rounded-full py-2.5 pl-4 pr-10 text-left text-[15px] transition-colors ${active ? 'font-semibold text-pp-navy' : 'text-pp-ink hover:bg-pp-canvas'}`,
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ReportIcon"], {
                                                className: `size-5 shrink-0 ${active ? 'text-pp-blue' : ''}`
                                            }, void 0, false, {
                                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                lineNumber: 92,
                                                columnNumber: 21
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                className: "truncate",
                                                children: report.name
                                            }, void 0, false, {
                                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                lineNumber: 93,
                                                columnNumber: 21
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                        lineNumber: 76,
                                        columnNumber: 19
                                    }, this),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "absolute right-1 top-1/2 -translate-y-1/2",
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                type: "button",
                                                "aria-label": `Actions for ${report.name}`,
                                                "aria-haspopup": "menu",
                                                "aria-expanded": menuFor === report.id,
                                                onClick: ()=>setMenuFor(menuFor === report.id ? null : report.id),
                                                className: `flex size-8 items-center justify-center rounded-full text-pp-muted hover:bg-white hover:text-pp-navy ${menuFor === report.id ? 'opacity-100' : 'opacity-0 focus-visible:opacity-100 group-hover:opacity-100'}`,
                                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MoreIcon"], {}, void 0, false, {
                                                    fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                    lineNumber: 107,
                                                    columnNumber: 21
                                                }, this)
                                            }, void 0, false, {
                                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                lineNumber: 97,
                                                columnNumber: 19
                                            }, this),
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Menu"], {
                                                open: menuFor === report.id,
                                                onClose: ()=>setMenuFor(null),
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MenuItem"], {
                                                        onClick: ()=>{
                                                            setMenuFor(null);
                                                            setRenaming(report.id);
                                                        },
                                                        children: "Rename"
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                        lineNumber: 110,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MenuItem"], {
                                                        onClick: ()=>{
                                                            setMenuFor(null);
                                                            onDuplicate(report.id);
                                                        },
                                                        children: "Duplicate"
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                        lineNumber: 118,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["MenuItem"], {
                                                        danger: true,
                                                        onClick: ()=>{
                                                            setMenuFor(null);
                                                            onDelete(report.id);
                                                        },
                                                        children: report.builtIn ? 'Reset to default' : 'Delete'
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                        lineNumber: 126,
                                                        columnNumber: 21
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                lineNumber: 109,
                                                columnNumber: 19
                                            }, this)
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                        lineNumber: 96,
                                        columnNumber: 17
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                lineNumber: 66,
                                columnNumber: 15
                            }, this),
                            open && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                                className: "mb-2 ml-[26px] mt-1 space-y-0.5 border-l border-pp-border pl-3",
                                "aria-label": `${report.name} pages`,
                                children: [
                                    pages.map((page)=>{
                                        const selected = active && page.id === selectedPageId;
                                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                            className: "group relative",
                                            children: [
                                                renaming === page.id ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(RenameInput, {
                                                    value: page.title,
                                                    label: "Page name",
                                                    className: "w-full py-1.5 text-sm",
                                                    onDone: (value)=>finishRename(value, (title)=>onRenamePage(page.id, title)),
                                                    onCancel: ()=>setRenaming(null)
                                                }, void 0, false, {
                                                    fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                    lineNumber: 146,
                                                    columnNumber: 27
                                                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                    type: "button",
                                                    disabled: !ready,
                                                    onClick: ()=>onSelectPage(report.id, page.id),
                                                    onDoubleClick: ()=>active && editing && setRenaming(page.id),
                                                    "aria-current": selected ? 'page' : undefined,
                                                    title: active && editing ? 'Double-click to rename' : undefined,
                                                    className: `block w-full truncate rounded-full py-2 pl-4 pr-8 text-left text-sm transition-colors ${selected ? 'bg-pp-highlight font-semibold text-pp-blue' : 'text-pp-muted hover:bg-pp-canvas hover:text-pp-navy'}`,
                                                    children: page.title
                                                }, void 0, false, {
                                                    fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                    lineNumber: 154,
                                                    columnNumber: 27
                                                }, this),
                                                active && editing && pages.length > 1 && renaming !== page.id && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                                    type: "button",
                                                    "aria-label": `Remove page ${page.title}`,
                                                    title: "Remove page",
                                                    onClick: ()=>onRemovePage(page.id),
                                                    className: "absolute right-1.5 top-1/2 flex size-6 -translate-y-1/2 items-center justify-center rounded-full text-pp-muted opacity-0 hover:bg-white hover:text-pp-danger focus-visible:opacity-100 group-hover:opacity-100",
                                                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["CloseIcon"], {
                                                        className: "size-3.5"
                                                    }, void 0, false, {
                                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                        lineNumber: 176,
                                                        columnNumber: 29
                                                    }, this)
                                                }, void 0, false, {
                                                    fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                    lineNumber: 169,
                                                    columnNumber: 27
                                                }, this)
                                            ]
                                        }, page.id, true, {
                                            fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                            lineNumber: 144,
                                            columnNumber: 23
                                        }, this);
                                    }),
                                    active && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                            type: "button",
                                            disabled: !ready,
                                            onClick: ()=>{
                                                const id = onAddPage();
                                                if (id) setRenaming(id);
                                            },
                                            className: "flex w-full items-center gap-1.5 rounded-full py-2 pl-4 text-left text-sm font-semibold text-pp-blue hover:bg-pp-highlight",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["PlusIcon"], {
                                                    className: "size-4"
                                                }, void 0, false, {
                                                    fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                                    lineNumber: 193,
                                                    columnNumber: 25
                                                }, this),
                                                " Add page"
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                            lineNumber: 184,
                                            columnNumber: 23
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                        lineNumber: 183,
                                        columnNumber: 21
                                    }, this)
                                ]
                            }, void 0, true, {
                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                lineNumber: 140,
                                columnNumber: 17
                            }, this)
                        ]
                    }, report.id, true, {
                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                        lineNumber: 65,
                        columnNumber: 13
                    }, this);
                })
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                lineNumber: 58,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "border-t border-pp-border p-4",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$ui$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        variant: "primary",
                        className: "w-full",
                        onClick: onCreate,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$ui$2f$icons$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["PlusIcon"], {}, void 0, false, {
                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                lineNumber: 205,
                                columnNumber: 11
                            }, this),
                            " New report"
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                        lineNumber: 204,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                        className: "mt-3 text-center text-xs text-pp-muted",
                        children: [
                            "Reports are saved in this browser.",
                            ' ',
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                                type: "button",
                                onClick: onReset,
                                disabled: !ready,
                                className: "font-semibold text-pp-blue hover:underline",
                                children: "Reset demo"
                            }, void 0, false, {
                                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                                lineNumber: 209,
                                columnNumber: 11
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/app/dashboard/components/sidebar.tsx",
                        lineNumber: 207,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/sidebar.tsx",
                lineNumber: 203,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/sidebar.tsx",
        lineNumber: 56,
        columnNumber: 5
    }, this);
}
// Studio moves focus when the selected page changes, so focus on the next frame.
const focusAndSelect = (input)=>{
    if (!input) return;
    requestAnimationFrame(()=>{
        input.focus();
        input.select();
    });
};
function RenameInput({ value, label, className, onDone, onCancel }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
        ref: focusAndSelect,
        defaultValue: value,
        "aria-label": label,
        onBlur: (e)=>onDone(e.currentTarget.value),
        onKeyDown: (e)=>{
            if (e.key === 'Enter') e.currentTarget.blur();
            if (e.key === 'Escape') onCancel();
        },
        className: `rounded-full border border-pp-blue bg-white px-4 font-semibold text-pp-navy outline-none ${className}`
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/sidebar.tsx",
        lineNumber: 241,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/skeleton.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "ContentSkeleton",
    ()=>ContentSkeleton,
    "DashboardSkeleton",
    ()=>DashboardSkeleton,
    "SidebarSkeleton",
    ()=>SidebarSkeleton
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$app$2d$shell$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/app-shell.tsx [app-ssr] (ecmascript)");
;
;
// Placeholder for the dashboard while PayPal data loads (./loading.tsx) and while saved
// reports are read from this browser.
function Skeleton({ className = '' }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: `animate-pulse rounded-lg bg-pp-border/60 ${className}`
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/skeleton.tsx",
        lineNumber: 7,
        columnNumber: 10
    }, this);
}
function SidebarSkeleton() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-3 p-4 pt-6",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                className: "h-3 w-20"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 13,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                className: "h-10 rounded-full"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this),
            [
                'w-28',
                'w-32',
                'w-36',
                'w-24'
            ].map((width)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                    className: `ml-10 h-7 rounded-full ${width}`
                }, width, false, {
                    fileName: "[project]/app/dashboard/components/skeleton.tsx",
                    lineNumber: 16,
                    columnNumber: 9
                }, this)),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                className: "h-10 rounded-full"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 18,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/skeleton.tsx",
        lineNumber: 12,
        columnNumber: 5
    }, this);
}
function ContentSkeleton() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "border-b border-pp-border bg-white px-8 py-5",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                        className: "h-4 w-32"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 27,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                        className: "mt-2 h-8 w-56"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 28,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                        className: "mt-3 h-4 w-48"
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 29,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 26,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "grid flex-1 grid-cols-4 grid-rows-[112px_1fr_1fr] gap-4 p-4",
                "aria-hidden": true,
                children: [
                    [
                        0,
                        1,
                        2,
                        3
                    ].map((i)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "rounded-lg border border-pp-border bg-white p-5",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                                    className: "h-7 w-28"
                                }, void 0, false, {
                                    fileName: "[project]/app/dashboard/components/skeleton.tsx",
                                    lineNumber: 34,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                                    className: "mt-4 h-3 w-16"
                                }, void 0, false, {
                                    fileName: "[project]/app/dashboard/components/skeleton.tsx",
                                    lineNumber: 35,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, i, true, {
                            fileName: "[project]/app/dashboard/components/skeleton.tsx",
                            lineNumber: 33,
                            columnNumber: 11
                        }, this)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "col-span-3 rounded-lg border border-pp-border bg-white p-5",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                            className: "h-full"
                        }, void 0, false, {
                            fileName: "[project]/app/dashboard/components/skeleton.tsx",
                            lineNumber: 39,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 38,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "rounded-lg border border-pp-border bg-white p-5",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                            className: "h-full rounded-full"
                        }, void 0, false, {
                            fileName: "[project]/app/dashboard/components/skeleton.tsx",
                            lineNumber: 42,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 41,
                        columnNumber: 9
                    }, this),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "col-span-4 rounded-lg border border-pp-border bg-white p-5",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Skeleton, {
                            className: "h-full"
                        }, void 0, false, {
                            fileName: "[project]/app/dashboard/components/skeleton.tsx",
                            lineNumber: 45,
                            columnNumber: 11
                        }, this)
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/components/skeleton.tsx",
                        lineNumber: 44,
                        columnNumber: 9
                    }, this)
                ]
            }, void 0, true, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 31,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                className: "sr-only",
                role: "status",
                children: "Loading PayPal data…"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/skeleton.tsx",
                lineNumber: 48,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/skeleton.tsx",
        lineNumber: 25,
        columnNumber: 5
    }, this);
}
function DashboardSkeleton() {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$app$2d$shell$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AppShell"], {
        sidebar: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(SidebarSkeleton, {}, void 0, false, {
            fileName: "[project]/app/dashboard/components/skeleton.tsx",
            lineNumber: 57,
            columnNumber: 24
        }, this),
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(ContentSkeleton, {}, void 0, false, {
            fileName: "[project]/app/dashboard/components/skeleton.tsx",
            lineNumber: 58,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/skeleton.tsx",
        lineNumber: 57,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/ui/icons.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AlertIcon",
    ()=>AlertIcon,
    "BellIcon",
    ()=>BellIcon,
    "CloseIcon",
    ()=>CloseIcon,
    "EditIcon",
    ()=>EditIcon,
    "EyeIcon",
    ()=>EyeIcon,
    "HelpIcon",
    ()=>HelpIcon,
    "InboxIcon",
    ()=>InboxIcon,
    "MoreIcon",
    ()=>MoreIcon,
    "PlusIcon",
    ()=>PlusIcon,
    "RedoIcon",
    ()=>RedoIcon,
    "RefreshIcon",
    ()=>RefreshIcon,
    "ReportIcon",
    ()=>ReportIcon,
    "UndoIcon",
    ()=>UndoIcon
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
;
// 24px stroke icons for the dashboard shell, drawn at 20px by default.
const icon = (paths)=>function Icon({ className = 'size-5', ...props }) {
        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
            viewBox: "0 0 24 24",
            fill: "none",
            stroke: "currentColor",
            strokeWidth: 1.8,
            strokeLinecap: "round",
            strokeLinejoin: "round",
            "aria-hidden": true,
            className: className,
            ...props,
            children: paths
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 8,
            columnNumber: 7
        }, this);
    };
const ReportIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("rect", {
            x: "3",
            y: "3",
            width: "18",
            height: "18",
            rx: "3"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 26,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M8 16v-4M12 16V8M16 16v-6"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 27,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 25,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const PlusIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
    d: "M12 5v14M5 12h14"
}, void 0, false, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 30,
    columnNumber: 30
}, ("TURBOPACK compile-time value", void 0)));
const RefreshIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M20 11a8 8 0 0 0-14.3-4.9L4 8"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 33,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M4 4v4h4M4 13a8 8 0 0 0 14.3 4.9L20 16"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 34,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M20 20v-4h-4"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 35,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 32,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const BellIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M6 9a6 6 0 1 1 12 0c0 6 2.5 7.5 2.5 7.5h-17S6 15 6 9"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 40,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M10 20a2 2 0 0 0 4 0"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 41,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 39,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const HelpIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
            cx: "12",
            cy: "12",
            r: "9"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 46,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17.5h.01"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 47,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 45,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const MoreIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
            cx: "5",
            cy: "12",
            r: "1"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 52,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
            cx: "12",
            cy: "12",
            r: "1"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 53,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
            cx: "19",
            cy: "12",
            r: "1"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 54,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 51,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const UndoIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
    d: "M9 14 4 9l5-5M4 9h10.5a5.5 5.5 0 0 1 0 11H11"
}, void 0, false, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 57,
    columnNumber: 30
}, ("TURBOPACK compile-time value", void 0)));
const RedoIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
    d: "m15 14 5-5-5-5M20 9H9.5a5.5 5.5 0 0 0 0 11H13"
}, void 0, false, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 58,
    columnNumber: 30
}, ("TURBOPACK compile-time value", void 0)));
const EyeIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M2.5 12S6 5 12 5s9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 61,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("circle", {
            cx: "12",
            cy: "12",
            r: "3"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 62,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 60,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const EditIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M4 20h4L19 9a2.8 2.8 0 0 0-4-4L4 16z"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 67,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "m13.5 6.5 4 4"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 68,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 66,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const CloseIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
    d: "M6 6l12 12M18 6 6 18"
}, void 0, false, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 71,
    columnNumber: 31
}, ("TURBOPACK compile-time value", void 0)));
const AlertIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M10.3 3.9 2.4 17.5A2 2 0 0 0 4.1 20.5h15.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 74,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M12 9v4M12 17h.01"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 75,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 73,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
const InboxIcon = icon(/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
    children: [
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M3 13h5l1.5 3h5L16 13h5"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 80,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0)),
        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
            d: "M5.5 5h13L21 13v5a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-5z"
        }, void 0, false, {
            fileName: "[project]/app/dashboard/components/ui/icons.tsx",
            lineNumber: 81,
            columnNumber: 5
        }, ("TURBOPACK compile-time value", void 0))
    ]
}, void 0, true, {
    fileName: "[project]/app/dashboard/components/ui/icons.tsx",
    lineNumber: 79,
    columnNumber: 3
}, ("TURBOPACK compile-time value", void 0)));
}),
"[project]/app/dashboard/components/ui/logo.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AgStudioLogo",
    ()=>AgStudioLogo
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
;
function AgStudioLogo(props) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
        viewBox: "0 0 304 70",
        fill: "none",
        xmlns: "http://www.w3.org/2000/svg",
        role: "img",
        "aria-label": "AG Studio",
        ...props,
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M229.665 46.9718L237.537 46.9853H242.035V42.4872L246.524 37.989L229.665 37.9361V46.9718ZM240.91 33.4908H251.031L255.529 33.4931V28.9927L260.027 24.4945H240.91V33.4908ZM235.288 11H269.024V19.9963H235.288V11Z",
                fill: "#B4BBBF"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 7,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M237.537 46.9968L242.035 42.4874H257.779V51.4838H237.537V46.9968Z",
                fill: "#FF0000"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 8,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M271.273 37.9891V28.9984H255.529L246.524 37.9891H271.273Z",
                fill: "#FF8B00"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 9,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M288.141 15.4982H269.024L260.028 24.4945H288.141V15.4982Z",
                fill: "#55B2C6"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 10,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M38.6102 45.2504H24.6433L22.185 51.2724H16L28.9425 20.9635H34.3077L47.2502 51.2724H41.0651L38.6069 45.2504H38.6102ZM36.6861 40.4598L31.6481 28.1314L26.609 40.4598H36.6861ZM79.4461 34.1916H65.6422V38.9856H73.4668C73.2194 41.3876 72.3198 43.305 70.7645 44.7388C69.2093 46.1714 67.1592 46.89 64.6211 46.89C63.1738 46.89 61.8558 46.6314 60.6672 46.1118C59.5037 45.6116 58.4627 44.8645 57.6163 43.9223C56.7695 42.9811 56.1139 41.8475 55.6494 40.5228C55.1861 39.1981 54.9522 37.7306 54.9522 36.1191C54.9522 34.5087 55.1828 33.0412 55.6494 31.7153C56.1139 30.3906 56.7695 29.2582 57.6163 28.3158C58.4682 27.3709 59.5164 26.6236 60.6874 26.1263C61.8873 25.6068 63.2121 25.3492 64.6627 25.3492C67.6608 25.3492 69.938 26.0712 71.4933 27.514L75.1818 23.8255C72.3895 21.6495 68.8573 20.5587 64.5795 20.5587C62.2045 20.5587 60.0599 20.9354 58.1493 21.6843C56.2387 22.4344 54.6002 23.487 53.2339 24.8364C51.8665 26.1893 50.8172 27.821 50.0784 29.7316C49.3385 31.6422 48.973 33.7733 48.973 36.1225C48.973 38.4728 49.3497 40.5689 50.0987 42.493C50.8487 44.4171 51.9092 46.0567 53.2721 47.4096C54.6385 48.7624 56.2736 49.8116 58.1876 50.5651C60.0993 51.314 62.2292 51.6907 64.5795 51.6907C66.9287 51.6907 68.9405 51.314 70.7848 50.5651C72.6302 49.815 74.1989 48.7624 75.4955 47.4096C76.7933 46.0567 77.7896 44.4171 78.4868 42.493C79.1852 40.5689 79.5338 38.4447 79.5338 36.1225C79.5333 35.4802 79.5052 34.8382 79.4495 34.1983L79.4461 34.1916Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 11,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                fillRule: "evenodd",
                clipRule: "evenodd",
                d: "M184.923 19.3698H190.5V25.9473H184.923V19.3698ZM184.923 28.9284H190.5V51.3259H184.923V28.9284Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 12,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                fillRule: "evenodd",
                clipRule: "evenodd",
                d: "M102.143 20.3181C102.945 20.3181 103.76 20.3873 104.588 20.5253C105.332 20.6216 106.046 20.76 106.729 20.9405L107.021 21.0208C107.794 21.2417 108.527 21.5182 109.219 21.8503C109.845 22.1158 110.411 22.4135 110.915 22.7446L111.128 22.889L111.295 23.0057L108.665 27.3738L108.477 27.2527C107.494 26.623 106.527 26.1489 105.575 25.8285L105.385 25.7667L105.38 25.7648C104.365 25.4178 103.382 25.2459 102.429 25.2459C101.684 25.246 101.027 25.3392 100.453 25.5216C99.9028 25.7055 99.4213 25.9531 99.0071 26.2637C98.5964 26.5718 98.2775 26.9422 98.0482 27.3753L98.0458 27.3806C97.8209 27.7805 97.7064 28.2329 97.7064 28.7432L97.7103 28.9041C97.7269 29.2226 97.7937 29.5257 97.9096 29.8144L97.9719 29.9578C98.1471 30.3332 98.4396 30.7187 98.8593 31.1127C99.2799 31.4803 99.8235 31.8524 100.494 32.2277C101.192 32.6034 102.04 32.9941 103.041 33.3996L104.469 33.9715L104.471 33.972C107.071 35.0392 108.971 36.2527 110.146 37.6228C111.355 39.0006 111.956 40.7005 111.956 42.7072L111.953 42.9611C111.924 44.2232 111.675 45.3809 111.202 46.4311C110.699 47.5483 109.986 48.5125 109.065 49.3224L109.062 49.3248C108.14 50.1064 107.041 50.7182 105.767 51.1614L105.763 51.1624C104.486 51.5788 103.074 51.7858 101.53 51.7858C99.7213 51.7858 97.9367 51.5072 96.1776 50.9504L95.826 50.8352L95.8231 50.8342C94.0679 50.2147 92.5724 49.3993 91.3407 48.3854L91.098 48.1802L90.9551 48.0557L93.7662 43.7274L93.9548 43.8889C95.0527 44.826 96.2289 45.5479 97.4832 46.0557C98.7668 46.537 100.048 46.7768 101.326 46.7768C102.928 46.7768 104.184 46.4162 105.115 45.7177L105.118 45.7162C106.071 45.0204 106.538 44.1179 106.538 42.9932C106.538 42.1126 106.207 41.3424 105.527 40.6746L105.386 40.5424L105.383 40.54C104.672 39.8777 103.482 39.2009 101.795 38.5156L101.451 38.3785L101.448 38.3775L100.142 37.8465C97.518 36.7864 95.577 35.6018 94.3405 34.2841L94.2228 34.1563C92.9852 32.778 92.3706 31.0636 92.3706 29.0291C92.3706 27.7248 92.5925 26.5386 93.0407 25.474L93.0416 25.4716C93.5168 24.3815 94.1892 23.4563 95.0582 22.6994C95.9251 21.9443 96.9575 21.3594 98.1513 20.943C99.3483 20.5254 100.68 20.3181 102.143 20.3181Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 13,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                fillRule: "evenodd",
                clipRule: "evenodd",
                d: "M138.014 40.997C138.014 42.7866 138.505 44.2357 139.348 45.2329C140.188 46.226 141.394 46.7903 142.869 46.7904C144.414 46.7903 145.652 46.2135 146.508 45.2149C147.368 44.2122 147.858 42.7638 147.858 40.997V29.4788H153.156V41.8027C153.133 44.7408 152.084 47.2275 150.258 48.979C148.433 50.73 145.847 51.7303 142.78 51.7303C139.736 51.7303 137.216 50.7524 135.456 49.0097C133.696 47.2668 132.717 44.7797 132.717 41.8013V29.4788H138.014V40.997Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 14,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                fillRule: "evenodd",
                clipRule: "evenodd",
                d: "M205.695 28.7509C212.358 28.7509 217.671 33.8804 217.671 40.3076C217.671 46.7349 212.359 51.8652 205.695 51.8652C199.031 51.865 193.718 46.7348 193.718 40.3076C193.718 33.8805 199.031 28.7511 205.695 28.7509ZM205.695 33.4023C201.966 33.4024 199 36.4409 198.999 40.3076L199.001 40.4892C199.092 44.2694 202.024 47.2136 205.695 47.2138C209.464 47.2138 212.391 44.1754 212.391 40.3076C212.391 36.4399 209.464 33.4023 205.695 33.4023Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 15,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M129.037 28.9284H124.761V22.7435H119.193V28.9284H114.96V34.0541H119.193V51.4193H124.761V34.0541H128.994L129.037 28.9284Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 16,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("path", {
                d: "M179.889 19.3698V51.3259H174.528L174.385 47.9658C173.602 49.1055 172.577 50.0576 171.382 50.7535C170.167 51.3968 168.665 51.7544 166.949 51.7544C165.448 51.7544 164.019 51.4687 162.803 50.9683C161.517 50.3959 160.372 49.6818 159.443 48.681C158.476 47.6465 157.723 46.4318 157.226 45.1061C156.655 43.7476 156.44 42.1755 156.44 40.4595C156.44 38.7434 156.726 37.1713 157.226 35.7409C157.799 34.3116 158.514 33.096 159.443 32.0951C160.372 31.0943 161.517 30.3082 162.803 29.7358C164.09 29.1634 165.448 28.8778 166.949 28.8778C168.665 28.8778 170.095 29.1634 171.31 29.8078C172.526 30.451 173.527 31.3091 174.313 32.5236V19.4418H179.889V19.3698ZM168.165 46.9649C170.024 46.9649 171.453 46.3217 172.597 45.1061C173.74 43.8904 174.313 42.2464 174.313 40.2447C174.313 38.243 173.74 36.6698 172.597 35.3833C171.453 34.1677 170.024 33.5244 168.165 33.5244C166.377 33.5244 164.876 34.1677 163.804 35.3833C162.66 36.5989 162.088 38.243 162.088 40.2447C162.088 42.2464 162.66 43.8196 163.804 45.0341C164.948 46.3217 166.377 46.9649 168.165 46.9649Z",
                fill: "#003264"
            }, void 0, false, {
                fileName: "[project]/app/dashboard/components/ui/logo.tsx",
                lineNumber: 17,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/components/ui/logo.tsx",
        lineNumber: 6,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/components/ui/ui.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Button",
    ()=>Button,
    "Dialog",
    ()=>Dialog,
    "IconButton",
    ()=>IconButton,
    "Menu",
    ()=>Menu,
    "MenuItem",
    ()=>MenuItem
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
'use client';
;
;
const VARIANTS = {
    primary: 'bg-pp-blue text-white hover:bg-pp-blue-dark disabled:bg-pp-border disabled:text-pp-muted',
    secondary: 'border border-pp-navy text-pp-navy hover:bg-pp-highlight disabled:border-pp-border disabled:text-pp-muted',
    ghost: 'text-pp-blue hover:bg-pp-highlight disabled:text-pp-muted',
    danger: 'bg-pp-danger text-white hover:brightness-90'
};
function Button({ variant = 'secondary', size = 'md', className = '', ...props }) {
    const sizing = size === 'sm' ? 'h-8 px-4 text-sm' : 'h-10 px-5 text-[15px]';
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        type: "button",
        className: `inline-flex shrink-0 items-center justify-center gap-2 rounded-full font-semibold transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-pp-blue disabled:cursor-not-allowed ${sizing} ${VARIANTS[variant]} ${className}`,
        ...props
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/ui/ui.tsx",
        lineNumber: 25,
        columnNumber: 5
    }, this);
}
function IconButton({ label, className = '', ...props }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        type: "button",
        "aria-label": label,
        title: label,
        className: `inline-flex size-9 shrink-0 items-center justify-center rounded-full text-pp-navy transition-colors hover:bg-pp-highlight focus-visible:outline-2 focus-visible:outline-pp-blue disabled:cursor-not-allowed disabled:text-pp-border disabled:hover:bg-transparent ${className}`,
        ...props
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/ui/ui.tsx",
        lineNumber: 35,
        columnNumber: 5
    }, this);
}
function Dialog({ open, title, children, actions, onClose }) {
    const ref = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const dialog = ref.current;
        if (!dialog) return;
        if (open && !dialog.open) dialog.showModal();
        if (!open && dialog.open) dialog.close();
    }, [
        open
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("dialog", {
        ref: ref,
        onClose: onClose,
        onClick: (event)=>event.target === ref.current && onClose(),
        className: "m-auto w-[min(440px,calc(100vw-32px))] rounded-lg bg-white p-0 font-paypal text-pp-ink shadow-xl backdrop:bg-pp-navy/40",
        children: open && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "p-6",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-xl font-semibold text-pp-navy",
                    children: title
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/ui/ui.tsx",
                    lineNumber: 75,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "mt-3 text-[15px] text-pp-muted",
                    children: children
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/ui/ui.tsx",
                    lineNumber: 76,
                    columnNumber: 11
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "mt-6 flex flex-wrap justify-end gap-3",
                    children: actions
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/components/ui/ui.tsx",
                    lineNumber: 77,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/app/dashboard/components/ui/ui.tsx",
            lineNumber: 74,
            columnNumber: 9
        }, this)
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/ui/ui.tsx",
        lineNumber: 67,
        columnNumber: 5
    }, this);
}
function Menu({ open, onClose, children }) {
    const ref = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    // Callers pass a new onClose each render; this keeps the listeners below from re-attaching.
    const close = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffectEvent"])(onClose);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (!open) return;
        const onPointer = (event)=>{
            if (!ref.current?.contains(event.target)) close();
        };
        const onKey = (event)=>event.key === 'Escape' && close();
        document.addEventListener('pointerdown', onPointer);
        document.addEventListener('keydown', onKey);
        return ()=>{
            document.removeEventListener('pointerdown', onPointer);
            document.removeEventListener('keydown', onKey);
        };
    }, [
        open
    ]);
    if (!open) return null;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        ref: ref,
        role: "menu",
        className: "absolute right-0 top-full z-20 mt-1 w-48 overflow-hidden rounded-md border border-pp-border bg-white py-1 shadow-lg",
        children: children
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/ui/ui.tsx",
        lineNumber: 112,
        columnNumber: 5
    }, this);
}
function MenuItem({ danger, ...props }) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        type: "button",
        role: "menuitem",
        className: `block w-full px-4 py-2 text-left text-sm hover:bg-pp-highlight ${danger ? 'text-pp-danger' : 'text-pp-ink'}`,
        ...props
    }, void 0, false, {
        fileName: "[project]/app/dashboard/components/ui/ui.tsx",
        lineNumber: 124,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/dashboard.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Dashboard",
    ()=>Dashboard
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
// The dashboard: the PayPal shell (./components) wrapped around a single AG Studio instance, which
// this file renders. Studio's configuration (data sources, theme, default report, AI) lives in
// ./studio. The shell owns saved reports, page names and navigation; Studio owns
// the report being edited. They meet in two places:
//   - the shell drives Studio through its AgStudioApi (setState, getState, undo, redo)
//   - Studio reports every change back through onStateUpdated, which only redraws the shell
//
// Nothing tracks edits as they happen. Save reads the report from Studio with getState(), and
// leaving a report compares Studio's state with the saved one there and then.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/ag-studio/dist/package/main.esm.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2d$react$2f$dist$2f$package$2f$index$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/ag-studio-react/dist/package/index.esm.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$app$2d$shell$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/app-shell.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$dialogs$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/dialogs.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$empty$2d$data$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/empty-data.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$report$2d$header$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/report-header.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/reports-store.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$page$2d$titles$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/page-titles.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$sidebar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/sidebar.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$skeleton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/components/skeleton.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/report-state.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$ai$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/studio/ai.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$data$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/studio/data.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$theme$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/studio/theme.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$use$2d$reports$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/use-reports.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
;
if ("TURBOPACK compile-time truthy", 1) {
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["enableStudioDevValidations"])();
}
const NO_HISTORY = {
    canUndo: false,
    canRedo: false
};
const noSubscription = ()=>()=>{};
function Dashboard(props) {
    // Saved reports live in localStorage, which only exists in the browser.
    const inBrowser = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useSyncExternalStore"])(noSubscription, ()=>true, ()=>false);
    return inBrowser ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(ReportsDashboard, {
        ...props
    }, void 0, false, {
        fileName: "[project]/app/dashboard/dashboard.tsx",
        lineNumber: 77,
        columnNumber: 22
    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$skeleton$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["DashboardSkeleton"], {}, void 0, false, {
        fileName: "[project]/app/dashboard/dashboard.tsx",
        lineNumber: 77,
        columnNumber: 56
    }, this);
}
function ReportsDashboard({ data, licenseKey, aiModels }) {
    const { store, latest, update, editReport } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$use$2d$reports$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useReports"])();
    const apiRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    // The open report as it is in Studio now, unsaved edits included, for drawing the shell.
    // Null until Studio is ready.
    const [studioState, setStudioState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [history, setHistory] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(NO_HISTORY);
    const [mode, setMode] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])('view');
    const [dialog, setDialog] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const { reports } = store;
    // The open report, as it was last saved.
    const saved = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(reports, store.activeId) ?? reports[0];
    // Studio reads initialState once, when it is created, and starts on the open report; after that,
    // its state is read from Studio.
    const [initialState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(()=>__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["withFiltersPanelFor"]('view', saved.state));
    const state = studioState ?? initialState;
    const studioData = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useMemo"])(()=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$data$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["buildStudioData"])(data), [
        data
    ]);
    // `ai` is read once, when Studio is created.
    const ai = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useMemo"])(()=>aiModels?.length ? (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$ai$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["buildAi"])(aiModels) : undefined, [
        aiModels
    ]);
    // --- Driving Studio ---------------------------------------------------------------
    const load = (report, selectedPageId = report.state.selectedPageId, nextMode = mode)=>{
        const api = apiRef.current;
        if (!api) return;
        api.setState(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["withFiltersPanelFor"](nextMode, {
            ...report.state,
            selectedPageId
        }));
        // Undo shouldn't step back into the previous report.
        api.clearHistory();
        setStudioState(api.getState());
        setHistory(NO_HISTORY);
        setMode(nextMode);
        update((current)=>({
                ...current,
                activeId: report.id
            }));
    };
    const updateState = (next)=>{
        const api = apiRef.current;
        if (api) api.setState(next(api.getState()));
    };
    const changeMode = (next)=>{
        updateState((s)=>__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["withFiltersPanelFor"](next, s));
        setMode(next);
    };
    // --- Saving -----------------------------------------------------------------------
    const save = ()=>{
        const api = apiRef.current;
        if (!api) return;
        const current = api.getState();
        editReport(saved.id, (report)=>({
                ...report,
                // Titles for exactly the pages being saved.
                pageTitles: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$page$2d$titles$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["pageTitlesFor"])({
                    pageTitles: report.pageTitles,
                    state: current
                }),
                state: current,
                updatedAt: new Date().toISOString()
            }));
        console.log('[AG Studio] saved report', saved.name, current);
    };
    const discard = ()=>load(saved, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["pageToSelect"](saved.state, state.selectedPageId));
    // Anything that leaves the current report or edit mode asks first when it has unsaved changes.
    const guard = (then)=>{
        const api = apiRef.current;
        if (api && __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["hasChanges"](api.getState(), saved.state)) {
            setDialog({
                kind: 'unsaved',
                then
            });
        } else then();
    };
    // --- Reports ----------------------------------------------------------------------
    const openReport = (id)=>{
        const report = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(reports, id);
        if (report && id !== saved.id) guard(()=>load(report));
    };
    const createReport = (name)=>{
        const report = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["blankReport"])(name);
        update((current)=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["upsert"])(current, report));
        load(report, report.state.selectedPageId, 'edit');
    };
    const duplicateReport = (id)=>guard(()=>{
            const source = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(reports, id);
            if (!source) return;
            const copy = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["copyOf"])(source);
            update((current)=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["upsert"])(current, copy));
            load(copy);
        });
    const resetDemo = ()=>{
        update(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["initialReports"]);
        load((0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["defaultReport"])(), undefined, 'view');
    };
    const deleteReport = (report)=>{
        update((current)=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["remove"])(current, report.id));
        if (report.id !== saved.id) return;
        const { reports: next, activeId } = latest();
        load((0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(next, activeId) ?? next[0]);
    };
    const renameReport = (id, name)=>editReport(id, (report)=>({
                ...report,
                name
            }));
    // --- Pages ------------------------------------------------------------------------
    // Studio leaves page navigation to the host, and its state has no page names. Page names are
    // saved as soon as they change; new pages are numbered until they're named.
    const selectPage = (id, pageId)=>{
        if (id === saved.id) updateState((s)=>__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["selectPage"](s, pageId));
        else {
            const report = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(reports, id);
            if (report) guard(()=>load(report, pageId));
        }
    };
    const addPage = ()=>{
        const id = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["newId"])('page');
        updateState((s)=>__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["addPage"](s, id));
        // A new page is empty, so open edit mode to fill it.
        if (mode !== 'edit') changeMode('edit');
        return id;
    };
    const removePage = (id)=>updateState((s)=>__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["removePage"](s, id));
    const renamePage = (id, title)=>editReport(saved.id, (report)=>({
                ...report,
                pageTitles: {
                    ...report.pageTitles,
                    [id]: title
                }
            }));
    const editing = mode === 'edit';
    const pages = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$page$2d$titles$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["pagesFor"])({
        pageTitles: saved.pageTitles,
        state
    });
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$app$2d$shell$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AppShell"], {
        sidebar: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$sidebar$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ReportsSidebar"], {
            reports: reports,
            activeId: saved.id,
            activePages: pages,
            selectedPageId: state.selectedPageId,
            editing: editing,
            ready: studioState !== null,
            onSelectReport: openReport,
            onSelectPage: selectPage,
            onAddPage: ()=>apiRef.current ? addPage() : undefined,
            onRemovePage: removePage,
            onRenamePage: renamePage,
            onRenameReport: renameReport,
            onCreate: ()=>guard(()=>setDialog({
                        kind: 'create'
                    })),
            onDuplicate: duplicateReport,
            onDelete: (id)=>{
                const report = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(reports, id);
                if (report) setDialog({
                    kind: 'delete',
                    report
                });
            },
            onReset: ()=>setDialog({
                    kind: 'reset'
                })
        }, void 0, false, {
            fileName: "[project]/app/dashboard/dashboard.tsx",
            lineNumber: 218,
            columnNumber: 9
        }, this),
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$report$2d$header$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ReportHeader"], {
                reportName: saved.name,
                pageTitle: pages.find((p)=>p.id === state.selectedPageId)?.title,
                asOf: data.asOf,
                editing: editing,
                pageIsEmpty: studioState !== null && !__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$report$2d$state$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["pageHasWidgets"](state),
                canUndo: history.canUndo,
                canRedo: history.canRedo,
                onUndo: ()=>apiRef.current?.undo(),
                onRedo: ()=>apiRef.current?.redo(),
                onSave: save,
                onDiscard: discard,
                onEditingChange: (next)=>next ? changeMode('edit') : guard(()=>changeMode('view'))
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 241,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "min-h-0 flex-1",
                children: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$data$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["hasData"])(data) ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2d$react$2f$dist$2f$package$2f$index$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AgStudioProvider"], {
                    licenseKey: licenseKey,
                    modules: ai ? [
                        __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AgStudioAiModule"]
                    ] : undefined,
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2d$react$2f$dist$2f$package$2f$index$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AgStudio"], {
                        style: {
                            height: '100%',
                            width: '100%'
                        },
                        theme: __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$theme$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["agStudioPayPalTheme"],
                        layout: {
                            widgetBorderEnabled: true
                        },
                        data: studioData,
                        ai: ai,
                        initialState: initialState,
                        mode: mode,
                        onApiReady: (event)=>{
                            apiRef.current = event.api;
                        },
                        onStudioReady: (event)=>{
                            const current = event.api.getState();
                            console.log('[AG Studio] initial state', current);
                            setStudioState(current);
                        },
                        onStateUpdated: (event)=>{
                            console.log('[AG Studio] state updated', event.state);
                            const { undo, redo } = event.api.getHistory();
                            setStudioState(event.state);
                            setHistory({
                                canUndo: undo.length > 0,
                                canRedo: redo.length > 0
                            });
                        }
                    }, void 0, false, {
                        fileName: "[project]/app/dashboard/dashboard.tsx",
                        lineNumber: 261,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/app/dashboard/dashboard.tsx",
                    lineNumber: 260,
                    columnNumber: 11
                }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$empty$2d$data$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["EmptyData"], {}, void 0, false, {
                    fileName: "[project]/app/dashboard/dashboard.tsx",
                    lineNumber: 286,
                    columnNumber: 11
                }, this)
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 258,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$dialogs$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["UnsavedChangesDialog"], {
                open: dialog?.kind === 'unsaved',
                reportName: saved.name,
                onCancel: ()=>setDialog(null),
                onDiscard: ()=>{
                    discard();
                    if (dialog?.kind === 'unsaved') dialog.then();
                    setDialog(null);
                },
                onSave: ()=>{
                    save();
                    if (dialog?.kind === 'unsaved') dialog.then();
                    setDialog(null);
                }
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 290,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$dialogs$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["CreateReportDialog"], {
                open: dialog?.kind === 'create',
                onClose: ()=>setDialog(null),
                onCreate: (name)=>{
                    setDialog(null);
                    createReport(name);
                }
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 305,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$dialogs$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["DeleteReportDialog"], {
                report: dialog?.kind === 'delete' ? dialog.report : null,
                onCancel: ()=>setDialog(null),
                onConfirm: (report)=>{
                    deleteReport(report);
                    setDialog(null);
                }
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 313,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$components$2f$dialogs$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ResetDemoDialog"], {
                open: dialog?.kind === 'reset',
                builtInName: (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["defaultReport"])().name,
                onCancel: ()=>setDialog(null),
                onConfirm: ()=>{
                    resetDemo();
                    setDialog(null);
                }
            }, void 0, false, {
                fileName: "[project]/app/dashboard/dashboard.tsx",
                lineNumber: 321,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/app/dashboard/dashboard.tsx",
        lineNumber: 216,
        columnNumber: 5
    }, this);
}
}),
"[project]/app/dashboard/page-titles.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Page titles for the sidebar and header. Studio's state has no page names, so each report
// keeps its own map of page id -> title. Pages without a saved title are numbered by position.
__turbopack_context__.s([
    "pageTitle",
    ()=>pageTitle,
    "pageTitlesFor",
    ()=>pageTitlesFor,
    "pagesFor",
    ()=>pagesFor
]);
const pageTitle = (report, pageId)=>report.pageTitles[pageId] ?? `Page ${report.state.pages.findIndex((page)=>page.id === pageId) + 1}`;
const pagesFor = (report)=>report.state.pages.map((page)=>({
            id: page.id,
            title: pageTitle(report, page.id)
        }));
const pageTitlesFor = (report)=>Object.fromEntries(pagesFor(report).map((page)=>[
            page.id,
            page.title
        ]));
}),
"[project]/app/dashboard/report-state.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Pure helpers over AG Studio's report state (AgReportState). The shell uses these to check for
// unsaved changes and to edit pages; none of them touch the Studio API.
__turbopack_context__.s([
    "addPage",
    ()=>addPage,
    "hasChanges",
    ()=>hasChanges,
    "pageHasWidgets",
    ()=>pageHasWidgets,
    "pageToSelect",
    ()=>pageToSelect,
    "removePage",
    ()=>removePage,
    "selectPage",
    ()=>selectPage,
    "withFiltersPanelFor",
    ()=>withFiltersPanelFor
]);
const hasChanges = (state, saved)=>durable(state) !== durable(saved);
const durable = (state)=>JSON.stringify({
        schema: state.schema,
        pages: state.pages.map(({ id, widgets, widgetLayout, layout, filter })=>({
                id,
                widgets,
                widgetLayout,
                layout,
                filter
            }))
    });
const withFiltersPanelFor = (mode, state)=>({
        ...state,
        panels: {
            ...state.panels,
            filters: {
                ...state.panels?.filters,
                collapsed: mode === 'edit'
            }
        }
    });
const selectPage = (state, pageId)=>({
        ...state,
        selectedPageId: pageId
    });
const pageToSelect = (state, preferredPageId)=>state.pages.some((p)=>p.id === preferredPageId) ? preferredPageId : state.selectedPageId;
const addPage = (state, pageId)=>({
        ...state,
        pages: [
            ...state.pages,
            {
                id: pageId
            }
        ],
        selectedPageId: pageId
    });
const removePage = (state, pageId)=>{
    const index = state.pages.findIndex((p)=>p.id === pageId);
    const pages = state.pages.filter((p)=>p.id !== pageId);
    const selectedPageId = state.selectedPageId === pageId ? pages[Math.max(0, index - 1)].id : state.selectedPageId;
    return {
        ...state,
        pages,
        selectedPageId
    };
};
const pageHasWidgets = (state)=>Object.keys(state.pages.find((p)=>p.id === state.selectedPageId)?.widgets ?? {}).length > 0;
}),
"[project]/app/dashboard/reports-store.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Saved reports, kept in this browser's localStorage. Studio's state has no page names, so each
// report carries its page titles alongside the AG Studio state.
//
// The built-in report comes from ./studio/initial-report.ts until it is saved;
// after that the saved copy wins until it is reset to default.
__turbopack_context__.s([
    "BUILT_IN_ID",
    ()=>BUILT_IN_ID,
    "blankReport",
    ()=>blankReport,
    "copyOf",
    ()=>copyOf,
    "defaultReport",
    ()=>defaultReport,
    "findReport",
    ()=>findReport,
    "initialReports",
    ()=>initialReports,
    "loadReports",
    ()=>loadReports,
    "newId",
    ()=>newId,
    "remove",
    ()=>remove,
    "saveReports",
    ()=>saveReports,
    "upsert",
    ()=>upsert
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$initial$2d$report$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/studio/initial-report.ts [app-ssr] (ecmascript)");
;
const STORAGE_KEY = 'hope-admin:reports:v1';
const BUILT_IN_ID = 'hope-financial-overview';
// Sidebar titles for the built-in report's pages, keyed by page id in initial-report.ts.
const defaultPageTitles = {
    overview: 'Financial Overview',
    donations: 'Donations History',
    payouts: 'Beneficiary Payouts'
};
const defaultReport = ()=>({
        id: BUILT_IN_ID,
        name: 'Hope Financial Overview',
        builtIn: true,
        pageTitles: defaultPageTitles,
        state: __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$initial$2d$report$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["dashboardReport"],
        updatedAt: new Date(0).toISOString()
    });
const newId = (prefix)=>`${prefix}-${crypto.randomUUID().slice(0, 8)}`;
function blankReport(name) {
    const pageId = newId('page');
    return {
        id: newId('report'),
        name,
        pageTitles: {
            [pageId]: 'Page 1'
        },
        state: {
            selectedPageId: pageId,
            pages: [
                {
                    id: pageId
                }
            ]
        },
        updatedAt: new Date().toISOString()
    };
}
const copyOf = (source)=>({
        ...source,
        id: newId('report'),
        name: `${source.name} (copy)`,
        builtIn: undefined,
        updatedAt: new Date().toISOString()
    });
const findReport = (reports, id)=>reports.find((r)=>r.id === id);
function upsert(current, report) {
    const exists = current.reports.some((r)=>r.id === report.id);
    const reports = exists ? current.reports.map((r)=>r.id === report.id ? report : r) : [
        ...current.reports,
        report
    ];
    return {
        ...current,
        reports
    };
}
function remove(current, id) {
    if (id === BUILT_IN_ID) return upsert(current, defaultReport());
    const reports = current.reports.filter((r)=>r.id !== id);
    return {
        reports,
        activeId: current.activeId === id ? BUILT_IN_ID : current.activeId
    };
}
const initialReports = ()=>({
        reports: [
            defaultReport()
        ],
        activeId: BUILT_IN_ID
    });
function loadReports() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) return initialReports();
        const stored = JSON.parse(raw);
        // The built-in report is always listed first, from code unless a saved copy exists.
        const reports = [
            stored.reports.find((r)=>r.id === BUILT_IN_ID) ?? defaultReport(),
            ...stored.reports.filter((r)=>r.id !== BUILT_IN_ID)
        ];
        const activeId = reports.some((r)=>r.id === stored.activeId) ? stored.activeId : BUILT_IN_ID;
        return {
            reports,
            activeId
        };
    } catch  {
        return initialReports();
    }
}
function saveReports(next) {
    // Only keep the built-in report once it differs from code, so edits to initial-report.ts show up.
    const untouched = (r)=>r.id === BUILT_IN_ID && r.state === __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$initial$2d$report$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["dashboardReport"] && r.pageTitles === defaultPageTitles && r.name === defaultReport().name;
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({
            ...next,
            reports: next.reports.filter((r)=>!untouched(r))
        }));
    } catch  {
    // Storage full or blocked: keep working in memory for this session.
    }
}
}),
"[project]/app/dashboard/studio/ai.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "buildAi",
    ()=>buildAi
]);
// The AG Studio AI assistant. The adapter calls `${endpoint}/responses`, i.e. this app's proxy at
// app/api/ai/responses, which holds the OpenAI key, so nothing secret is sent from the browser.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/ag-studio/dist/package/main.esm.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$openai$2d$adapter$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/studio/openai-adapter.ts [app-ssr] (ecmascript)");
;
;
// Suggestions shown in a new AI conversation, before anything has been typed.
const PROMPT_STARTERS = [
    {
        label: 'Summarise this page',
        prompt: 'Summarise what this page shows: every widget, the fields it reads, and what stands out.'
    },
    {
        label: 'Overdue invoices',
        prompt: 'Which customers owe the most on overdue invoices?'
    },
    {
        label: 'Revenue by month',
        prompt: 'Add a chart of paid invoice revenue by month.'
    }
];
function buildAi(models) {
    const adapter = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$studio$2f$openai$2d$adapter$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["openaiAdapter"])({
        endpoint: '/api/ai',
        model: models[0]
    });
    return ({ api })=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createAiHarness"])(api, {
            adapter,
            promptStarters: PROMPT_STARTERS,
            models: models.length > 1 ? models.map((id)=>({
                    id,
                    label: id
                })) : undefined
        });
}
}),
"[project]/app/dashboard/studio/data.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// AG Studio data sources definition for Hope Medical Crowdfunding
__turbopack_context__.s([
    "buildStudioData",
    ()=>buildStudioData,
    "hasData",
    ()=>hasData
]);
const CALENDAR_ID = "calendar";
const fields = (specs)=>specs.map(([id, name, format, hide])=>({
            id,
            name,
            format,
            ...hide && {
                hide
            }
        }));
const onCalendar = (tableId, fieldId, truncate)=>({
        id: `${tableId}-${fieldId}-calendar`,
        source: {
            tableId,
            fieldId
        },
        target: {
            calendarId: CALENDAR_ID
        },
        ...truncate && {
            truncate
        }
    });
const hasData = (data)=>data.donations.length > 0 || data.payouts.length > 0 || data.transactions.length > 0;
function buildStudioData(data) {
    const dates = [
        ...data.donations.map((d)=>d.date),
        ...data.payouts.map((p)=>p.date),
        ...data.transactions.map((t)=>t.date)
    ].filter((d)=>!!d).sort();
    const today = data.asOf.slice(0, 10);
    return {
        description: "Hope medical crowdfunding platform financial analytics: donations, beneficiary payouts, and pooled fund balance.",
        sources: [
            {
                id: "pooledFund",
                name: "Pooled Fund Summary",
                description: "High-level summary of total donations, total payouts, and available pooled balance.",
                data: data.pooledFund,
                fields: fields([
                    [
                        "id",
                        "Fund ID",
                        "textFormat",
                        true
                    ],
                    [
                        "name",
                        "Fund Name",
                        "textFormat"
                    ],
                    [
                        "totalDonations",
                        "Total Donations",
                        "currencyFormat"
                    ],
                    [
                        "totalPayouts",
                        "Total Payouts",
                        "currencyFormat"
                    ],
                    [
                        "availableBalance",
                        "Available Pooled Balance",
                        "currencyFormat"
                    ],
                    [
                        "pendingDonations",
                        "Pending Donations",
                        "currencyFormat"
                    ],
                    [
                        "pendingPayouts",
                        "Pending Payouts",
                        "currencyFormat"
                    ],
                    [
                        "totalTransactions",
                        "Total Transactions",
                        "integerFormat"
                    ]
                ])
            },
            {
                id: "donations",
                name: "Donation Transactions",
                description: "Inbound donor contributions received through PayPal Orders API.",
                data: data.donations,
                fields: fields([
                    [
                        "id",
                        "ID",
                        "textFormat",
                        true
                    ],
                    [
                        "donorName",
                        "Donor Name",
                        "textFormat"
                    ],
                    [
                        "donorEmail",
                        "Donor Email",
                        "textFormat"
                    ],
                    [
                        "amount",
                        "Donation Amount",
                        "currencyFormat"
                    ],
                    [
                        "currency",
                        "Currency",
                        "textFormat",
                        true
                    ],
                    [
                        "status",
                        "Payment Status",
                        "textFormat"
                    ],
                    [
                        "orderId",
                        "PayPal Order ID",
                        "textFormat"
                    ],
                    [
                        "captureId",
                        "PayPal Capture ID",
                        "textFormat"
                    ],
                    [
                        "date",
                        "Date",
                        "dateFormat"
                    ],
                    [
                        "dateTime",
                        "Timestamp",
                        "dateTimeFormat",
                        true
                    ],
                    [
                        "isCompleted",
                        "Is Completed",
                        "booleanFormat"
                    ]
                ])
            },
            {
                id: "payouts",
                name: "Beneficiary Payouts",
                description: "Outbound payouts sent from Hope merchant account to verified medical beneficiaries.",
                data: data.payouts,
                fields: fields([
                    [
                        "id",
                        "Payout ID",
                        "textFormat",
                        true
                    ],
                    [
                        "beneficiaryName",
                        "Beneficiary",
                        "textFormat"
                    ],
                    [
                        "recipientEmail",
                        "PayPal Recipient Email",
                        "textFormat"
                    ],
                    [
                        "amount",
                        "Payout Amount",
                        "currencyFormat"
                    ],
                    [
                        "currency",
                        "Currency",
                        "textFormat",
                        true
                    ],
                    [
                        "batchStatus",
                        "Batch Status",
                        "textFormat"
                    ],
                    [
                        "itemStatus",
                        "Item Status",
                        "textFormat"
                    ],
                    [
                        "status",
                        "Payout Status",
                        "textFormat"
                    ],
                    [
                        "batchId",
                        "PayPal Batch ID",
                        "textFormat"
                    ],
                    [
                        "itemId",
                        "PayPal Item ID",
                        "textFormat"
                    ],
                    [
                        "date",
                        "Date",
                        "dateFormat"
                    ],
                    [
                        "dateTime",
                        "Timestamp",
                        "dateTimeFormat",
                        true
                    ],
                    [
                        "isSuccess",
                        "Is Success",
                        "booleanFormat"
                    ]
                ])
            },
            {
                id: "transactions",
                name: "Cash Flow Ledger",
                description: "Combined ledger of all inflows (donations) and outflows (payouts).",
                data: data.transactions,
                fields: fields([
                    [
                        "id",
                        "Transaction ID",
                        "textFormat"
                    ],
                    [
                        "type",
                        "Transaction Type",
                        "textFormat"
                    ],
                    [
                        "direction",
                        "Direction",
                        "textFormat"
                    ],
                    [
                        "counterparty",
                        "Donor / Beneficiary",
                        "textFormat"
                    ],
                    [
                        "amount",
                        "Gross Amount",
                        "currencyFormat"
                    ],
                    [
                        "signedAmount",
                        "Net Cash Flow",
                        "currencyFormat"
                    ],
                    [
                        "currency",
                        "Currency",
                        "textFormat",
                        true
                    ],
                    [
                        "status",
                        "Status",
                        "textFormat"
                    ],
                    [
                        "referenceId",
                        "Reference ID",
                        "textFormat"
                    ],
                    [
                        "date",
                        "Date",
                        "dateFormat"
                    ],
                    [
                        "dateTime",
                        "Timestamp",
                        "dateTimeFormat",
                        true
                    ]
                ])
            },
            {
                id: "statusBreakdown",
                name: "Status Breakdown",
                description: "Aggregated counts and amounts by transaction status.",
                data: data.statusBreakdown,
                fields: fields([
                    [
                        "id",
                        "ID",
                        "textFormat",
                        true
                    ],
                    [
                        "category",
                        "Category",
                        "textFormat"
                    ],
                    [
                        "status",
                        "Status",
                        "textFormat"
                    ],
                    [
                        "count",
                        "Transaction Count",
                        "integerFormat"
                    ],
                    [
                        "totalAmount",
                        "Total Amount",
                        "currencyFormat"
                    ]
                ])
            }
        ],
        relationships: [
            onCalendar("donations", "date"),
            onCalendar("payouts", "date"),
            onCalendar("transactions", "date", "day")
        ],
        calendars: [
            {
                id: CALENDAR_ID,
                label: "Calendar",
                range: {
                    from: {
                        type: "date",
                        value: dates[0] ?? today
                    },
                    to: {
                        type: "date",
                        value: dates.at(-1) ?? today
                    }
                },
                fragments: [
                    "year",
                    "quarter",
                    "month",
                    "week",
                    "day",
                    "dayOfWeek"
                ]
            }
        ],
        expressions: [
            {
                id: "payoutRate",
                name: "Payout Distribution Rate",
                description: "Percentage of received donations distributed as payouts.",
                format: "percentageFormat",
                isMeasure: true,
                expression: {
                    operator: "divide",
                    inputs: [
                        {
                            id: "payouts.amount",
                            aggregation: "sum"
                        },
                        {
                            id: "donations.amount",
                            aggregation: "sum"
                        }
                    ]
                }
            }
        ]
    };
}
}),
"[project]/app/dashboard/studio/initial-report.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// The built-in "Hope Financial Overview" report: pages for overview, donations, and payouts.
__turbopack_context__.s([
    "dashboardReport",
    ()=>dashboardReport,
    "initialReport",
    ()=>initialReport
]);
const at = (xTrack, yTrack, xSpan, ySpan)=>({
        xTrack,
        yTrack,
        xSpan,
        ySpan
    });
const title = (text)=>({
        title: {
            enabled: true,
            text
        }
    });
const sum = (id)=>({
        id,
        aggregation: "sum"
    });
const avg = (id)=>({
        id,
        aggregation: "avg"
    });
const countd = (id)=>({
        id,
        aggregation: "countd"
    });
const HOPE_FONT = 'Outfit, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
const typography = (fontSize, fontWeight = "normal")=>({
        fontFamily: HOPE_FONT,
        fontSize,
        fontWeight,
        fontStyle: "normal"
    });
const kpi = (text, value)=>({
        type: "value",
        dataMapping: {
            value: [
                value
            ]
        },
        format: {
            title: {
                enabled: true,
                text,
                typography: typography(14, "bold")
            },
            caption: {
                enabled: true,
                text: "",
                typography: typography(0)
            },
            style: {
                typography: typography(22, "bold")
            }
        }
    });
// --- Overview Page -------------------------------------------------------------
const overview = {
    id: "overview",
    widgets: {
        "kpi-donations": kpi("Total Donations Received", sum("pooledFund.totalDonations")),
        "kpi-payouts": kpi("Total Payouts Made", sum("pooledFund.totalPayouts")),
        "kpi-balance": kpi("Available Pooled Fund", sum("pooledFund.availableBalance")),
        "kpi-pending": kpi("Pending Payouts", sum("pooledFund.pendingPayouts")),
        "status-breakdown-chart": {
            type: "pie-chart",
            dataMapping: {
                categoryKey: [
                    {
                        id: "statusBreakdown.status"
                    }
                ],
                valueKey: [
                    sum("statusBreakdown.totalAmount")
                ]
            },
            format: {
                ...title("Volume by Transaction Status"),
                style: {
                    theme: {
                        common: {
                            legend: {
                                enabled: true
                            }
                        }
                    }
                }
            }
        },
        "cashflow-grid": {
            type: "grid",
            dataMapping: {
                cols: [
                    {
                        id: "transactions.date"
                    },
                    {
                        id: "transactions.type"
                    },
                    {
                        id: "transactions.direction"
                    },
                    {
                        id: "transactions.counterparty"
                    },
                    {
                        id: "transactions.status"
                    },
                    {
                        id: "transactions.amount"
                    },
                    {
                        id: "transactions.signedAmount"
                    },
                    {
                        id: "transactions.referenceId"
                    }
                ]
            },
            format: title("Recent Cash Flow Activity")
        }
    },
    widgetLayout: {
        "kpi-donations": at(0, 0, 6, 7),
        "kpi-payouts": at(6, 0, 6, 7),
        "kpi-balance": at(12, 0, 6, 7),
        "kpi-pending": at(18, 0, 6, 7),
        "status-breakdown-chart": at(0, 7, 8, 20),
        "cashflow-grid": at(8, 7, 16, 20)
    }
};
// --- Donations Page ------------------------------------------------------------
const donations = {
    id: "donations",
    widgets: {
        "kpi-donations-total": kpi("Total Donations Received", sum("donations.amount")),
        "kpi-donations-count": kpi("Donation Transactions", countd("donations.id")),
        "kpi-donations-avg": kpi("Average Donation", avg("donations.amount")),
        "donations-grid": {
            type: "grid",
            dataMapping: {
                cols: [
                    {
                        id: "donations.date"
                    },
                    {
                        id: "donations.donorName"
                    },
                    {
                        id: "donations.donorEmail"
                    },
                    {
                        id: "donations.amount"
                    },
                    {
                        id: "donations.status"
                    },
                    {
                        id: "donations.orderId"
                    },
                    {
                        id: "donations.captureId"
                    }
                ]
            },
            format: title("Inbound Donations (PayPal Orders API)")
        }
    },
    widgetLayout: {
        "kpi-donations-total": at(0, 0, 8, 7),
        "kpi-donations-count": at(8, 0, 8, 7),
        "kpi-donations-avg": at(16, 0, 8, 7),
        "donations-grid": at(0, 7, 24, 22)
    }
};
// --- Payouts Page --------------------------------------------------------------
const payouts = {
    id: "payouts",
    widgets: {
        "kpi-payouts-total": kpi("Total Beneficiary Payouts", sum("payouts.amount")),
        "kpi-payouts-count": kpi("Payout Disbursals", countd("payouts.id")),
        "kpi-payouts-avg": kpi("Average Payout", avg("payouts.amount")),
        "payouts-grid": {
            type: "grid",
            dataMapping: {
                cols: [
                    {
                        id: "payouts.date"
                    },
                    {
                        id: "payouts.beneficiaryName"
                    },
                    {
                        id: "payouts.recipientEmail"
                    },
                    {
                        id: "payouts.amount"
                    },
                    {
                        id: "payouts.status"
                    },
                    {
                        id: "payouts.batchId"
                    },
                    {
                        id: "payouts.itemId"
                    }
                ]
            },
            format: title("Outbound Beneficiary Transfers (PayPal Payouts API)")
        }
    },
    widgetLayout: {
        "kpi-payouts-total": at(0, 0, 8, 7),
        "kpi-payouts-count": at(8, 0, 8, 7),
        "kpi-payouts-avg": at(16, 0, 8, 7),
        "payouts-grid": at(0, 7, 24, 22)
    }
};
const dashboardReport = {
    selectedPageId: overview.id,
    pages: [
        overview,
        donations,
        payouts
    ]
};
const initialReport = dashboardReport;
}),
"[project]/app/dashboard/studio/openai-adapter.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

// Copied verbatim from the AG Studio 3.0.0 docs example (Direct LLM Runner, shared/openaiAdapter.tsx):
// https://www.ag-grid.com/studio/archive/3.0.0/react/ai-adapter/
// Keep it unchanged so it can be diffed against new releases. It runs in the browser, so here it is
// pointed at this app's own proxy (app/api/ai/responses/route.ts) with no key: the server adds it.
// The upstream source uses `any` for untyped OpenAI payloads; lint is relaxed rather than editing it.
/* eslint-disable @typescript-eslint/no-explicit-any, @typescript-eslint/no-unused-vars */ /**
 * OpenAI Responses API adapter for AG Studio.
 *
 * This is example code - copy it into your project and adapt as needed.
 * It maps between AG Studio's AI types and the OpenAI Responses API,
 * handling encoding (AG → OpenAI), decoding (OpenAI → AG), and SSE streaming.
 */ __turbopack_context__.s([
    "openaiAdapter",
    ()=>openaiAdapter
]);
const BANNED_KEYWORDS = [
    'allOf',
    'not',
    'oneOf',
    'if',
    'then',
    'else',
    'prefixItems',
    'patternProperties',
    'propertyNames',
    'unevaluatedProperties',
    'unevaluatedItems',
    'dependentSchemas',
    'dependentRequired',
    'contains'
];
function isSchema(value) {
    return typeof value === 'object' && value !== null && !Array.isArray(value);
}
// Shape encodes "undefined" (used in `union(T, undefined)` to mark optionality) as the
// sentinel `{ not: {} }`. OpenAI doesn't allow `not`, so strip these from any `anyOf`
// branches; the surrounding object handler turns the remaining schema nullable for
// optional properties.
function isUndefinedSentinel(s) {
    if (!isSchema(s)) return false;
    return Object.keys(s).length === 1 && isSchema(s.not) && Object.keys(s.not).length === 0;
}
function stripUndefinedSentinel(schema) {
    if (!Array.isArray(schema.anyOf)) return schema;
    const filtered = schema.anyOf.filter((b)=>!isUndefinedSentinel(b));
    if (filtered.length === schema.anyOf.length) return schema;
    if (filtered.length === 0) {
        throw new Error('toOpenAiSchema: schema reduces to `undefined`-only - nothing to express');
    }
    const { anyOf: _, ...rest } = schema;
    if (filtered.length === 1 && isSchema(filtered[0])) {
        return {
            ...filtered[0],
            ...rest
        };
    }
    return {
        ...rest,
        anyOf: filtered
    };
}
function inferTypeFromValue(v) {
    if (v === null) return 'null';
    if (typeof v === 'string') return 'string';
    if (typeof v === 'boolean') return 'boolean';
    if (typeof v === 'number') return Number.isInteger(v) ? 'integer' : 'number';
    return undefined;
}
function makeNullable(schema) {
    if (typeof schema.type === 'string') {
        return schema.type === 'null' ? schema : {
            ...schema,
            type: [
                schema.type,
                'null'
            ]
        };
    }
    if (Array.isArray(schema.type)) {
        return schema.type.includes('null') ? schema : {
            ...schema,
            type: [
                ...schema.type,
                'null'
            ]
        };
    }
    if (Array.isArray(schema.anyOf)) {
        const branches = schema.anyOf;
        const hasNull = branches.some((b)=>isSchema(b) && b.type === 'null');
        return hasNull ? schema : {
            ...schema,
            anyOf: [
                ...branches,
                {
                    type: 'null'
                }
            ]
        };
    }
    return {
        anyOf: [
            schema,
            {
                type: 'null'
            }
        ]
    };
}
function transformSchema(schema) {
    schema = stripUndefinedSentinel(schema);
    // OpenAI strict mode rejects any sibling keyword on `$ref` (description, examples, etc.).
    // Shape authors apply per-callsite descriptions on the outside of the def - preserve `$ref`
    // itself, drop everything else; the description lives inside the referenced `$def` via the
    // first emission.
    if ('$ref' in schema) {
        const { $ref, $defs } = schema;
        return $defs !== undefined ? {
            $ref,
            $defs
        } : {
            $ref
        };
    }
    for (const kw of BANNED_KEYWORDS){
        if (kw in schema) {
            throw new Error(`toOpenAiSchema: '${kw}' is not supported by OpenAI strict mode`);
        }
    }
    if ('const' in schema) {
        const { const: literalValue, ...rest } = schema;
        const inferred = inferTypeFromValue(literalValue);
        const out = {
            ...rest,
            enum: [
                literalValue
            ]
        };
        if (out.type == null && inferred != null) out.type = inferred;
        return transformSchema(out);
    }
    const out = {
        ...schema
    };
    if (Array.isArray(out.anyOf)) {
        out.anyOf = out.anyOf.map((branch)=>isSchema(branch) ? transformSchema(branch) : branch);
    }
    if (isSchema(out.$defs)) {
        const transformedDefs = {};
        for (const [k, v] of Object.entries(out.$defs)){
            transformedDefs[k] = isSchema(v) ? transformSchema(v) : v;
        }
        out.$defs = transformedDefs;
    }
    if (out.type === 'object' || isSchema(out.properties)) {
        if ('additionalProperties' in out && out.additionalProperties !== false) {
            throw new Error('toOpenAiSchema: open-ended `additionalProperties` (e.g. s.record(...)) cannot be expressed in OpenAI strict mode');
        }
        const properties = isSchema(out.properties) ? out.properties : {};
        const required = new Set(Array.isArray(out.required) ? out.required : []);
        const newProperties = {};
        for (const [key, propSchema] of Object.entries(properties)){
            const transformed = isSchema(propSchema) ? transformSchema(propSchema) : propSchema;
            newProperties[key] = required.has(key) ? transformed : isSchema(transformed) ? makeNullable(transformed) : transformed;
        }
        out.properties = newProperties;
        out.required = Object.keys(newProperties);
        out.additionalProperties = false;
    }
    // Array items keep their real schema: only optional PROPERTIES need the required+nullable
    // rewrite. Advertising nullable items invites the model to emit `[null]` for values the
    // AG-side shapes reject.
    if (isSchema(out.items)) {
        out.items = transformSchema(out.items);
    }
    return out;
}
function toOpenAiSchema(schema) {
    if (Array.isArray(schema.anyOf) && schema.type !== 'object' && !isSchema(schema.properties)) {
        throw new Error('toOpenAiSchema: root schema cannot be `anyOf` - wrap in an object (e.g. `s.object({ value: ... })`)');
    }
    return transformSchema(schema);
}
// =============================================================================
// Encoding: AG → OpenAI
// =============================================================================
function encodeConversationItems(items) {
    return items.map((item)=>{
        if (item.kind === 'input' && item.type === 'message') {
            return {
                type: 'message',
                role: item.role,
                status: item.status,
                content: item.content.map((c)=>{
                    switch(c.type){
                        case 'text':
                            return {
                                type: 'input_text',
                                text: c.text
                            };
                        case 'image':
                            return {
                                type: 'input_image',
                                detail: c.detail,
                                file_id: c.fileId ?? null,
                                image_url: c.imageUrl ?? null
                            };
                        case 'file':
                            return {
                                type: 'input_file',
                                file_id: c.fileId ?? null,
                                file_data: c.fileData,
                                file_url: c.fileUrl,
                                filename: c.filename
                            };
                    }
                })
            };
        }
        if (item.type === 'function_call_output') {
            return {
                type: 'function_call_output',
                call_id: item.callId,
                output: item.output,
                status: item.status
            };
        }
        if (item.kind === 'output' && item.type === 'message') {
            // No `id`: replayed history is reconstructed conversational context, not a resumed
            // OpenAI response. Echoing the original `msg_…` id makes the API treat it as response
            // state and demand the linked `reasoning` item (which a view-derived history lacks).
            return {
                type: 'message',
                role: 'assistant',
                status: item.status,
                content: item.content.map((c)=>{
                    if (c.type === 'text') {
                        return {
                            type: 'output_text',
                            text: c.text,
                            annotations: c.annotations.map((ann)=>{
                                switch(ann.type){
                                    case 'file_path':
                                        return {
                                            type: 'file_path',
                                            file_id: ann.fileId,
                                            index: ann.index
                                        };
                                    case 'file_citation':
                                        return {
                                            type: 'file_citation',
                                            file_id: ann.fileId,
                                            index: ann.index,
                                            filename: ann.filename
                                        };
                                    case 'url_citation':
                                        return {
                                            type: 'url_citation',
                                            url: ann.url,
                                            start_index: ann.startIndex,
                                            end_index: ann.endIndex,
                                            title: ann.title
                                        };
                                    case 'container_file_citation':
                                        return {
                                            type: 'container_file_citation',
                                            container_id: ann.containerId,
                                            file_id: ann.fileId,
                                            start_index: ann.startIndex,
                                            end_index: ann.endIndex,
                                            filename: ann.filename
                                        };
                                }
                            })
                        };
                    }
                    return {
                        type: 'refusal',
                        refusal: c.refusal
                    };
                })
            };
        }
        if (item.kind === 'output' && item.type === 'function_call') {
            // No `id` (same reason as the assistant message above): `call_id` alone pairs the call
            // with its `function_call_output`, and a reconstructed `id` isn't a valid `fc_…` anyway.
            return {
                type: 'function_call',
                call_id: item.callId,
                name: item.name,
                arguments: item.arguments,
                status: item.status
            };
        }
        if (item.kind === 'output' && item.type === 'reasoning') {
            return {
                id: item.id,
                type: 'reasoning',
                summary: item.summary.map((s)=>({
                        type: 'summary_text',
                        text: s.text
                    })),
                content: item.content?.map((c)=>({
                        type: 'reasoning_text',
                        text: c.text
                    }))
            };
        }
        throw new Error(`Unknown conversation item type: ${item.type}`);
    });
}
// =============================================================================
// Decoding: OpenAI → AG
// =============================================================================
// `toOpenAiSchema` rewrites optional properties as required + nullable to satisfy
// OpenAI strict mode, so the model returns `null` for unset optionals. AG-side
// validation treats those fields as optional (not nullable), so strip `null`s
// from tool-call argument payloads on the way back. Only object PROPERTIES are
// stripped: a null array item is either a genuinely nullable value that must
// survive (e.g. a rank filter's `[10, null]` bounds) or invalid input that
// AG-side validation should report rather than have silently deleted.
function stripNulls(value) {
    if (Array.isArray(value)) return value.map((v)=>stripNulls(v));
    if (value !== null && typeof value === 'object') {
        const out = {};
        for (const [k, v] of Object.entries(value)){
            if (v === null) continue;
            out[k] = stripNulls(v);
        }
        return out;
    }
    return value;
}
function stripNullsFromToolArgs(argsJson) {
    if (!argsJson) return argsJson;
    let parsed;
    try {
        parsed = JSON.parse(argsJson);
    } catch  {
        return argsJson;
    }
    return JSON.stringify(stripNulls(parsed));
}
function decodeAnnotations(annotations) {
    return (annotations ?? []).map((ann)=>{
        if (ann.type === 'file_path') {
            return {
                type: 'file_path',
                fileId: ann.file_id,
                index: ann.index
            };
        }
        if (ann.type === 'file_citation') {
            return {
                type: 'file_citation',
                fileId: ann.file_id,
                index: ann.index,
                filename: ann.filename
            };
        }
        if (ann.type === 'url_citation') {
            return {
                type: 'url_citation',
                url: ann.url,
                startIndex: ann.start_index,
                endIndex: ann.end_index,
                title: ann.title
            };
        }
        if (ann.type === 'container_file_citation') {
            return {
                type: 'container_file_citation',
                containerId: ann.container_id,
                fileId: ann.file_id,
                startIndex: ann.start_index,
                endIndex: ann.end_index,
                filename: ann.filename
            };
        }
        return ann;
    });
}
function decodeOutputContent(input) {
    if (input.type === 'output_text') {
        return {
            type: 'text',
            text: input.text,
            annotations: decodeAnnotations(input.annotations)
        };
    }
    return input;
}
function decodeOutputItem(input) {
    switch(input.type){
        case 'message':
            {
                const message = {
                    id: input.id ?? '',
                    kind: 'output',
                    type: 'message',
                    role: 'assistant',
                    status: input.status ?? 'completed',
                    content: input.content.map(decodeOutputContent)
                };
                return message;
            }
        case 'function_call':
            return {
                id: input.id ?? '',
                kind: 'output',
                type: 'function_call',
                callId: input.call_id,
                name: input.name,
                arguments: stripNullsFromToolArgs(input.arguments ?? ''),
                status: input.status
            };
        case 'reasoning':
            {
                const reasoning = {
                    id: input.id ?? '',
                    kind: 'output',
                    type: 'reasoning',
                    summary: input.summary.map((s)=>({
                            type: 'summary',
                            text: s.text
                        })),
                    content: input.content?.map((c)=>({
                            type: 'text',
                            text: c.text
                        }))
                };
                return reasoning;
            }
        default:
            throw new Error(`Unknown output item type: ${input.type}`);
    }
}
function decodeResponse(input) {
    return {
        id: input.id,
        createdAt: input.created_at,
        model: input.model,
        incompleteDetails: input.incomplete_details ? {
            reason: input.incomplete_details.reason
        } : undefined,
        output: input.output.map(decodeOutputItem),
        status: input.status,
        error: input.error ? {
            code: input.error.code,
            message: input.error.message
        } : undefined,
        usage: input.usage ? {
            inputTokens: input.usage.input_tokens,
            outputTokens: input.usage.output_tokens,
            totalTokens: input.usage.total_tokens,
            reasoningTokens: input.usage.output_tokens_details?.reasoning_tokens,
            cachedInputTokens: input.usage.input_tokens_details?.cached_tokens,
            cacheWriteTokens: input.usage.input_tokens_details?.cache_write_tokens
        } : undefined
    };
}
/**
 * Translates the OpenAI Responses stream into the events AG Studio reads.
 *
 * The provider is item-and-index shaped; AG Studio is message-shaped, keyed by id. The only state
 * needed to bridge them is the item id of each open item, since argument deltas arrive against the
 * item while tool events are keyed by the call.
 */ class ResponseStreamTranslator {
    callIdByItemId = new Map();
    kindByItemId = new Map();
    /** The events one SSE payload maps to. Anything not recognised is ignored, not an error. */ translate(input, outcome) {
        switch(input.type){
            case 'response.output_item.added':
                return this.open(input.item);
            case 'response.output_item.done':
                return this.close(input.item);
            case 'response.output_text.delta':
            case 'response.refusal.delta':
                return [
                    {
                        type: 'TEXT_MESSAGE_CONTENT',
                        messageId: input.item_id,
                        delta: input.delta
                    }
                ];
            case 'response.reasoning_text.delta':
            case 'response.reasoning_summary_text.delta':
                return [
                    {
                        type: 'REASONING_MESSAGE_CONTENT',
                        messageId: input.item_id,
                        delta: input.delta
                    }
                ];
            case 'response.function_call_arguments.delta':
                {
                    const toolCallId = this.callIdByItemId.get(input.item_id);
                    return toolCallId ? [
                        {
                            type: 'TOOL_CALL_ARGS',
                            toolCallId,
                            delta: input.delta
                        }
                    ] : [];
                }
            case 'response.completed':
                outcome.response = decodeResponse(input.response);
                return [];
            case 'response.failed':
            case 'response.incomplete':
                outcome.error ??= new Error(input.response?.error?.message ?? `Response ${input.type}.`);
                return [];
            case 'error':
                outcome.error ??= new Error(`${input.code ?? 'api_error'}: ${input.message}`);
                return [];
            default:
                return [];
        }
    }
    open(item) {
        switch(item?.type){
            case 'message':
                this.kindByItemId.set(item.id, 'message');
                return [
                    {
                        type: 'TEXT_MESSAGE_START',
                        messageId: item.id,
                        role: 'assistant'
                    }
                ];
            case 'reasoning':
                this.kindByItemId.set(item.id, 'reasoning');
                return [
                    {
                        type: 'REASONING_MESSAGE_START',
                        messageId: item.id,
                        role: 'reasoning'
                    }
                ];
            case 'function_call':
                this.kindByItemId.set(item.id, 'function_call');
                this.callIdByItemId.set(item.id, item.call_id);
                return [
                    {
                        type: 'TOOL_CALL_START',
                        toolCallId: item.call_id,
                        toolCallName: item.name
                    }
                ];
            default:
                return [];
        }
    }
    close(item) {
        switch(this.kindByItemId.get(item?.id)){
            case 'message':
                return [
                    {
                        type: 'TEXT_MESSAGE_END',
                        messageId: item.id
                    }
                ];
            case 'reasoning':
                return [
                    {
                        type: 'REASONING_MESSAGE_END',
                        messageId: item.id
                    }
                ];
            case 'function_call':
                {
                    const toolCallId = this.callIdByItemId.get(item.id);
                    return toolCallId ? [
                        {
                            type: 'TOOL_CALL_END',
                            toolCallId
                        }
                    ] : [];
                }
            default:
                return [];
        }
    }
}
// =============================================================================
// Stream Processor
// =============================================================================
async function* streamOpenAi(config, requestBody, outcome, signal) {
    const translator = new ResponseStreamTranslator();
    const emit = (payload)=>{
        if (payload === '[DONE]') {
            return [];
        }
        try {
            const parsed = JSON.parse(payload);
            return parsed.type === 'keepalive' ? [] : translator.translate(parsed, outcome);
        } catch (error) {
            outcome.error ??= error instanceof Error ? error : new Error(String(error));
            return [];
        }
    };
    const response = await fetch(`${config.endpoint}/responses`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...config.key && {
                Authorization: `Bearer ${config.key}`
            },
            ...config.organization && {
                'OpenAI-Organization': config.organization
            }
        },
        body: JSON.stringify(requestBody),
        signal
    });
    if (!response.ok) {
        const body = await response.json().catch(()=>({}));
        throw new Error(body.error?.message || `HTTP ${response.status}: ${response.statusText}`);
    }
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    while(true){
        const { done, value } = await reader.read();
        if (done) {
            break;
        }
        buffer += decoder.decode(value, {
            stream: true
        });
        const frames = buffer.split('\n\n');
        buffer = frames.pop() ?? '';
        for (const frame of frames){
            for (const line of frame.split('\n')){
                if (line.startsWith('data: ')) {
                    yield* emit(line.slice(6));
                }
            }
        }
    }
}
// =============================================================================
// Request Builder
// =============================================================================
function prepareToolChoice(toolChoice) {
    if (!toolChoice) return undefined;
    if (typeof toolChoice === 'string') return toolChoice;
    return {
        type: 'function',
        name: toolChoice.name
    };
}
function prepareResponseFormat(format) {
    if (format.type === 'text') return {
        type: 'text'
    };
    return {
        type: 'json_schema',
        name: format.name,
        description: format.description,
        schema: toOpenAiSchema(format.schema),
        strict: true
    };
}
function runRequest(config, request, signal) {
    const { tools = [], toolChoice, responseFormat, input, model, ...rest } = request;
    const requestBody = {
        ...rest,
        input: encodeConversationItems(input),
        // `request.model` carries whichever model the reader picked, and is absent when the chat
        // offers no choice - so the adapter's own model is the fallback, not an override.
        model: model?.id ?? config.model,
        stream: true,
        tools: tools.map((tool)=>({
                type: 'function',
                name: tool.name,
                description: tool.description,
                parameters: toOpenAiSchema(tool.parameters),
                strict: true
            })),
        tool_choice: prepareToolChoice(toolChoice),
        text: {
            format: prepareResponseFormat(responseFormat)
        },
        // Studio's effort ids are passed straight through as OpenAI's reasoning effort. A model
        // declared without efforts sends none, so the adapter's own default applies.
        reasoning: {
            effort: model?.effort ?? 'medium'
        },
        parallel_tool_calls: true
    };
    const outcome = {};
    const streamIterator = streamOpenAi(config, requestBody, outcome, signal);
    let resolveComplete;
    let rejectComplete;
    const completePromise = new Promise((resolve, reject)=>{
        resolveComplete = resolve;
        rejectComplete = reject;
    });
    // `complete` rejects on a failed turn: the host ends a run on a throw from here and reads
    // nothing off the response's own status.
    // A failed turn is reported once, through `complete`. Rethrowing as well would leave the
    // rejection unobserved whenever a consumer stops reading the stream before awaiting it - which
    // is exactly what happens on an HTTP error or a cancellation - and that surfaces as an unhandled
    // rejection rather than as the run's own error.
    async function* wrappedIterator() {
        try {
            yield* streamIterator;
        } catch (error) {
            outcome.error ??= error instanceof Error ? error : new Error(String(error));
        }
        if (outcome.error) {
            rejectComplete(outcome.error);
        } else if (outcome.response) {
            resolveComplete(outcome.response);
        } else {
            rejectComplete(new Error('Stream completed without a final response.'));
        }
    }
    // Marks the rejection observed for a consumer that abandons the stream and never awaits
    // `complete`; anyone who does await it still sees the failure.
    void completePromise.catch(()=>{});
    const wrapped = wrappedIterator();
    return {
        stream: {
            [Symbol.asyncIterator]: ()=>wrapped
        },
        complete: completePromise
    };
}
function openaiAdapter(options) {
    const config = {
        endpoint: options.endpoint ?? 'https://api.openai.com/v1',
        key: options.key,
        model: options.model ?? 'gpt-5.4-mini',
        organization: options.organization
    };
    return {
        executeTurn: (request, options)=>runRequest(config, request, options?.signal)
    };
}
}),
"[project]/app/dashboard/studio/theme.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "agStudioPayPalTheme",
    ()=>agStudioPayPalTheme
]);
// AG Studio theme for the PayPal dashboard. Every value points at a design token from
// app/globals.css, the same variables the shell's Tailwind classes use, so Studio renders as
// part of the page rather than a component embedded in it: change a token there and the shell,
// widgets, grids and charts all follow.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/ag-studio/dist/package/main.esm.mjs [app-ssr] (ecmascript)");
;
const token = (name)=>`var(--pp-${name})`;
const line = (color)=>({
        width: 1,
        color: token(color)
    });
const palette = Object.fromEntries(Array.from({
    length: 10
}, (_, i)=>[
        [
            `chartPaletteFills${i + 1}Color`,
            token(`chart-${i + 1}`)
        ],
        [
            `chartPaletteStrokes${i + 1}Color`,
            token(`chart-${i + 1}`)
        ]
    ]).flat());
const agStudioPayPalTheme = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$ag$2d$studio$2f$dist$2f$package$2f$main$2e$esm$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["studioTheme"].withParams({
    // Shared by Studio's UI, grids and charts.
    fontFamily: token('font'),
    fontSize: 14,
    textColor: token('ink'),
    foregroundColor: token('ink'),
    subtleTextColor: token('muted'),
    backgroundColor: token('surface'),
    borderColor: token('border'),
    accentColor: token('blue'),
    iconColor: token('navy'),
    rowHoverColor: token('highlight'),
    // No frame: the canvas is the page's own background. Each widget is inset 12px inside its
    // grid cell, so 20px of padding puts widget edges on the header's 32px gutter.
    studioWrapperBorder: false,
    studioWrapperBorderRadius: 0,
    studioWrapperSpacing: 0,
    studioWrapperBackgroundColor: token('canvas'),
    studioCanvasBorder: false,
    studioCanvasBorderRadius: 0,
    studioCanvasShadow: false,
    studioCanvasBackgroundColor: token('canvas'),
    studioCanvasPadding: 20,
    // Slightly taller rows than the default 16px make room for card padding.
    studioCanvasRowHeight: 18,
    studioCanvasFontFamily: token('font'),
    // Widgets are the shell's cards: white, 1px border, 8px radius.
    studioWidgetBackgroundColor: token('surface'),
    studioWidgetBorder: line('border'),
    studioWidgetBorderRadius: 8,
    studioWidgetPadding: 10,
    studioWidgetTitleFontFamily: token('font'),
    studioWidgetTitleFontSize: 16,
    studioWidgetTitleFontWeight: 600,
    studioWidgetTitleTextColor: token('navy'),
    studioWidgetSubtitleFontFamily: token('font'),
    studioWidgetSubtitleFontSize: 13,
    studioWidgetSubtitleTextColor: token('muted'),
    studioWidgetCaptionFontFamily: token('font'),
    studioWidgetCaptionFontSize: 13,
    studioWidgetCaptionTextColor: token('muted'),
    studioWidgetResizeBorderColor: token('blue'),
    // Edit-mode panels read as more of the sidebar.
    studioPanelContainerBackgroundColor: token('surface'),
    studioPanelContainerBorder: line('border'),
    studioPanelContainerBorderRadius: 0,
    studioPanelDividerColor: token('border'),
    studioPanelDividerActiveColor: token('blue'),
    studioPanelSectionBorderColor: token('border'),
    studioPanelHeaderFontFamily: token('font'),
    studioPanelHeaderFontWeight: 600,
    studioPanelChevronButtonHoverBackgroundColor: token('highlight'),
    studioPanelChevronButtonHoverColor: token('blue'),
    // Selected toggles match the sidebar's selected item: highlight fill, blue text and edge.
    studioToggleButtonActiveBackgroundColor: token('highlight'),
    studioToggleButtonActiveBorderColor: token('blue'),
    studioToggleButtonActiveColor: token('blue'),
    // Grid widgets: muted semibold headers, light dividers, roomy rows.
    gridFontFamily: token('font'),
    gridFontSize: 14,
    gridCellTextColor: token('ink'),
    gridHeaderBackgroundColor: token('surface'),
    gridHeaderTextColor: token('muted'),
    gridHeaderFontWeight: 600,
    gridHeaderFontSize: 13,
    gridRowHeight: 40,
    gridRowBorder: line('gridline'),
    gridHeaderRowBorder: line('border'),
    gridPinnedRowBorder: line('border'),
    gridRowHoverColor: token('highlight'),
    gridWrapperBorder: false,
    // Charts.
    chartFontFamily: token('font'),
    chartTextColor: token('ink'),
    chartSubtleTextColor: token('muted'),
    chartAxisLineColor: token('border'),
    chartGridLineColor: token('gridline'),
    ...palette
});
}),
"[project]/app/dashboard/use-reports.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useReports",
    ()=>useReports
]);
// Saved reports as React state, written through to localStorage on every change.
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/app/dashboard/reports-store.ts [app-ssr] (ecmascript)");
;
;
function useReports() {
    const [store, setStore] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(__TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loadReports"]);
    // The latest reports, for handlers that run one after another before React re-renders.
    const storeRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(store);
    const update = (change)=>{
        const next = change(storeRef.current);
        storeRef.current = next;
        (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["saveReports"])(next);
        setStore(next);
    };
    const editReport = (id, change)=>update((current)=>{
            const report = (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["findReport"])(current.reports, id);
            return report ? (0, __TURBOPACK__imported__module__$5b$project$5d2f$app$2f$dashboard$2f$reports$2d$store$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["upsert"])(current, change(report)) : current;
        });
    return {
        store,
        latest: ()=>storeRef.current,
        update,
        editReport
    };
}
}),
];

//# sourceMappingURL=app_dashboard_1f0nav7._.js.map