/** traceId 기준 전체 Dashboard 패널 병렬 로드 */
import { getSignal, loadDashboardData } from "@/services/api";
import type { DashboardData } from "@/types/dashboard";
import type { SignalEvaluationData } from "@/types/signal-evaluation";

export interface RuntimePanelBundle {
  data: DashboardData;
  signal: SignalEvaluationData;
  traceId: string;
}

export async function loadRuntimePanels(
  traceId: string,
): Promise<RuntimePanelBundle> {
  const id = traceId.trim();
  if (!id) {
    throw new Error("trace_id가 필요합니다");
  }

  const [dashboard, signal] = await Promise.all([
    loadDashboardData(id),
    getSignal(id),
  ]);

  const resolved =
    dashboard.evaluation?.trace_id ||
    dashboard.retrieval?.trace_id ||
    id;

  return {
    data: dashboard,
    signal,
    traceId: resolved,
  };
}
