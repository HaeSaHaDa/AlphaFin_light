import type { StockChainEntity, StockChainLink } from "@/types/dashboard";

export type EntityTypeFilter =
  | "all"
  | "company"
  | "industry"
  | "product"
  | "market_event"
  | "price_change"
  | "supply_chain";

export interface GraphEntity extends StockChainEntity {
  id: string;
}

export interface GraphLink extends StockChainLink {
  id: string;
}

export interface TemporalEvent {
  period: string;
  label: string;
  relation?: string;
}

export interface PropagationStep {
  source: string;
  target: string;
  relation_type: string;
  impact_score: number;
}

export interface EventGraphFilters {
  entityType: EntityTypeFilter;
  minImpact: number;
  search: string;
  highlightEntities: string[];
}

export interface EventGraphPayload {
  traceId: string;
  query: string;
  ticker: string;
  centerName: string;
  centerTicker: string;
  entities: GraphEntity[];
  links: GraphLink[];
  propagationPath: PropagationStep[];
  temporalEvents: TemporalEvent[];
}
