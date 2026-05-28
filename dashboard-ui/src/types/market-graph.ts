export type MarketNodeCategory =
  | "company"
  | "sector"
  | "product"
  | "risk"
  | "theme"
  | "macro"
  | "competitor"
  | "customer";

export type MarketEdgeType =
  | "SUPPLIES"
  | "COMPETES_WITH"
  | "DEPENDS_ON"
  | "AFFECTED_BY"
  | "BENEFITS_FROM"
  | "EXPOSED_TO"
  | "RELATED_TO";

export interface MarketGraphNode {
  id: string;
  label: string;
  category: MarketNodeCategory;
  ticker?: string | null;
  is_center?: boolean;
  relevance: number;
  description?: string;
}

export interface MarketGraphEdge {
  id: string;
  source: string;
  target: string;
  edge_type: MarketEdgeType;
  direction?: "inbound" | "outbound" | "lateral" | string;
  confidence?: number;
  relevance: number;
  impact?: "positive" | "negative" | "neutral" | string;
  reason?: string;
  evidence?: string[];
}

export interface MarketGraphPayload {
  trace_id: string;
  query: string;
  center_ticker: string;
  center_company: string;
  nodes: MarketGraphNode[];
  edges: MarketGraphEdge[];
  risks: string[];
  themes: string[];
}

export interface RuntimeStatusPayload {
  trace_id: string;
  ticker: string;
  company_name: string;
  query: string;
  phase: string;
  label: string;
  step_count: number;
  last_step: string;
}

export interface RelationExplanationItem {
  source: string;
  target: string;
  relation: MarketEdgeType;
  direction: string;
  confidence: number;
  impact: string;
  explanation: string;
  evidence: string[];
}

export interface RelationExplanationPayload {
  trace_id: string;
  center_ticker: string;
  center_company: string;
  relations: RelationExplanationItem[];
}

export interface RiskExposureItem {
  risk: string;
  exposure_level: string;
  confidence: number;
  impact: string;
  evidence: string[];
}

export interface RiskExposurePayload {
  trace_id: string;
  center_ticker: string;
  center_company: string;
  risks: RiskExposureItem[];
}

export interface MarketInsightPayload {
  trace_id: string;
  center_ticker: string;
  center_company: string;
  market_story: string;
  bullish: string[];
  bearish: string[];
  key_relations: RelationExplanationItem[];
}

export interface MarketGraphFilters {
  minRelevance: number;
  category: MarketNodeCategory | "all";
  edgeType: MarketEdgeType | "all";
}
