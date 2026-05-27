import type { MemoryNodeData } from "@/types/memory-timeline";

interface MemorySummaryPanelProps {
  nodes: MemoryNodeData[];
  query: string;
}

export function MemorySummaryPanel({ nodes, query }: MemorySummaryPanelProps) {
  const longTerm = nodes.filter((n) => n.layer === "long_term" && n.status !== "decayed");
  const promoted = nodes.filter((n) => n.status === "promoted");
  const topNodes = [...nodes]
    .filter((n) => n.status !== "decayed")
    .sort((a, b) => b.importance_score - a.importance_score)
    .slice(0, 5);

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card/60 p-4 text-sm">
      <h3 className="font-semibold text-primary">AI 시장 기억 요약</h3>

      {query && (
        <p className="text-xs text-muted-foreground">
          분석 쿼리:{" "}
          <span className="font-medium text-foreground">{query}</span>
        </p>
      )}

      {/* 핵심 기억 */}
      <div className="space-y-2">
        <p className="text-xs font-medium text-muted-foreground">현재 AI 핵심 기억</p>
        {topNodes.length === 0 ? (
          <p className="text-xs text-muted-foreground">기억 없음</p>
        ) : (
          <ul className="space-y-1">
            {topNodes.map((n) => (
              <li key={n.id} className="flex items-start gap-2 text-xs">
                <span className="mt-0.5 text-primary">·</span>
                <span className="line-clamp-1">{n.summary || n.query}</span>
                <span className="ml-auto shrink-0 font-mono text-muted-foreground">
                  {n.importance_score.toFixed(2)}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* 통계 */}
      <div className="grid grid-cols-3 gap-2 border-t border-border pt-3">
        <div className="text-center">
          <p className="text-lg font-bold text-blue-400">
            {nodes.filter((n) => n.layer === "short_term").length}
          </p>
          <p className="text-xs text-muted-foreground">단기 기억</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-yellow-400">
            {nodes.filter((n) => n.layer === "mid_term").length}
          </p>
          <p className="text-xs text-muted-foreground">중기 기억</p>
        </div>
        <div className="text-center">
          <p className="text-lg font-bold text-purple-400">{longTerm.length}</p>
          <p className="text-xs text-muted-foreground">장기 기억</p>
        </div>
      </div>

      {/* 승격 이슈 */}
      {promoted.length > 0 && (
        <div className="rounded-md bg-green-500/10 px-3 py-2">
          <p className="mb-1 text-xs font-medium text-green-400">
            AI가 장기 이슈로 판단 ({promoted.length}건)
          </p>
          {promoted.slice(0, 3).map((n) => (
            <p key={n.id} className="line-clamp-1 text-xs text-muted-foreground">
              · {n.summary || n.query}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
