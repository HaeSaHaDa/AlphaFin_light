"use client";

import { useActiveTrace } from "@/hooks/use-active-trace";
import { RuntimeTraceBanner } from "@/components/runtime-panels/RuntimeTraceBanner";
import { Loader2, AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { PresentationModeToggle } from "@/components/layout/presentation-mode-toggle";
import { MemoryTimeline } from "@/components/memory-timeline/MemoryTimeline";
import { useMemoryTimeline } from "@/hooks/use-memory-timeline";

export function MemoryTimelineViewerClient() {
  const { traceId } = useActiveTrace();

  const { nodes, query, status, error, reload } = useMemoryTimeline(traceId);

  return (
    <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-6">
      <RuntimeTraceBanner />

      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border pb-4">
        <div>
          <h1 className="text-xl font-bold">시장 기억 타임라인</h1>
          <p className="text-xs text-muted-foreground">
            AI가 기억하는 시장 이슈의 생성 · 승격 · 소멸 흐름
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <PresentationModeToggle />
          {traceId && (
            <span className="rounded border border-border px-2 py-1 font-mono text-xs text-muted-foreground">
              trace: {traceId}
            </span>
          )}
          <Button variant="outline" size="sm" onClick={reload} disabled={status === "loading"}>
            <RefreshCw className="h-3 w-3" />
            새로고침
          </Button>
        </div>
      </div>

      {!traceId && status === "idle" && (
        <div className="rounded-lg border border-dashed border-border p-6 text-center text-sm text-muted-foreground">
          trace_id가 없습니다. Dashboard에서 분석을 실행한 뒤 이 페이지로 이동하세요.
        </div>
      )}

      {/* 로딩 */}
      {status === "loading" && (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-6 w-6 animate-spin text-primary" />
          <span className="ml-2 text-sm text-muted-foreground">시장 기억 로드 중…</span>
        </div>
      )}

      {/* 에러 */}
      {status === "error" && (
        <div className="flex items-center gap-2 rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          <AlertTriangle className="h-4 w-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* 타임라인 */}
      {status === "success" && (
        <MemoryTimeline nodes={nodes} query={query} />
      )}
    </div>
  );
}
