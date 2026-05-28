"use client";

import Link from "next/link";
import { CollapsibleSection } from "@/components/ui/collapsible-section";
import { RetrievalViewer } from "@/components/retrieval/retrieval-viewer";
import { ReflectionViewer } from "@/components/reflection/reflection-viewer";
import { MemoryTimelineViewer } from "@/components/memory/memory-timeline-viewer";
import { EvaluationScorePanel } from "@/components/evaluation/evaluation-score-panel";
import { Button } from "@/components/ui/button";
import type { DashboardData, LoadStatus } from "@/types/dashboard";
import type { SignalEvaluationData } from "@/types/signal-evaluation";
import { DashboardSection } from "./DashboardSection";
import { AnalysisFlowPanel } from "./AnalysisFlowPanel";

interface ExplainabilityAccordionProps {
  data: DashboardData;
  signal: SignalEvaluationData | null;
  status: LoadStatus;
  traceId?: string | null;
}

function SignalAccordionBody({ signal }: { signal: SignalEvaluationData | null }) {
  if (!signal) {
    return <p className="text-sm text-muted-foreground">Signal 데이터 없음</p>;
  }
  const m = signal.metrics;
  return (
    <div className="space-y-3 text-sm">
      <p>{signal.summary_text}</p>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="rounded border border-border p-2">
          <p className="text-muted-foreground">방향 예측 정확도</p>
          <p className="font-bold">
            {Math.round(m.direction_accuracy * 100)}%
          </p>
        </div>
        <div className="rounded border border-border p-2">
          <p className="text-muted-foreground">예측 적중률</p>
          <p className="font-bold">{m.hit_ratio_pct}%</p>
        </div>
      </div>
      <p className="text-xs text-muted-foreground">
        실제 시장 변화:{" "}
        {signal.market_comparison.price_change_pct >= 0 ? "+" : ""}
        {signal.market_comparison.price_change_pct}% ·{" "}
        {signal.market_comparison.direction_correct ? "방향 일치" : "방향 불일치"}
      </p>
    </div>
  );
}

export function ExplainabilityAccordion({
  data,
  signal,
  status,
  traceId,
}: ExplainabilityAccordionProps) {
  const memoryHref = traceId
    ? `/memory-timeline?trace_id=${encodeURIComponent(traceId)}`
    : "/memory-timeline";
  const signalHref = traceId
    ? `/signal-evaluation?trace_id=${encodeURIComponent(traceId)}`
    : "/signal-evaluation";

  return (
    <DashboardSection
      title="AI 분석 과정"
      description="엔진 내부 단계를 펼쳐 확인할 수 있습니다. 발표 시 기본은 접힌 상태입니다."
    >
      <div className="space-y-2">
        <CollapsibleSection title="분석 과정 요약" defaultOpen={false}>
          <AnalysisFlowPanel trace={data.trace} />
        </CollapsibleSection>

        <div id="section-retrieval" className="scroll-mt-24">
          <CollapsibleSection title="AI가 참고한 자료" defaultOpen={false}>
            <RetrievalViewer data={data.retrieval} status={status} />
          </CollapsibleSection>
        </div>

        <div id="section-reflection" className="scroll-mt-24">
          <CollapsibleSection title="AI 자기 검토" defaultOpen={false}>
            <ReflectionViewer data={data.reflection} status={status} />
          </CollapsibleSection>
        </div>

        <div id="section-memory" className="scroll-mt-24">
          <CollapsibleSection title="시장 기억 변화" defaultOpen={false}>
            <MemoryTimelineViewer data={data.memory} status={status} />
          <Button variant="ghost" size="sm" className="mt-2 h-auto px-0 text-primary" asChild>
            <Link href={memoryHref}>시장 기억 타임라인 전체 보기</Link>
          </Button>
          </CollapsibleSection>
        </div>

        <div id="section-evaluation" className="scroll-mt-24">
          <CollapsibleSection title="분석 신뢰도" defaultOpen={false}>
            <EvaluationScorePanel data={data.evaluation} status={status} />
          </CollapsibleSection>
        </div>

        <CollapsibleSection title="Signal 평가" defaultOpen={false}>
          <SignalAccordionBody signal={signal} />
          <Button variant="ghost" size="sm" className="mt-2 h-auto px-0 text-primary" asChild>
            <Link href={signalHref}>Signal 평가 상세 보기</Link>
          </Button>
        </CollapsibleSection>
      </div>
    </DashboardSection>
  );
}
