"use client";

import {
  Bar,
  BarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { MarketComparison, SignalMetrics } from "@/types/signal-evaluation";

interface AccuracyPanelProps {
  metrics: SignalMetrics;
  market: MarketComparison;
}

export function AccuracyPanel({ metrics, market }: AccuracyPanelProps) {
  const hasMarketOutcome = market.actual_direction !== "unavailable";
  const chartData = [
    { name: "적중", value: metrics.correct_count },
    { name: "미적중", value: metrics.total_signals - metrics.correct_count },
  ];

  const accPct = Math.round(metrics.direction_accuracy * 100);

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card/60 p-4">
      <h3 className="text-sm font-semibold">방향 예측 정확도 · 예측 적중률</h3>

      {hasMarketOutcome ? (
        <>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-md bg-muted/30 p-3 text-center">
              <p className="text-2xl font-bold text-primary">{accPct}%</p>
              <p className="text-xs text-muted-foreground">방향 예측 정확도</p>
            </div>
            <div className="rounded-md bg-muted/30 p-3 text-center">
              <p className="text-2xl font-bold text-primary">{metrics.hit_ratio_pct}%</p>
              <p className="text-xs text-muted-foreground">예측 적중률</p>
            </div>
          </div>
          <p className="text-xs text-muted-foreground">
            총 Signal {metrics.total_signals}건 · 정확한 방향 예측{" "}
            {metrics.correct_count}건
          </p>
        </>
      ) : (
        <p className="rounded-md bg-muted/30 p-3 text-sm text-muted-foreground">
          실제 시장 결과가 연동되지 않아 정확도와 적중률을 계산하지 않습니다.
        </p>
      )}

      <div className="rounded-md border border-border bg-background/50 p-3 text-sm">
        <p className="text-xs text-muted-foreground">실제 시장 변화 (trace 기준)</p>
        {hasMarketOutcome ? (
          <p className="mt-1 font-medium">
            {market.period_label}:{" "}
            <span
              className={
                market.price_change_pct >= 0 ? "text-green-400" : "text-red-400"
              }
            >
              {market.price_change_pct >= 0 ? "+" : ""}
              {market.price_change_pct}%
            </span>
            {" · "}
            <span
              className={
                market.direction_correct ? "text-green-400" : "text-red-400"
              }
            >
              {market.direction_correct ? "방향 일치" : "방향 불일치"}
            </span>
          </p>
        ) : (
          <p className="mt-1 text-muted-foreground">{market.period_label}</p>
        )}
      </div>

      {hasMarketOutcome && metrics.total_signals > 0 && (
        <div className="h-32">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis allowDecimals={false} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="value" fill="hsl(var(--primary))" radius={4} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
