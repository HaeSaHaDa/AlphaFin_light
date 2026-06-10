import {
  createInitialRuntimeState,
  EMPTY_DASHBOARD,
  type RuntimeTraceState,
} from "./runtime-trace-store";
import { extractTickerMetaFromDashboard } from "./runtime-ticker-meta";

/** query 실행 전 전체 상태 초기화 */
export function resetRuntimeForNewQuery(
  state: RuntimeTraceState,
  ticker: string,
  companyName: string,
): RuntimeTraceState {
  return {
    ...createInitialRuntimeState(),
    selectedTicker: ticker,
    companyName,
    phase: "running_query",
    panelStatus: "loading",
    loadingMessage: "뉴스·공시 Retrieval 및 Runtime 분석 실행 중…",
  };
}

/** 패널 로드 시작 */
export function beginPanelLoad(state: RuntimeTraceState): RuntimeTraceState {
  return {
    ...state,
    phase: "loading_panels",
    panelStatus: "loading",
    loadingMessage: "뉴스 Retrieval · 공시 Retrieval · Event Consolidation · 패널 동기화 중…",
    data: EMPTY_DASHBOARD,
    signal: null,
  };
}

/** 패널 로드 완료 */
export function applyPanelBundle(
  state: RuntimeTraceState,
  bundle: {
    traceId: string;
    data: RuntimeTraceState["data"];
    signal: RuntimeTraceState["signal"];
    runtimeQuery?: string;
  },
): RuntimeTraceState {
  const meta = extractTickerMetaFromDashboard(bundle.data, bundle.runtimeQuery, {
    selectedTicker: state.selectedTicker,
    companyName: state.companyName,
  });
  return {
    ...state,
    traceId: bundle.traceId,
    data: bundle.data,
    signal: bundle.signal,
    selectedTicker: meta.selectedTicker ?? state.selectedTicker,
    companyName: meta.companyName ?? state.companyName,
    runtimeQuery: meta.runtimeQuery ?? bundle.runtimeQuery ?? state.runtimeQuery,
    phase: "ready",
    panelStatus: "success",
    loadingMessage: null,
    error: null,
  };
}
