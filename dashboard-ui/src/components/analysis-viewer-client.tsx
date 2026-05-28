"use client";

import Link from "next/link";
import { useEffect } from "react";
import { useActiveTrace } from "@/hooks/use-active-trace";
import { RuntimeTraceBanner } from "@/components/runtime-panels/RuntimeTraceBanner";
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
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import { API_BASE } from "@/services/api";
import { Loader2, Play } from "lucide-react";

export function AnalysisViewerClient() {
  const { traceId: activeTraceId } = useActiveTrace();
  const urlTraceId = activeTraceId;

  const { data, status, error, traceId, loadByTraceId } = useAnalysisViewer();

  useEffect(() => {
    if (urlTraceId) loadByTraceId(urlTraceId);
  }, [urlTraceId, loadByTraceId]);

  const query =
    data.evaluation?.query ||
    data.retrieval?.query ||
    data.reflection?.query;

  return (
    <div className="mx-auto max-w-7xl space-y-4 p-4 md:p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <DashboardNav traceId={traceId ?? urlTraceId} apiBase={API_BASE} />
        <Button variant="outline" size="sm" asChild>
          <Link href={traceQueryHref("/", traceId ?? urlTraceId)}>← Overview Dashboard</Link>
        </Button>
      </div>

      <RuntimeTraceBanner />

      <div className="rounded-lg border border-border bg-card p-4">
        <h2 className="text-sm font-semibold">Retrieval &amp; Analysis Viewer</h2>
        <p className="mt-1 text-xs text-muted-foreground">
          traceId 기준 explainability (latest/sample fallback 없음)
        </p>
        <div className="mt-3 flex flex-wrap items-end gap-2">
          <div className="min-w-[200px] flex-1">
            <label className="text-xs text-muted-foreground">trace_id</label>
            <Input
              placeholder={traceId ?? "trace_id 입력"}
              id="trace-input"
              defaultValue={urlTraceId ?? ""}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  const v = (e.target as HTMLInputElement).value.trim();
                  if (v) loadByTraceId(v);
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
      </div>

      {!urlTraceId && !traceId && status === "idle" && (
        <Alert className="border-border bg-muted/30">
          <p className="text-sm">trace_id가 필요합니다. Dashboard에서 분석을 실행하세요.</p>
        </Alert>
      )}

      {error && (
        <Alert variant="destructive">
          <p className="text-sm">{error}</p>
        </Alert>
      )}

      {query && (
        <p className="text-sm text-muted-foreground">
          Query: <span className="text-foreground">{query}</span>
        </p>
      )}

      <div className="grid gap-4 lg:grid-cols-2">
        <RetrievalDetailViewer data={data.retrieval} status={status} />
        <ReflectionDetailViewer data={data.reflection} status={status} />
      </div>
      <AnalysisReasoningViewer data={data.retrieval} status={status} />
      <ContextAssemblyViewer data={data.retrieval} status={status} />
      <EngineStepTimeline trace={data.trace} status={status} />
      <SourceTraceViewer data={data.retrieval} status={status} />
      <AnalysisMetadataPanel
        trace={data.trace}
        evaluation={data.evaluation}
        status={status}
      />
    </div>
  );
}
