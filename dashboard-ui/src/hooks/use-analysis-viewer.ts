"use client";

import { useCallback, useState } from "react";
import {
  ApiError,
  getEvaluation,
  getReflection,
  getRetrieval,
  getTrace,
  normalizeTrace,
} from "@/services/api";
import type { AnalysisLoadStatus, AnalysisViewerData } from "@/types/analysis";
import type { TraceData } from "@/types/dashboard";

const EMPTY: AnalysisViewerData = {
  retrieval: null,
  reflection: null,
  trace: null,
  evaluation: null,
};

export function useAnalysisViewer() {
  const [data, setData] = useState<AnalysisViewerData>(EMPTY);
  const [status, setStatus] = useState<AnalysisLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [traceId, setTraceId] = useState<string | null>(null);

  const loadByTraceId = useCallback(async (id: string) => {
    const target = id.trim();
    if (!target) {
      setData(EMPTY);
      setTraceId(null);
      setStatus("idle");
      return;
    }
    setStatus("loading");
    setError(null);
    try {
      const [retrieval, reflection, traceRaw, evaluation] = await Promise.all([
        getRetrieval(target),
        getReflection(target),
        getTrace(target),
        getEvaluation(target),
      ]);
      const resolved =
        evaluation?.trace_id || retrieval?.trace_id || target;
      const trace = normalizeTrace(
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
      setTraceId(resolved);
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

  return { data, status, error, traceId, loadByTraceId };
}
