"use client";

import { EvaluationScorePanel } from "@/components/evaluation/evaluation-score-panel";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { EvaluationData, LoadStatus } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  evaluation: EvaluationData | null;
}

export function RuntimeEvaluationPanel({ traceId, status, evaluation }: Props) {
  return (
    <RuntimePanelShell traceId={traceId} status={status} title="Evaluation">
      <EvaluationScorePanel data={evaluation} status={status} />
    </RuntimePanelShell>
  );
}
