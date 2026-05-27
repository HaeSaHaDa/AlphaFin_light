import type { MemoryNodeData } from "@/types/memory-timeline";

interface MemoryNodeProps {
  node: MemoryNodeData;
  isSelected: boolean;
  onClick: (node: MemoryNodeData) => void;
}

const LAYER_STYLE = {
  short_term: "border-blue-400 bg-blue-500/20 hover:bg-blue-500/30",
  mid_term: "border-yellow-400 bg-yellow-500/20 hover:bg-yellow-500/30",
  long_term: "border-purple-400 bg-purple-500/20 hover:bg-purple-500/30",
};

const STATUS_DOT = {
  active: "bg-cyan-400",
  promoted: "bg-green-400",
  decayed: "bg-red-400",
  archived: "bg-gray-400",
};

const STATUS_LABEL = {
  active: "활성",
  promoted: "승격됨",
  decayed: "소멸됨",
  archived: "보관됨",
};

export function MemoryNode({ node, isSelected, onClick }: MemoryNodeProps) {
  const score = node.importance_score ?? 0;
  const scoreColor =
    score >= 0.8 ? "text-green-400" : score >= 0.5 ? "text-yellow-400" : "text-red-400";

  return (
    <button
      onClick={() => onClick(node)}
      className={`relative w-full cursor-pointer rounded-lg border px-3 py-2 text-left transition-all ${LAYER_STYLE[node.layer]} ${
        isSelected ? "ring-2 ring-primary" : ""
      }`}
    >
      {/* 상단: 중요도 배지 + 상태 */}
      <div className="mb-1 flex items-center justify-between gap-2">
        <span className={`text-xs font-bold ${scoreColor}`}>
          중요도 {score.toFixed(2)}
        </span>
        <span className="flex items-center gap-1 text-xs text-muted-foreground">
          <span className={`inline-block h-1.5 w-1.5 rounded-full ${STATUS_DOT[node.status]}`} />
          {STATUS_LABEL[node.status]}
        </span>
      </div>

      {/* 기억 내용 */}
      <p className="line-clamp-2 text-sm font-medium leading-snug">
        {node.summary || node.query}
      </p>

      {/* 하단: 시간 / 승격 표시 */}
      <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-muted-foreground">
        {node.timestamp && <span>{node.timestamp.slice(0, 10)}</span>}
        {node.status === "promoted" && node.promoted_from && (
          <span className="rounded bg-green-500/20 px-1.5 py-0.5 text-green-400">
            ↑ 승격
          </span>
        )}
        {node.status === "decayed" && (
          <span className="rounded bg-red-500/20 px-1.5 py-0.5 text-red-400">
            ↓ 소멸
          </span>
        )}
        {node.retention_action === "keep" && node.status === "active" && (
          <span className="rounded bg-cyan-500/20 px-1.5 py-0.5 text-cyan-400">
            유지 중
          </span>
        )}
      </div>
    </button>
  );
}
