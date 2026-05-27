"use client";

import { useCallback, useState } from "react";
import { ApiError, loadDashboardData, runEngine } from "@/services/api";
import type { DashboardData, LoadStatus } from "@/types/dashboard";

const EMPTY: DashboardData = {
  retrieval: null,
  reflection: null,
  memory: null,
  stockChain: null,
  trace: null,
  evaluation: null,
};

export function useDashboardData() {
  const [data, setData] = useState<DashboardData>(EMPTY);
  const [status, setStatus] = useState<LoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [traceId, setTraceId] = useState<string | null>(null);
  const [engineRunning, setEngineRunning] = useState(false);

  const load = useCallback(async (id?: string | null) => {
    setStatus("loading");
    setError(null);
    const targetId = id?.trim() || null;
    try {
      const result = await loadDashboardData(targetId);
      setData({
        retrieval: result.retrieval,
        reflection: result.reflection,
        memory: result.memory,
        stockChain: result.stockChain,
        trace: result.trace,
        evaluation: result.evaluation,
      });
      const resolved =
        result.evaluation?.trace_id ||
        result.retrieval?.trace_id ||
        targetId;
      setTraceId(resolved || null);
      setStatus("success");
    } catch (e) {
      const msg =
        e instanceof ApiError
          ? `API 오류 (${e.status}): ${e.path}`
          : e instanceof Error
            ? e.message
            : "알 수 없는 오류";
      setError(msg);
      setStatus("error");
    }
  }, []);

  /**
   * Unified Engine을 실행한 뒤 반환된 trace_id로 Dashboard를 로드한다.
   * query 변경 시 이전 결과를 초기화한다.
   */
  const runAndLoad = useCallback(
    async (query: string) => {
      setData(EMPTY);
      setTraceId(null);
      setError(null);
      setEngineRunning(true);
      setStatus("loading");
      try {
        const resp = await runEngine(query);
        setEngineRunning(false);
        await load(resp.trace_id);
      } catch (e) {
        setEngineRunning(false);
        const msg =
          e instanceof ApiError
            ? `Engine 실행 오류 (${e.status}): ${e.message}`
            : e instanceof Error
              ? e.message
              : "알 수 없는 오류";
        setError(msg);
        setStatus("error");
      }
    },
    [load],
  );

  const loadLatest = useCallback(() => load(null), [load]);
  const loadByTraceId = useCallback((id: string) => load(id), [load]);

  return {
    data,
    status,
    error,
    traceId,
    engineRunning,
    load,
    loadLatest,
    loadByTraceId,
    runAndLoad,
  };
}
