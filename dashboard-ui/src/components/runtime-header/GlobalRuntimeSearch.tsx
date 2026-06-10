"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2, Search } from "lucide-react";
import { useRouter } from "next/navigation";
import { useCompanySearch } from "@/hooks/use-company-search";
import { useRuntimeTicker } from "@/hooks/use-runtime-ticker";
import { useRuntimeQuery } from "@/runtime-state/runtime-query-context";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import type { CompanySearchItem } from "@/services/api";

export function GlobalRuntimeSearch() {
  const router = useRouter();
  const { ticker, companyName } = useRuntimeTicker();
  const {
    traceId: runtimeTraceId,
    engineRunning,
    runQuerySelected,
  } = useRuntimeQuery();
  const [query, setQuery] = useState("");
  const [keywords, setKeywords] = useState("");
  const [selected, setSelected] = useState<CompanySearchItem | null>(null);
  const hydratedRuntimeTickerRef = useRef<string | null>(null);
  const [previousTraceId, setPreviousTraceId] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const { results, loading, error } = useCompanySearch(
    query,
    open && !selected,
  );

  useEffect(() => {
    if (!ticker || !companyName) return;
    if (hydratedRuntimeTickerRef.current === ticker) return;
    hydratedRuntimeTickerRef.current = ticker;
    const item = { ticker, company_name: companyName };
    setSelected(item);
    setQuery(companyName);
  }, [ticker, companyName]);

  useEffect(() => {
    if (!previousTraceId || engineRunning || !runtimeTraceId) return;
    if (runtimeTraceId === previousTraceId) return;
    router.replace(traceQueryHref("/", runtimeTraceId));
    setPreviousTraceId(null);
  }, [previousTraceId, engineRunning, runtimeTraceId, router]);

  const selectCompany = (item: CompanySearchItem) => {
    setSelected(item);
    setQuery(item.company_name);
    setOpen(false);
  };

  const runAnalysis = () => {
    if (!selected || engineRunning) return;
    setPreviousTraceId(runtimeTraceId || "pending");
    void runQuerySelected({
      ticker: selected.ticker,
      company: selected.company_name,
      keywords: keywords
        .split(/[\s,]+/)
        .map((value) => value.trim())
        .filter(Boolean),
    });
  };

  return (
    <div className="flex flex-1 flex-wrap items-end gap-2">
      <div className="relative min-w-[220px] flex-1">
        <label className="text-[11px] text-muted-foreground" htmlFor="runtime-company-search">
          종목 검색
        </label>
        <input
          id="runtime-company-search"
          value={query}
          onChange={(event) => {
            const value = event.target.value;
            setQuery(value);
            setOpen(Boolean(value.trim()));
            if (selected && value !== selected.company_name) setSelected(null);
          }}
          onFocus={() => setOpen(Boolean(query.trim()) && !selected)}
          onKeyDown={(event) => {
            if (event.key !== "Enter") return;
            if (selected) {
              runAnalysis();
              return;
            }
            if (results.length === 1) selectCompany(results[0]);
          }}
          placeholder="종목명 또는 ticker"
          disabled={engineRunning}
          autoComplete="off"
          className="h-8 w-full rounded-md border border-border bg-card px-2 text-xs outline-none placeholder:text-muted-foreground"
        />
        {open && !selected && (
          <ul
            role="listbox"
            className="absolute left-0 right-0 top-full z-[200] mt-1 max-h-56 overflow-auto rounded-md border border-border bg-card py-1 shadow-xl"
          >
            {loading && (
              <li className="px-3 py-2 text-xs text-muted-foreground">검색 중…</li>
            )}
            {!loading && error && (
              <li className="px-3 py-2 text-xs text-destructive">{error}</li>
            )}
            {!loading && !error && results.length === 0 && (
              <li className="px-3 py-2 text-xs text-muted-foreground">
                검색 결과 없음
              </li>
            )}
            {results.map((item) => (
              <li key={item.ticker}>
                <button
                  type="button"
                  onMouseDown={(event) => event.preventDefault()}
                  onClick={() => selectCompany(item)}
                  className="w-full px-3 py-2 text-left text-xs hover:bg-muted"
                >
                  <span className="font-medium">{item.company_name}</span>
                  <span className="ml-2 font-mono text-muted-foreground">
                    {item.ticker}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      <label className="min-w-[150px] flex-1 text-[11px] text-muted-foreground">
        분석 키워드
        <input
          value={keywords}
          onChange={(event) => setKeywords(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") runAnalysis();
          }}
          placeholder="예: 실적, 수주"
          disabled={engineRunning}
          className="mt-0.5 h-8 w-full rounded-md border border-border bg-card px-2 text-xs text-foreground outline-none placeholder:text-muted-foreground"
        />
      </label>

      <button
        type="button"
        onClick={runAnalysis}
        disabled={!selected || engineRunning}
        className="inline-flex h-8 items-center gap-1 rounded-md border border-primary/50 bg-primary/10 px-3 text-xs text-primary disabled:cursor-not-allowed disabled:opacity-40"
      >
        {engineRunning ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
        ) : (
          <Search className="h-3.5 w-3.5" />
        )}
        {engineRunning ? "분석 중…" : "분석 실행"}
      </button>
    </div>
  );
}
