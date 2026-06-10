import type { MemoryNodeData } from "@/types/memory-timeline";

interface MemoryDetailPanelProps {
  node: MemoryNodeData | null;
}

const LAYER_KR = {
  short_term: "단기 기억",
  mid_term: "중기 기억",
  long_term: "장기 기억",
};

const STATUS_KR = {
  active: "활성",
  promoted: "승격됨",
  decayed: "소멸됨",
  archived: "보관됨",
};

export function MemoryDetailPanel({ node }: MemoryDetailPanelProps) {
  if (!node) {
    return (
      <div className="flex h-full items-center justify-center rounded-lg border border-dashed border-border p-6 text-center text-sm text-muted-foreground">
        기억 노드를 클릭하면
        <br />
        상세 정보가 표시됩니다.
      </div>
    );
  }

  const score = node.importance_score ?? 0;
  const barWidth = Math.round(score * 100);
  const barColor =
    score >= 0.8 ? "bg-green-500" : score >= 0.5 ? "bg-yellow-500" : "bg-red-500";
  const disclosures = (node.evidence ?? []).filter(
    (item) => item.document_type === "disclosure",
  );

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card/60 p-4 text-sm">
      <h3 className="font-semibold text-primary">기억 상세</h3>

      <div className="space-y-1">
        <p className="text-xs text-muted-foreground">기억 내용</p>
        <p className="font-medium">{node.summary || node.query}</p>
      </div>

      {disclosures.length > 0 && (
        <div className="space-y-2 border-t border-border pt-3">
          <p className="text-xs font-medium text-muted-foreground">
            저장된 공시 근거 ({disclosures.length})
          </p>
          {disclosures.map((item, index) => {
            const title =
              item.title ||
              item.report_name ||
              item.text?.split("\n")[0] ||
              item.chunk_text?.split("\n")[0] ||
              `공시 근거 ${index + 1}`;
            const content = item.text || item.chunk_text || "";
            const url = item.url || item.document_url;
            return (
              <details
                key={`${item.chunk_id ?? index}-${title}`}
                className="rounded-md border border-border/70 bg-muted/15 px-3 py-2"
              >
                <summary className="cursor-pointer text-xs font-medium">
                  {title}
                </summary>
                {(item.report_date || item.published_at) && (
                  <p className="mt-2 text-[11px] text-muted-foreground">
                    {item.report_date || item.published_at}
                  </p>
                )}
                {content && (
                  <p className="mt-2 whitespace-pre-wrap text-xs leading-relaxed text-foreground/90">
                    {content}
                  </p>
                )}
                {url && (
                  <a
                    href={url}
                    target="_blank"
                    rel="noreferrer"
                    className="mt-2 inline-block text-xs text-primary hover:underline"
                  >
                    공시 원문 열기
                  </a>
                )}
              </details>
            );
          })}
        </div>
      )}

      <div className="grid grid-cols-2 gap-3">
        <div className="space-y-1">
          <p className="text-xs text-muted-foreground">기억 유형</p>
          <p className="font-medium">{LAYER_KR[node.layer]}</p>
        </div>
        <div className="space-y-1">
          <p className="text-xs text-muted-foreground">상태</p>
          <p className="font-medium">{STATUS_KR[node.status]}</p>
        </div>
        {node.persona && (
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">분석 관점</p>
            <p className="font-medium">{node.persona}</p>
          </div>
        )}
        {node.timestamp && (
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">기록 시각</p>
            <p className="font-mono text-xs">{node.timestamp.slice(0, 19)}</p>
          </div>
        )}
      </div>

      {/* 중요도 바 */}
      <div className="space-y-1">
        <div className="flex items-center justify-between text-xs">
          <span className="text-muted-foreground">중요도 (Importance)</span>
          <span className="font-bold">{score.toFixed(2)}</span>
        </div>
        <div className="h-2 w-full overflow-hidden rounded-full bg-muted">
          <div
            className={`h-full rounded-full transition-all ${barColor}`}
            style={{ width: `${barWidth}%` }}
          />
        </div>
      </div>

      {node.status === "promoted" && (
        <div className="rounded-md bg-green-500/10 px-3 py-2 text-xs text-green-400">
          AI가 이 이슈를 장기 이슈로 판단하여 승격했습니다.
        </div>
      )}
      {node.status === "decayed" && (
        <div className="rounded-md bg-red-500/10 px-3 py-2 text-xs text-red-400">
          시장 영향이 감소하여 기억이 소멸되었습니다.
        </div>
      )}
    </div>
  );
}
