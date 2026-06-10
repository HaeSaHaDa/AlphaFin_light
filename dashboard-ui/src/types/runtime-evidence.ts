export interface RuntimeEvidenceItem {
  chunk_id?: number;
  document_type?: string;
  score?: number;
  merge_score?: number;
  source_priority?: string;
  title?: string;
  text?: string;
  chunk_text?: string;
  report_name?: string;
  section_name?: string;
  report_type?: string;
  priority?: string;
  source?: string;
  url?: string;
  published_at?: string;
}

export interface RuntimeContextPayload {
  trace_id?: string;
  ticker: string;
  query: string;
  news_chunks: RuntimeEvidenceItem[];
  disclosure_chunks: RuntimeEvidenceItem[];
  merged_evidence: RuntimeEvidenceItem[];
  reasoning_context: string[];
  source_breakdown: Record<string, number>;
  has_disclosure?: boolean;
  disclosure_collect_status?: string;
  disclosure_priority?: string;
}

export interface RuntimeEvidencePayload {
  trace_id: string;
  ticker: string;
  query: string;
  merged_evidence: RuntimeEvidenceItem[];
  reasoning_context: string[];
  source_breakdown: Record<string, number>;
  has_disclosure: boolean;
  analysis_summary?: string;
  bullish_factors?: string[];
  bearish_factors?: string[];
  risks?: string[];
}
