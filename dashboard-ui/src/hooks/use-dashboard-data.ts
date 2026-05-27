"use client";

import { useCallback, useState } from "react";
import { ApiError, loadDashboardData } from "@/services/api";
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
  const [refreshKey, setRefreshKey] = useState(0);

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

  const loadLatest = useCallback(() => load(null), [load]);

  const loadByTraceId = useCallback(
    (id: string) => load(id),
    [load],
  );

  return {
    data,
    status,
    error,
    traceId,
    setTraceId,
    refreshKey,
    bumpRefresh: () => setRefreshKey((k) => k + 1),
    load,
    loadLatest,
    loadByTraceId,
  };
}
