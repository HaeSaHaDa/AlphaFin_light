"use client";

import { useCallback, useState } from "react";
import { ApiError, getEvaluation, getReflection, getRetrieval, getTrace } from "@/services/api";
import type { AnalysisLoadStatus, AnalysisViewerData } from "@/types/analysis";
import type { TraceData } from "@/types/dashboard";

const EMPTY: AnalysisViewerData = {
  retrieval: null,
  reflection: null,
  trace: null,
  evaluation: null,
};

function normalizeTraceById(
  raw: TraceData | Record<string, unknown>,
  traceId: string,
): TraceData {
  if (raw && "pipeline_flow" in raw) return raw as TraceData;
  const t = raw as {
    trace_id?: string;
    steps?: TraceData["trace"]["steps"];
    started_at?: string;
    completed_at?: string;
    query?: string;
  };
  return {
    trace: {
      trace_id: t.trace_id ?? traceId,
      steps: t.steps,
    },
    unified_result_summary: {
      trace_id: t.trace_id ?? traceId,
      query: t.query ?? "",
      completed_at: t.completed_at ?? "",
    },
    pipeline_flow: [
      "retrieval",
      "context_assembly",
      "reasoning",
      "reflection",
      "memory_update",
      "stock_chain",
      "evaluation",
    ],
  };
}

export function useAnalysisViewer() {
  const [data, setData] = useState<AnalysisViewerData>(EMPTY);
  const [status, setStatus] = useState<AnalysisLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [traceId, setTraceId] = useState<string | null>(null);

  const load = useCallback(async (id?: string | null) => {
    setStatus("loading");
    setError(null);
    const target = id?.trim() || null;
    try {
      const [retrieval, reflection, traceRaw, evaluation] = await Promise.all([
        getRetrieval(target),
        getReflection(target),
        getTrace(target),
        getEvaluation(target),
      ]);
      const resolved =
        evaluation?.trace_id || retrieval?.trace_id || target || "";
      const trace = normalizeTraceById(
        traceRaw as TraceData | Record<string, unknown>,
        resolved,
      );
      if (!trace.unified_result_summary.query && retrieval?.query) {
        trace.unified_result_summary.query = retrieval.query;
      }
      setData({
        retrieval: retrieval as AnalysisViewerData["retrieval"],
        reflection,
        trace,
        evaluation,
      });
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
  const loadByTraceId = useCallback((id: string) => load(id), [load]);

  return { data, status, error, traceId, load, loadLatest, loadByTraceId };
}
