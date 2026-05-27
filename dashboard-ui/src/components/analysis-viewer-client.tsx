"use client";

import Link from "next/link";
import { useEffect } from "react";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { DashboardNav } from "@/components/layout/dashboard-nav";
import { ContextAssemblyViewer } from "@/components/context-viewer/context-assembly-viewer";
import { AnalysisMetadataPanel } from "@/components/metadata-panel/analysis-metadata-panel";
import { AnalysisReasoningViewer } from "@/components/reasoning-viewer/analysis-reasoning-viewer";
import { ReflectionDetailViewer } from "@/components/reflection-detail/reflection-detail-viewer";
import { RetrievalDetailViewer } from "@/components/retrieval-detail/retrieval-detail-viewer";
import { SourceTraceViewer } from "@/components/source-trace/source-trace-viewer";
import { EngineStepTimeline } from "@/components/timeline/engine-step-timeline";
import { useAnalysisViewer } from "@/hooks/use-analysis-viewer";
import { API_BASE } from "@/services/api";
import { Loader2, Play } from "lucide-react";

const SAMPLE_QUERIES = [
  "삼성전자 반도체 전망 분석",
  "HBM 공급 부족 영향",
  "AI 서버 투자 확대",
];

export function AnalysisViewerClient() {
  const {
    data,
    status,
    error,
    traceId,
    loadLatest,
    loadByTraceId,
  } = useAnalysisViewer();

  useEffect(() => {
    loadLatest();
  }, [loadLatest]);

  const query =
    data.evaluation?.query ||
    data.retrieval?.query ||
    data.reflection?.query;

  return (
    <div className="mx-auto max-w-7xl space-y-4 p-4 md:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <DashboardNav traceId={traceId} apiBase={API_BASE} />
        <Button variant="outline" size="sm" asChild>
          <Link href="/">← Overview Dashboard</Link>
        </Button>
      </div>

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-sm font-semibold">Retrieval &amp; Analysis Viewer</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          Explainability: retrieval 근거 → context → reasoning → reflection → trace
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          {SAMPLE_QUERIES.map((q) => (
            <span
              key={q}
              className="rounded border border-border/60 px-2 py-0.5 text-[10px] text-muted-foreground"
            >
              {q}
            </span>
          ))}
        </div>
        <div className="mt-3 flex flex-wrap items-end gap-2">
          <div className="min-w-[200px] flex-1">
            <label className="text-xs text-muted-foreground">trace_id</label>
            <Input
              placeholder={traceId ?? "20260527_123745"}
              id="trace-input"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  const v = (e.target as HTMLInputElement).value.trim();
                  if (v) loadByTraceId(v);
                  else loadLatest();
                }
              }}
            />
          </div>
          <Button
            type="button"
            disabled={status === "loading"}
            onClick={() => {
              const el = document.getElementById("trace-input") as HTMLInputElement | null;
              const v = el?.value.trim();
              if (v) loadByTraceId(v);
              else loadLatest();
            }}
          >
            {status === "loading" ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            Load Analysis
          </Button>
        </div>
        {query && (
          <p className="mt-2 text-xs text-muted-foreground">
            Query: <span className="text-foreground">{query}</span>
          </p>
        )}
      </div>

      {error && (
        <Alert variant="destructive">
          <p className="font-medium">API 연동 실패</p>
          <p className="mt-1 text-xs">{error}</p>
        </Alert>
      )}

      <AnalysisMetadataPanel
        trace={data.trace}
        evaluation={data.evaluation}
        status={status}
      />

      <div className="grid gap-4 lg:grid-cols-2">
        <RetrievalDetailViewer data={data.retrieval} status={status} />
        <ContextAssemblyViewer data={data.retrieval} status={status} />
        <AnalysisReasoningViewer data={data.retrieval} status={status} />
        <ReflectionDetailViewer data={data.reflection} status={status} />
      </div>

      <SourceTraceViewer
        data={data.retrieval}
        status={status}
        ticker={data.retrieval?.ticker}
      />
      <EngineStepTimeline trace={data.trace} status={status} />
    </div>
  );
}
