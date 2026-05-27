"use client";

import { useCallback, useEffect, useState } from "react";
import type { MemoryData } from "@/types/dashboard";
import type { MemoryLayer, MemoryNodeData, MemoryStatus } from "@/types/memory-timeline";
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

function buildNodes(data: MemoryData): MemoryNodeData[] {
  const nodes: MemoryNodeData[] = [];

  const push = (items: unknown[], layer: MemoryLayer) => {
    if (!Array.isArray(items)) return;
    items.forEach((raw, idx) => {
      const item = raw as Record<string, unknown>;
      nodes.push({
        id: `${layer}-${idx}`,
        query: String(item.query ?? ""),
        summary: item.summary ? String(item.summary) : undefined,
        layer,
        importance_score: typeof item.importance_score === "number" ? item.importance_score : 0.5,
        status: deriveStatus({
          retention_action: item.retention_action as string | undefined,
          layer,
          importance_score: item.importance_score as number | undefined,
        }),
        timestamp: item.timestamp as string | undefined,
        persona: item.persona as string | undefined,
        retention_action: item.retention_action as string | undefined,
      });
    });
  };

  push(data.layered_memory?.short_term ?? [], "short_term");
  push(data.layered_memory?.mid_term ?? [], "mid_term");
  push(data.layered_memory?.long_term ?? [], "long_term");

  return nodes;
}

export function useMemoryTimeline(traceId?: string | null) {
  const [nodes, setNodes] = useState<MemoryNodeData[]>([]);
  const [query, setQuery] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async (id?: string | null) => {
    setStatus("loading");
    setError(null);
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
    load(traceId);
  }, [load, traceId]);

  return { nodes, query, status, error, reload: () => load(traceId) };
}
