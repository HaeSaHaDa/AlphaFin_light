import type { TraceData } from "@/types/dashboard";

const STEP_LABELS: Record<string, string> = {
  retrieval: "AI가 참고한 자료",
  context_assembly: "맥락 조립",
  character_analysis: "시장 분석",
  evaluation: "분석 신뢰도",
  reflection: "AI 자기 검토",
  memory_save: "시장 기억 저장",
  event_graph: "시장 연결 구조",
  stock_chain: "영향 흐름",
  result_save: "결과 저장",
};

interface AnalysisFlowPanelProps {
  trace: TraceData | null;
}

export function AnalysisFlowPanel({ trace }: AnalysisFlowPanelProps) {
  const steps = trace?.trace?.steps ?? [];
  const flow = trace?.pipeline_flow ?? [];

  if (!steps.length && !flow.length) {
    return (
      <p className="text-sm text-muted-foreground">분석 과정 데이터 없음</p>
    );
  }

  const items =
    steps.length > 0
      ? steps.map((s) => ({
          key: s.step ?? s.name ?? "",
          label: STEP_LABELS[s.step ?? s.name ?? ""] ?? s.step ?? s.name,
          status: s.status,
          summary: s.summary ?? s.detail,
        }))
      : flow.map((step) => ({
          key: step,
          label: STEP_LABELS[step] ?? step,
          status: "ok",
          summary: "",
        }));

  return (
    <ol className="space-y-2">
      {items.map((item, i) => (
        <li
          key={`${item.key}-${i}`}
          className="flex gap-3 rounded-lg border border-border/60 bg-muted/20 px-3 py-2 text-sm"
        >
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/20 text-xs font-bold text-primary">
            {i + 1}
          </span>
          <div className="min-w-0 flex-1">
            <p className="font-medium">{item.label}</p>
            {item.summary && (
              <p className="mt-0.5 line-clamp-2 text-xs text-muted-foreground">
                {item.summary}
              </p>
            )}
          </div>
          {item.status && (
            <span
              className={`shrink-0 text-xs ${
                item.status === "ok" ? "text-green-400" : "text-yellow-400"
              }`}
            >
              {item.status}
            </span>
          )}
        </li>
      ))}
    </ol>
  );
}
