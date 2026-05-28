"use client";

import { useCallback, useState } from "react";
import {
  ApiError,
  getMarketGraph,
  getMarketInsight,
  getRelationExplanation,
  getRiskExposure,
  getRuntimeStatus,
} from "@/services/api";
import type {
  MarketGraphFilters,
  MarketGraphPayload,
  MarketInsightPayload,
  RelationExplanationPayload,
  RiskExposurePayload,
  RuntimeStatusPayload,
} from "@/types/market-graph";

const DEFAULT_FILTERS: MarketGraphFilters = {
  minRelevance: 0.45,
  category: "all",
  edgeType: "all",
};

export type MarketGraphLoadStatus = "idle" | "loading" | "success" | "error";

export function useMarketGraph() {
  const [payload, setPayload] = useState<MarketGraphPayload | null>(null);
  const [runtimeStatus, setRuntimeStatus] = useState<RuntimeStatusPayload | null>(
    null,
  );
  const [marketInsight, setMarketInsight] = useState<MarketInsightPayload | null>(null);
  const [relationExplanation, setRelationExplanation] =
    useState<RelationExplanationPayload | null>(null);
  const [riskExposure, setRiskExposure] = useState<RiskExposurePayload | null>(null);
  const [filters, setFilters] = useState<MarketGraphFilters>(DEFAULT_FILTERS);
  const [status, setStatus] = useState<MarketGraphLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);

  const updateFilters = useCallback((partial: Partial<MarketGraphFilters>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);

  const load = useCallback(async (traceId: string) => {
    const id = traceId.trim();
    if (!id) {
      setPayload(null);
      setRuntimeStatus(null);
      setStatus("idle");
      return;
    }
    setStatus("loading");
    setError(null);
    try {
      const [graph, rt] = await Promise.all([
        getMarketGraph(id),
        getRuntimeStatus(id).catch(() => null),
      ]);
      const [insight, relationExp, riskExp] = await Promise.all([
        getMarketInsight(id).catch(() => null),
        getRelationExplanation(id).catch(() => null),
        getRiskExposure(id).catch(() => null),
      ]);
      setPayload(graph);
      setRuntimeStatus(rt);
      setMarketInsight(insight);
      setRelationExplanation(relationExp);
      setRiskExposure(riskExp);
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

  return {
    payload,
    runtimeStatus,
    marketInsight,
    relationExplanation,
    riskExposure,
    filters,
    updateFilters,
    status,
    error,
    load,
  };
}
