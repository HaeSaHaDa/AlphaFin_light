"use client";

import { useCallback, useEffect, useState } from "react";
import { getSignal } from "@/services/api";
import type { SignalEvaluationData } from "@/types/signal-evaluation";

export function useSignalEvaluation(traceId?: string | null) {
  const [data, setData] = useState<SignalEvaluationData | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (id: string) => {
    setStatus("loading");
    setError(null);
    setData(null);
    try {
      const result = await getSignal(id);
      setData(result);
      setStatus("success");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Signal 로드 실패");
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    const id = traceId?.trim();
    if (!id) {
      setData(null);
      setStatus("idle");
      setError(null);
      return;
    }
    load(id);
  }, [load, traceId]);

  return {
    data,
    status,
    error,
    reload: () => {
      const id = traceId?.trim();
      if (id) return load(id);
    },
  };
}
