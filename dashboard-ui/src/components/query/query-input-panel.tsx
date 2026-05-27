"use client";

import { useState } from "react";
import { Loader2, Play, RefreshCw, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { LoadStatus } from "@/types/dashboard";

interface QueryInputPanelProps {
  status: LoadStatus;
  engineRunning: boolean;
  traceId: string | null;
  displayQuery?: string;
  onRunEngine: (query: string, ticker: string) => void;
  onLoadLatest: () => void;
  onLoadByTraceId: (traceId: string) => void;
}

const TICKER_MAP: Record<string, string> = {
  "삼성전자": "005930",
  "SK하이닉스": "000660",
  "현대자동차": "005380",
  "LG에너지솔루션": "373220",
  "카카오": "035720",
  "네이버": "035420",
  "셀트리온": "068270",
  "POSCO홀딩스": "005490",
};

function guessTicker(query: string): string {
  for (const [name, ticker] of Object.entries(TICKER_MAP)) {
    if (query.includes(name)) return ticker;
  }
  return "005930";
}

export function QueryInputPanel({
  status,
  engineRunning,
  traceId,
  displayQuery,
  onRunEngine,
  onLoadLatest,
  onLoadByTraceId,
}: QueryInputPanelProps) {
  const [query, setQuery] = useState("삼성전자 반도체 전망 분석");
  const [traceInput, setTraceInput] = useState("");

  const busy = status === "loading" || engineRunning;

  const handleRun = () => {
    const q = query.trim();
    if (!q) return;
    const ticker = guessTicker(q);
    onRunEngine(q, ticker);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleRun();
  };

  return (
    <Card className="border-primary/30 bg-card/80">
      <CardHeader>
        <CardTitle>Query Input</CardTitle>
        <p className="text-xs text-muted-foreground">
          질문을 입력하고 <strong>Run Engine</strong>을 누르면 Unified Engine이 실행되고 결과가 갱신됩니다.
        </p>
      </CardHeader>
      <CardContent className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-end">
        {/* 쿼리 입력 */}
        <div className="min-w-[260px] flex-1 space-y-1">
          <label className="text-xs text-muted-foreground">분석 질문</label>
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="예: 현대자동차 전기차 전망"
            disabled={busy}
          />
        </div>

        {/* 버튼 그룹 */}
        <div className="flex flex-wrap gap-2">
          {/* Run Engine — 엔진 실행 후 trace_id 기반 로드 */}
          <Button
            type="button"
            disabled={busy || !query.trim()}
            onClick={handleRun}
          >
            {engineRunning ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Zap className="h-4 w-4" />
            )}
            {engineRunning ? "Engine 실행 중…" : "Run Engine"}
          </Button>

          {/* Latest Trace — 가장 최근 저장된 결과 조회 */}
          <Button
            type="button"
            variant="secondary"
            disabled={busy}
            onClick={onLoadLatest}
          >
            <RefreshCw className="h-4 w-4" />
            Latest Trace
          </Button>
        </div>

        {/* trace_id 직접 입력 */}
        <div className="flex w-full flex-wrap items-end gap-2 sm:w-auto">
          <div className="min-w-[160px] space-y-1">
            <label className="text-xs text-muted-foreground">trace_id 직접 조회</label>
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

        {/* 현재 표시 중인 결과 정보 */}
        {displayQuery && (
          <p className="w-full text-xs text-muted-foreground">
            표시 중:{" "}
            <span className="text-foreground font-medium">{displayQuery}</span>
            {traceId && (
              <span className="ml-2 font-mono opacity-60">({traceId})</span>
            )}
            {query.trim() !== displayQuery && (
              <span className="ml-2 text-amber-400/90">
                ← 입력 질문과 다름. Run Engine을 눌러 갱신하세요.
              </span>
            )}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
