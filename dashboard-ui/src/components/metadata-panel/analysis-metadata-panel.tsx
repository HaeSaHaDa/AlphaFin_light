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
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { formatScore } from "@/lib/utils";
import type { AnalysisLoadStatus } from "@/types/analysis";
import type { EvaluationData, TraceData } from "@/types/dashboard";

const ENGINE_VERSION = "AlphaFin LTE 1.0";

interface AnalysisMetadataPanelProps {
  trace: TraceData | null;
  evaluation: EvaluationData | null;
  status: AnalysisLoadStatus;
}

export function AnalysisMetadataPanel({
  trace,
  evaluation,
  status,
}: AnalysisMetadataPanelProps) {
  const traceId =
    evaluation?.trace_id || trace?.unified_result_summary?.trace_id || "—";
  const completedAt = trace?.unified_result_summary?.completed_at ?? "—";
  const risk = evaluation?.hallucination_risk as { risk_level?: string };
  const loading = status === "loading";

  const chartData = evaluation
    ? [
        { name: "Retrieval", score: evaluation.retrieval_score ?? 0 },
        { name: "Reasoning", score: evaluation.reasoning_score ?? 0 },
        { name: "Reflection", score: evaluation.reflection_score ?? 0 },
        { name: "Memory", score: evaluation.memory_score ?? 0 },
        { name: "Chain", score: evaluation.stock_chain_score ?? 0 },
      ]
    : [];

  return (
    <Card className="border-primary/20">
      <CardHeader>
        <CardTitle>Analysis Metadata</CardTitle>
        <p className="text-xs text-muted-foreground">trace · execution · risk</p>
      </CardHeader>
      <CardContent className="space-y-4">
        {loading ? (
          <p className="text-sm text-muted-foreground">Loading…</p>
        ) : (
          <>
            <div className="flex flex-wrap gap-2 text-xs">
              <Badge variant="secondary">trace: {traceId}</Badge>
              <Badge variant="outline">completed: {completedAt}</Badge>
              <Badge variant="outline">{ENGINE_VERSION}</Badge>
              <Badge
                variant={risk?.risk_level === "low" ? "success" : "warning"}
              >
                hallucination: {risk?.risk_level ?? "—"}
              </Badge>
              {evaluation?.overall_score != null && (
                <Badge variant="default">
                  overall {formatScore(evaluation.overall_score)}
                </Badge>
              )}
            </div>
            {chartData.length > 0 && (
              <div className="h-[160px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="name" tick={{ fill: "#a1a1aa", fontSize: 10 }} />
                    <YAxis domain={[0, 1]} tick={{ fill: "#a1a1aa", fontSize: 10 }} />
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
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
}
