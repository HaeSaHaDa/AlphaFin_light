"use client";

import { useState } from "react";
import { Loader2, Play, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { LoadStatus } from "@/types/dashboard";

interface QueryInputPanelProps {
  status: LoadStatus;
  traceId: string | null;
  displayQuery?: string;
  onLoadLatest: () => void;
  onLoadByTraceId: (traceId: string) => void;
}

export function QueryInputPanel({
  status,
  traceId,
  displayQuery,
  onLoadLatest,
  onLoadByTraceId,
}: QueryInputPanelProps) {
  const [query, setQuery] = useState(
    "삼성전자 반도체 전망 분석",
  );
  const [traceInput, setTraceInput] = useState("");

  const loading = status === "loading";

  return (
    <Card className="border-primary/30 bg-card/80">
      <CardHeader>
        <CardTitle>Query Input</CardTitle>
        <p className="text-xs text-muted-foreground">
          질문 입력 후 Dashboard 로드 · 엔진 실행은 Unified Engine에서 수행
        </p>
      </CardHeader>
      <CardContent className="flex flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-end">
        <div className="min-w-[200px] flex-1 space-y-1">
          <label className="text-xs text-muted-foreground">분석 질문</label>
          <Input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="예: 삼성전자 반도체 전망 분석"
          />
        </div>
        <div className="min-w-[180px] space-y-1">
          <label className="text-xs text-muted-foreground">trace_id (선택)</label>
          <Input
            value={traceInput}
            onChange={(e) => setTraceInput(e.target.value)}
            placeholder={traceId ?? "20260527_123745"}
          />
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            type="button"
            disabled={loading}
            onClick={() => {
              if (traceInput.trim()) {
                onLoadByTraceId(traceInput.trim());
              } else {
                onLoadLatest();
              }
            }}
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            Load Dashboard
          </Button>
          <Button
            type="button"
            variant="secondary"
            disabled={loading}
            onClick={onLoadLatest}
          >
            <RefreshCw className="h-4 w-4" />
            Latest Trace
          </Button>
        </div>
        {displayQuery && (
          <p className="w-full text-xs text-muted-foreground">
            표시 중: <span className="text-foreground">{displayQuery}</span>
            {query !== displayQuery && (
              <span className="ml-2 text-amber-400/90">
                (입력 질문과 API 최신 결과가 다를 수 있음)
              </span>
            )}
          </p>
        )}
      </CardContent>
    </Card>
  );
}
