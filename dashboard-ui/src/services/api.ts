import type {
  EvaluationData,
  MemoryData,
  ReflectionData,
  RetrievalData,
  StockChainData,
  TraceData,
} from "@/types/dashboard";
import type { SignalEvaluationData } from "@/types/signal-evaluation";
import type {
  MarketGraphPayload,
  MarketInsightPayload,
  RelationExplanationPayload,
  RiskExposurePayload,
  RuntimeStatusPayload,
} from "@/types/market-graph";
import type {
  CompanyResolveData,
  DisclosurePreview,
  IngestionRunSummary,
} from "@/types/company";

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

function requireTracePath(traceId: string | null | undefined, base: string): string {
  const id = traceId?.trim();
  if (!id) {
    throw new ApiError("trace_id가 필요합니다 (latest fallback 없음)", 400, base);
  }
  return `${base}/${encodeURIComponent(id)}`;
}

export function getRetrieval(traceId: string) {
  return fetchJson<RetrievalData>(requireTracePath(traceId, "/api/retrieval"));
}

export function getReflection(traceId: string) {
  return fetchJson<ReflectionData>(requireTracePath(traceId, "/api/reflection"));
}

export function getMemory(traceId: string) {
  return fetchJson<MemoryData>(requireTracePath(traceId, "/api/memory"));
}

export function getStockChain(traceId: string) {
  return fetchJson<StockChainData>(requireTracePath(traceId, "/api/stock-chain"));
}

export function getMarketGraph(traceId: string) {
  return fetchJson<MarketGraphPayload>(
    requireTracePath(traceId, "/api/market-graph"),
  );
}

export function getRuntimeStatus(traceId: string) {
  return fetchJson<RuntimeStatusPayload>(
    requireTracePath(traceId, "/api/runtime-status"),
  );
}

export function getMarketInsight(traceId: string) {
  return fetchJson<MarketInsightPayload>(
    requireTracePath(traceId, "/api/market-insight"),
  );
}

export function getRelationExplanation(traceId: string) {
  return fetchJson<RelationExplanationPayload>(
    requireTracePath(traceId, "/api/relation-explanation"),
  );
}

export function getRiskExposure(traceId: string) {
  return fetchJson<RiskExposurePayload>(
    requireTracePath(traceId, "/api/risk-exposure"),
  );
}

export interface EngineRunResponse {
  trace_id: string;
  status: string;
  query: string;
  ticker?: string;
  company?: CompanyResolveData | null;
  ingestion?: IngestionRunSummary | null;
  recent_disclosures?: DisclosurePreview[];
}

export interface IngestionRunResponse {
  ticker: string;
  company_name: string;
  corp_code: string;
  status: string;
  documents: number;
  chunks: number;
  embeddings: number;
}

export interface CompanySearchItem {
  company_name: string;
  ticker: string;
  corp_code?: string;
  market?: string;
  sector?: string;
  industry?: string;
}

export interface QueryRunRequest {
  ticker: string;
  company: string;
  keywords: string[];
  run_engine?: boolean;
}

export interface QueryRunResponse {
  status: string;
  trace_id: string;
  ticker: string;
  company_name: string;
  runtime_query: string;
  keywords: string[];
  runtime_logs?: string[];
  company: CompanyResolveData | null;
}

export async function runIngestion(company: string, force = false) {
  const url = `${API_BASE}/api/ingestion/run`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ company, force }),
    cache: "no-store",
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new ApiError(
      detail || `Ingestion failed: ${res.status}`,
      res.status,
      "/api/ingestion/run",
    );
  }
  return res.json() as Promise<IngestionRunResponse>;
}

export async function searchCompany(q: string) {
  const path = `/api/company/search?q=${encodeURIComponent(q)}`;
  return fetchJson<CompanySearchItem[]>(path);
}

export async function getCompanyByTicker(ticker: string) {
  return fetchJson<CompanySearchItem>(
    `/api/company/${encodeURIComponent(ticker)}`,
  );
}

export async function runQuery(req: QueryRunRequest) {
  const url = `${API_BASE}/api/query/run`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ticker: req.ticker,
      company: req.company,
      keywords: req.keywords,
      run_engine: req.run_engine ?? true,
    }),
    cache: "no-store",
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new ApiError(
      detail || `Query run failed: ${res.status}`,
      res.status,
      "/api/query/run",
    );
  }
  return res.json() as Promise<QueryRunResponse>;
}

export async function resolveCompany(q: string, prefetch = true) {
  const path = `/api/company/resolve?q=${encodeURIComponent(q)}&prefetch=${prefetch}`;
  return fetchJson<CompanyResolveData>(path);
}

export interface SearchIngestResponse {
  status: string;
  query: string;
  company: CompanyResolveData | null;
  ingestion: IngestionRunSummary | null;
  trace_id: string;
  engine_status: string;
  error?: string | null;
}

export async function searchAndIngest(
  query: string,
  options: { runEngine?: boolean; force?: boolean } = {},
) {
  const url = `${API_BASE}/api/company/search-ingest`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      run_engine: options.runEngine ?? true,
      force: options.force ?? false,
    }),
    cache: "no-store",
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new ApiError(
      detail || `Search failed: ${res.status}`,
      res.status,
      "/api/company/search-ingest",
    );
  }
  return res.json() as Promise<SearchIngestResponse>;
}

export async function runEngine(
  query: string,
  persona = "growth_investor",
): Promise<EngineRunResponse> {
  const url = `${API_BASE}/api/engine/run`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, persona }),
    cache: "no-store",
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new ApiError(
      detail || `Engine run failed: ${res.status}`,
      res.status,
      "/api/engine/run",
    );
  }
  return res.json() as Promise<EngineRunResponse>;
}

export function getTrace(traceId: string) {
  return fetchJson<TraceData>(requireTracePath(traceId, "/api/trace"));
}

export function getEvaluation(traceId: string) {
  return fetchJson<EvaluationData>(requireTracePath(traceId, "/api/evaluation"));
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

export async function loadDashboardData(traceId: string) {
  const id = traceId.trim();
  if (!id) {
    throw new ApiError("trace_id가 필요합니다", 400, "/api/dashboard");
  }
  const [retrieval, reflection, memory, stockChain, traceRaw, evaluation] =
    await Promise.all([
      getRetrieval(id),
      getReflection(id),
      getMemory(id),
      getStockChain(id),
      getTrace(id),
      getEvaluation(id),
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

export function getSignal(traceId: string) {
  return fetchJson<SignalEvaluationData>(requireTracePath(traceId, "/api/signal"));
}

export interface CacheStatusResponse {
  count: number;
  tickers: Array<Record<string, unknown>>;
  presentation_mode: boolean;
}

export interface PresentationModeResponse {
  status: string;
  enabled: boolean;
  active: boolean;
}

async function postJson<T>(path: string): Promise<T> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    method: "POST",
    cache: "no-store",
  });
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

export function getCacheStatus() {
  return fetchJson<CacheStatusResponse>("/api/cache/status");
}

export function enablePresentationMode() {
  return postJson<PresentationModeResponse>("/api/presentation-mode/enable");
}

export function disablePresentationMode() {
  return postJson<PresentationModeResponse>("/api/presentation-mode/disable");
}

export { API_BASE };
