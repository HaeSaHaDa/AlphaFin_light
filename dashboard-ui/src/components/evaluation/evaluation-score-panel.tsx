"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import { formatScore } from "@/lib/utils";
import type { EvaluationData, LoadStatus } from "@/types/dashboard";

interface EvaluationScorePanelProps {
  data: EvaluationData | null;
  status: LoadStatus;
}

export function EvaluationScorePanel({
  data,
  status,
}: EvaluationScorePanelProps) {
  const chartData = data
    ? [
        { name: "Retrieval", score: data.retrieval_score ?? 0 },
        { name: "Reasoning", score: data.reasoning_score ?? 0 },
        { name: "Reflection", score: data.reflection_score ?? 0 },
        { name: "Memory", score: data.memory_score ?? 0 },
        { name: "Stock Chain", score: data.stock_chain_score ?? 0 },
      ]
    : [];

  const risk = data?.hallucination_risk as {
    risk_level?: string;
    reasons?: string[];
  };
  const consistency = data?.consistency as {
    consistency_score?: number;
  };

  return (
    <PanelShell
      title="Evaluation Score"
      subtitle={data?.evaluated_at}
      status={status}
      empty={!data}
      className="max-h-none"
    >
      {data && (
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-3">
            <div className="rounded-lg border border-primary/50 bg-primary/10 px-4 py-3">
              <p className="text-xs text-muted-foreground">Overall</p>
              <p className="text-3xl font-bold text-primary">
                {formatScore(data.overall_score)}
              </p>
            </div>
            <Badge
              variant={
                risk?.risk_level === "low" ? "success" : "warning"
              }
            >
              hallucination: {risk?.risk_level ?? "—"}
            </Badge>
            {consistency?.consistency_score != null && (
              <Badge variant="outline">
                consistency:{" "}
                {formatScore(consistency.consistency_score)}
              </Badge>
            )}
          </div>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis
                  dataKey="name"
                  tick={{ fill: "#a1a1aa", fontSize: 10 }}
                />
                <YAxis
                  domain={[0, 1]}
                  tick={{ fill: "#a1a1aa", fontSize: 10 }}
                  tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                />
                <Tooltip
                  formatter={(v: number) => formatScore(v)}
                  contentStyle={{
                    background: "#18181b",
                    border: "1px solid #3f3f46",
                  }}
                />
                <Bar dataKey="score" fill="hsl(210 90% 55%)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </PanelShell>
  );
}
