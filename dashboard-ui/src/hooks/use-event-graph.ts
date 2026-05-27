"use client";

import { useCallback, useState } from "react";
import { ApiError, getStockChain, getTrace } from "@/services/api";
import { buildPayloadFromStockChain } from "@/lib/event-graph/transform";
import type { EventGraphFilters, EventGraphPayload } from "@/types/event-graph";
import type { GraphEntity } from "@/types/event-graph";

const DEFAULT_FILTERS: EventGraphFilters = {
  entityType: "all",
  minImpact: 0.7,
  search: "",
  highlightEntities: ["NVIDIA", "HBM", "삼성전자"],
};

export type EventGraphLoadStatus = "idle" | "loading" | "success" | "error";

export function useEventGraph() {
  const [payload, setPayload] = useState<EventGraphPayload | null>(null);
  const [filters, setFilters] = useState<EventGraphFilters>(DEFAULT_FILTERS);
  const [status, setStatus] = useState<EventGraphLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [selectedEntity, setSelectedEntity] = useState<GraphEntity | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  const updateFilters = useCallback((partial: Partial<EventGraphFilters>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);

  const load = useCallback(async (traceId?: string | null) => {
    setStatus("loading");
    setError(null);
    try {
      const [stockChain, traceRaw] = await Promise.all([
        getStockChain(),
        getTrace(traceId),
      ]);
      const completedAt =
        (traceRaw as { unified_result_summary?: { completed_at?: string } })
          ?.unified_result_summary?.completed_at ??
        (traceRaw as { completed_at?: string })?.completed_at;

      const built = buildPayloadFromStockChain(stockChain, completedAt);
      setPayload(built);
      setSelectedEntity(null);
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

  const connectedCount = selectedEntity
    ? (payload?.links.filter(
        (l) =>
          l.source === selectedEntity.name || l.target === selectedEntity.name,
      ).length ?? 0)
    : 0;

  const activeFilters: EventGraphFilters = {
    ...filters,
    highlightEntities: [
      ...filters.highlightEntities,
      ...(hoveredId ? [hoveredId] : []),
    ],
  };

  return {
    payload,
    filters: activeFilters,
    baseFilters: filters,
    updateFilters,
    status,
    error,
    selectedEntity,
    setSelectedEntity,
    setHoveredId,
    connectedCount,
    load,
    loadLatest,
  };
}
