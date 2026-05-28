"use client";

import { useCallback, useState } from "react";
import { ApiError, getRetrieval, getStockChain, getTrace } from "@/services/api";
import { buildPayloadFromStockChain } from "@/lib/event-graph/transform";
import type { EventGraphFilters, EventGraphPayload } from "@/types/event-graph";
import type { GraphEntity } from "@/types/event-graph";

const DEFAULT_FILTERS: EventGraphFilters = {
  entityType: "all",
  minImpact: 0.7,
  search: "",
  highlightEntities: [],
};

export type EventGraphLoadStatus = "idle" | "loading" | "success" | "error";

export function useEventGraph() {
  const [payload, setPayload] = useState<EventGraphPayload | null>(null);
  const [filters, setFilters] = useState<EventGraphFilters>(DEFAULT_FILTERS);
  const [status, setStatus] = useState<EventGraphLoadStatus>("idle");
  const [error, setError] = useState<string | null>(null);
  const [selectedEntity, setSelectedEntity] = useState<GraphEntity | null>(null);
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [activeTraceId, setActiveTraceId] = useState<string | null>(null);

  const updateFilters = useCallback((partial: Partial<EventGraphFilters>) => {
    setFilters((prev) => ({ ...prev, ...partial }));
  }, []);

  const load = useCallback(async (traceId: string) => {
    const id = traceId.trim();
    if (!id) {
      setStatus("idle");
      setPayload(null);
      return;
    }
    setStatus("loading");
    setError(null);
    setActiveTraceId(id);
    try {
      const [stockChain, traceRaw, retrieval] = await Promise.all([
        getStockChain(id),
        getTrace(id),
        getRetrieval(id).catch(() => null),
      ]);
      const completedAt =
        (traceRaw as { unified_result_summary?: { completed_at?: string } })
          ?.unified_result_summary?.completed_at ??
        (traceRaw as { completed_at?: string })?.completed_at;

      const chunks = retrieval?.chunks ?? [];
      const built = buildPayloadFromStockChain(
        stockChain,
        completedAt,
        chunks,
      );
      built.traceId = id;
      setPayload(built);
      setFilters((prev) => ({
        ...prev,
        highlightEntities: built.centerName ? [built.centerName] : [],
      }));
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
    activeTraceId,
    load,
  };
}
