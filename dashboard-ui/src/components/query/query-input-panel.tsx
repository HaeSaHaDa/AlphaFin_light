"use client";

import { useState } from "react";
import { Loader2, Play, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CompanyContextPanel } from "@/components/query/company-context-panel";
import { useSearchTrigger } from "@/hooks/use-search-trigger";
import type { CompanyResolveData, IngestionRunSummary } from "@/types/company";
import type { LoadStatus } from "@/types/dashboard";

interface QueryInputPanelProps {
  status: LoadStatus;
  engineRunning: boolean;
  traceId: string | null;
  displayQuery?: string;
  companyContext?: CompanyResolveData | null;
  ingestionSummary?: IngestionRunSummary | null;
  onSearch: (query: string) => void;
  onLoadByTraceId: (traceId: string) => void;
  onIngestUpdate?: (payload: {
    company: CompanyResolveData;
    ingestion: IngestionRunSummary | null;
  }) => void;
}

export function QueryInputPanel({
  status,
  engineRunning,
  traceId,
  displayQuery,
  companyContext,
  ingestionSummary,
  onSearch,
  onLoadByTraceId,
  onIngestUpdate,
}: QueryInputPanelProps) {
  const [query, setQuery] = useState("현대자동차 전기차 전망");
  const [traceInput, setTraceInput] = useState("");

  const {
    preview,
    resolving,
    ingesting,
    error: searchError,
    resetIngestKey,
  } = useSearchTrigger(query, !engineRunning, onIngestUpdate);

  const company = companyContext ?? preview;
  const busy = status === "loading" || engineRunning || ingesting;

  const handleSearch = () => {
    const q = query.trim();
    if (!q) return;
    resetIngestKey();
    onSearch(q);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSearch();
  };

  return (
    <Card className="border-primary/30 bg-card/80">
      <CardHeader>
        <CardTitle>종목 검색 · AI 분석</CardTitle>
        <p className="text-xs text-muted-foreground">
          회사명이 포함된 검색어를 입력하면{" "}
          <strong>종목 식별 → 뉴스·공시 수집 → embedding</strong>이 자동 실행됩니다.
          Enter 또는 검색 버튼으로 AI 분석까지 진행합니다.
        </p>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <div className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-end">
          <div className="min-w-[260px] flex-1 space-y-1">
            <label className="text-xs text-muted-foreground">검색·분석 질문</label>
            <Input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="예: 현대자동차 전기차 전망"
              disabled={busy}
            />
          </div>

          <div className="flex flex-wrap gap-2">
            <Button
              type="button"
              disabled={busy || !query.trim()}
              onClick={handleSearch}
            >
              {engineRunning ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Search className="h-4 w-4" />
              )}
              {engineRunning
                ? "분석 중…"
                : ingesting
                  ? "수집·embedding 중…"
                  : "검색 · 분석"}
            </Button>
          </div>

          <div className="flex w-full flex-wrap items-end gap-2 sm:w-auto">
            <div className="min-w-[160px] space-y-1">
              <label className="text-xs text-muted-foreground">trace_id</label>
              <Input
                value={traceInput}
                onChange={(e) => setTraceInput(e.target.value)}
                placeholder={traceId ?? "20260527_123745"}
                disabled={busy}
              />
            </div>
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={busy || !traceInput.trim()}
              onClick={() => {
                if (traceInput.trim()) onLoadByTraceId(traceInput.trim());
              }}
            >
              <Play className="h-4 w-4" />
              Load
            </Button>
          </div>
        </div>

        {(resolving || ingesting) && !engineRunning && (
          <p className="text-xs text-primary">
            {resolving && !ingesting && "종목 식별 중…"}
            {ingesting && "뉴스·공시 수집 및 embedding 생성 중… (기존 데이터는 재사용)"}
          </p>
        )}

        <CompanyContextPanel
          company={company}
          ingestion={ingestionSummary}
          loading={resolving && !company}
          error={searchError}
        />

        {displayQuery && (
          <p className="text-xs text-muted-foreground">
            표시 중:{" "}
            <span className="font-medium text-foreground">{displayQuery}</span>
            {traceId && (
              <span className="ml-2 font-mono opacity-60">({traceId})</span>
            )}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
