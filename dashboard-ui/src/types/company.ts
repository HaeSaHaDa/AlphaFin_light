export interface TickerStats {
  news_count: number;
  disclosure_count: number;
  price_count: number;
  chunk_count: number;
  embedding_count: number;
  pending_embedding_count: number;
}

export interface DisclosurePreview {
  report_name: string;
  receipt_date: string;
  receipt_no?: string;
  disclosure_type?: string;
}

export interface CompanyResolveData {
  company_name: string;
  ticker: string;
  corp_code: string;
  market: string;
  stats: TickerStats;
  recent_disclosures: DisclosurePreview[];
  cache_ready: boolean;
}

export interface IngestionRunSummary {
  status: string;
  documents: number;
  chunks: number;
  embeddings: number;
  embeddings_created: number;
  embeddings_skipped: number;
  skipped_collectors: string[];
}
