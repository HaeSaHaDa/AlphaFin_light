export type SignalType = "bullish" | "neutral" | "bearish";

export interface CurrentSignal {
  signal: SignalType;
  display_label: string;
  confidence: number;
  reason: string[];
}

export interface MarketComparison {
  price_change_pct: number;
  period_label: string;
  direction_correct: boolean;
  actual_direction: string;
}

export interface SignalMetrics {
  direction_accuracy: number;
  hit_ratio_pct: number;
  total_signals: number;
  correct_count: number;
}

export interface TimelineEntry {
  period: string;
  signal: SignalType;
  display_label: string;
  price_change_pct?: number;
}

export interface SignalEvaluationData {
  trace_id: string;
  query: string;
  ticker: string;
  current_signal: CurrentSignal;
  market_comparison: MarketComparison;
  confidence_evaluation: {
    confidence?: number;
    direction_correct?: boolean;
    outcome?: string;
    label?: string;
    is_high_confidence?: boolean;
  };
  metrics: SignalMetrics;
  timeline: TimelineEntry[];
  history: Array<TimelineEntry & { direction_correct?: boolean; confidence?: number }>;
  confidence_summary: {
    avg_confidence?: number;
    high_confidence_hit_rate?: number;
    high_confidence_count?: number;
  };
  summary_text: string;
}
