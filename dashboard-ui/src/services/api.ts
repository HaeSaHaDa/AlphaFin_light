import type {
  EvaluationData,
  MemoryData,
  ReflectionData,
  RetrievalData,
  StockChainData,
  TraceData,
} from "@/types/dashboard";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ||
  "http://localhost:8000";

export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public path: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchJson<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new ApiError(
      detail || `Request failed: ${res.status}`,
      res.status,
      path,
    );
  }
  return res.json() as Promise<T>;
}

function suffix(traceId?: string | null): string {
  return traceId ? `/${encodeURIComponent(traceId)}` : "/latest";
}

export function getRetrieval(traceId?: string | null) {
  return fetchJson<RetrievalData>(`/api/retrieval${suffix(traceId)}`);
}

export function getReflection(traceId?: string | null) {
  return fetchJson<ReflectionData>(`/api/reflection${suffix(traceId)}`);
}

export function getMemory() {
  return fetchJson<MemoryData>("/api/memory/latest");
}

export function getStockChain() {
  return fetchJson<StockChainData>("/api/stock-chain/latest");
}

export function getTrace(traceId?: string | null) {
  return fetchJson<TraceData>(`/api/trace${suffix(traceId)}`);
}

export function getEvaluation(traceId?: string | null) {
  return fetchJson<EvaluationData>(`/api/evaluation${suffix(traceId)}`);
}

const DEFAULT_PIPELINE = [
  "retrieval",
  "context_assembly",
  "character_analysis",
  "evaluation",
  "reflection",
  "memory_save",
  "importance_update",
  "temporal_tracking",
  "event_graph",
  "stock_chain",
  "result_save",
];

function normalizeTrace(
  raw: TraceData | Record<string, unknown>,
  traceId?: string | null,
): TraceData {
  if (raw && "pipeline_flow" in raw && Array.isArray(raw.pipeline_flow)) {
    return raw as TraceData;
  }
  const trace = raw as { trace_id?: string; steps?: TraceData["trace"]["steps"] };
  return {
    trace: { trace_id: trace.trace_id, steps: trace.steps },
    unified_result_summary: {
      trace_id: trace.trace_id ?? traceId ?? "",
      query: "",
      completed_at: "",
    },
    pipeline_flow: DEFAULT_PIPELINE,
  };
}

export async function loadDashboardData(traceId?: string | null) {
  const [retrieval, reflection, memory, stockChain, traceRaw, evaluation] =
    await Promise.all([
      getRetrieval(traceId),
      getReflection(traceId),
      getMemory(),
      getStockChain(),
      getTrace(traceId),
      getEvaluation(traceId),
    ]);
  const trace = normalizeTrace(
    traceRaw as TraceData | Record<string, unknown>,
    traceId,
  );
  if (!trace.unified_result_summary.query && retrieval?.query) {
    trace.unified_result_summary.query = retrieval.query;
  }
  return { retrieval, reflection, memory, stockChain, trace, evaluation };
}

export { API_BASE };
