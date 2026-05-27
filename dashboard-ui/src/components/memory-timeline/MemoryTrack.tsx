import { MemoryNode } from "./MemoryNode";
import type { MemoryLayer, MemoryNodeData } from "@/types/memory-timeline";

interface MemoryTrackProps {
  layer: MemoryLayer;
  nodes: MemoryNodeData[];
  selectedId: string | null;
  onSelect: (node: MemoryNodeData) => void;
}

const TRACK_CONFIG: Record<MemoryLayer, { label: string; desc: string; headerClass: string }> = {
  short_term: {
    label: "단기 기억",
    desc: "최근 시장 이벤트 · 단기 분석 결과",
    headerClass: "border-blue-400/50 bg-blue-500/10 text-blue-300",
  },
  mid_term: {
    label: "중기 기억",
    desc: "중요도 높은 이슈 · 지속 모니터링 대상",
    headerClass: "border-yellow-400/50 bg-yellow-500/10 text-yellow-300",
  },
  long_term: {
    label: "장기 기억",
    desc: "AI가 장기 이슈로 판단 · 구조적 시장 변화",
    headerClass: "border-purple-400/50 bg-purple-500/10 text-purple-300",
  },
};

export function MemoryTrack({ layer, nodes, selectedId, onSelect }: MemoryTrackProps) {
  const cfg = TRACK_CONFIG[layer];

  return (
    <div className="flex flex-col gap-2">
      {/* 트랙 헤더 */}
      <div className={`rounded-md border px-3 py-2 ${cfg.headerClass}`}>
        <span className="font-semibold">{cfg.label}</span>
        <span className="ml-2 text-xs opacity-70">{cfg.desc}</span>
        <span className="float-right text-xs opacity-60">{nodes.length}건</span>
      </div>

      {/* 기억 노드 목록 */}
      {nodes.length === 0 ? (
        <p className="py-3 text-center text-xs text-muted-foreground">기억 없음</p>
      ) : (
        <div className="space-y-2">
          {nodes.map((node, idx) => (
            <div key={node.id} className="flex items-stretch gap-2">
              {/* 타임라인 연결선 */}
              <div className="flex w-4 flex-col items-center">
                <div className="h-3 w-px bg-border" />
                <div className="h-2 w-2 rounded-full border border-border bg-card" />
                {idx < nodes.length - 1 && <div className="flex-1 w-px bg-border" />}
              </div>
              <div className="flex-1 pb-2">
                <MemoryNode
                  node={node}
                  isSelected={selectedId === node.id}
                  onClick={onSelect}
                />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
