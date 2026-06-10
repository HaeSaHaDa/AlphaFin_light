"use client";

import { useCallback, useEffect, useState } from "react";
import type { MemoryData } from "@/types/dashboard";
import type {
  MemoryEvidence,
  MemoryLayer,
  MemoryNodeData,
  MemoryStatus,
} from "@/types/memory-timeline";
import { getMemory } from "@/services/api";

function deriveStatus(item: {
  retention_action?: string;
  layer?: string;
  importance_score?: number;
}): MemoryStatus {
  const action = item.retention_action ?? "";
  if (action === "promote") return "promoted";
  if (action === "decay" || action === "delete") return "decayed";
  if (action === "archive") return "archived";
  return "active";
}

function layerFromStr(s?: string): MemoryLayer {
  if (s === "mid_term") return "mid_term";
  if (s === "long_term") return "long_term";
  return "short_term";
}

const LAYER_RANK: Record<MemoryLayer, number> = {
  short_term: 1,
  mid_term: 2,
  long_term: 3,
};

function memoryKey(item: Record<string, unknown>): string {
  const id = item.memory_id as string | undefined;
  if (id) return id;
  const q = String(item.query ?? "");
  const s = String(item.summary ?? "").slice(0, 80);
  return `fp:${q}::${s}`;
}

function collapseNodesByMemoryId(
  entries: { item: Record<string, unknown>; fileLayer: MemoryLayer }[],
): { item: Record<string, unknown>; layer: MemoryLayer }[] {
  const best = new Map<string, { item: Record<string, unknown>; layer: MemoryLayer }>();
  for (const { item, fileLayer } of entries) {
    const key = memoryKey(item);
    const declared = (item.memory_layer as MemoryLayer | undefined) ?? fileLayer;
    const cur = best.get(key);
    if (!cur || LAYER_RANK[declared] >= LAYER_RANK[cur.layer]) {
      best.set(key, { item: { ...item, memory_layer: declared }, layer: declared });
    }
  }
  return Array.from(best.values());
}

function buildNodes(data: MemoryData): MemoryNodeData[] {
  const raw: { item: Record<string, unknown>; fileLayer: MemoryLayer }[] = [];
  const collect = (items: unknown[], layer: MemoryLayer) => {
    if (!Array.isArray(items)) return;
    for (const row of items) {
      raw.push({ item: row as Record<string, unknown>, fileLayer: layer });
    }
  };
  collect(data.layered_memory?.short_term ?? [], "short_term");
  collect(data.layered_memory?.mid_term ?? [], "mid_term");
  collect(data.layered_memory?.long_term ?? [], "long_term");

  const collapsed = collapseNodesByMemoryId(raw);

  return collapsed.map(({ item, layer }, idx) => ({
    id: String(item.memory_id ?? `${layer}-${idx}`),
    query: String(item.query ?? ""),
    summary: item.summary ? String(item.summary) : undefined,
    layer,
    importance_score:
      typeof item.importance_score === "number" ? item.importance_score : 0.5,
    status: deriveStatus({
      retention_action: item.retention_action as string | undefined,
      layer,
      importance_score: item.importance_score as number | undefined,
    }),
    timestamp: item.timestamp as string | undefined,
    persona: item.persona as string | undefined,
    retention_action: item.retention_action as string | undefined,
    evidence: Array.isArray(item.referenced_chunks)
      ? (item.referenced_chunks as MemoryEvidence[])
      : [],
  }));
}

export function useMemoryTimeline(traceId?: string | null) {
  const [nodes, setNodes] = useState<MemoryNodeData[]>([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (id: string) => {
    setStatus("loading");
    setError(null);
    setNodes([]);
    try {
      const data = await getMemory(id);
      setNodes(buildNodes(data));
      setQuery(data.query ?? "");
      setStatus("success");
    } catch (e) {
      setError(e instanceof Error ? e.message : "데이터 로드 실패");
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    const id = traceId?.trim();
    if (!id) {
      setNodes([]);
      setQuery("");
      setStatus("idle");
      setError(null);
      return;
    }
    load(id);
  }, [load, traceId]);

  return {
    nodes,
    query,
    status,
    error,
    reload: () => {
      const id = traceId?.trim();
      if (id) return load(id);
    },
  };
}
