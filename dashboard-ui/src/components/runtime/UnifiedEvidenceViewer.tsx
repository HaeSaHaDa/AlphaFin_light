"use client";

import type { RuntimeEvidenceItem } from "@/types/runtime-evidence";

interface Props {
  items: RuntimeEvidenceItem[];
  maxItems?: number;
}

function labelFor(item: RuntimeEvidenceItem): string {
  return (
    item.title ||
    item.report_name ||
    item.section_name ||
    item.text?.split("\n")[0] ||
    "제목 없는 근거 문서"
  );
}

export function UnifiedEvidenceViewer({ items, maxItems = 8 }: Props) {
  const list = items.slice(0, maxItems);
  if (list.length === 0) {
    return (
      <p className="text-sm text-muted-foreground">통합 근거가 없습니다.</p>
    );
  }

  return (
    <ul className="space-y-2">
      {list.map((item, i) => {
        const isDisc = item.document_type === "disclosure";
        return (
          <li
            key={`${item.chunk_id}-${i}`}
            className="rounded-lg border border-border/60 bg-muted/15 px-3 py-2 text-xs"
          >
            <div className="flex flex-wrap items-center gap-2">
              <span
                className={
                  isDisc
                    ? "rounded bg-emerald-500/15 px-1.5 py-0.5 text-[10px] text-emerald-400"
                    : "rounded bg-primary/10 px-1.5 py-0.5 text-[10px] text-primary"
                }
              >
                {isDisc ? "공시" : "뉴스"}
              </span>
              {item.source_priority && (
                <span className="text-muted-foreground">{item.source_priority}</span>
              )}
              {(item.merge_score ?? item.score) != null && (
                <span className="text-muted-foreground">
                  {Math.round((item.merge_score ?? item.score ?? 0) * 100)}%
                </span>
              )}
            </div>
            {item.url ? (
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="mt-1 block font-medium leading-snug hover:text-primary hover:underline"
              >
                {labelFor(item)}
              </a>
            ) : (
              <p className="mt-1 font-medium leading-snug">{labelFor(item)}</p>
            )}
            {(item.source || item.published_at) && (
              <p className="mt-1 text-[11px] text-muted-foreground">
                {[item.source, item.published_at].filter(Boolean).join(" · ")}
              </p>
            )}
          </li>
        );
      })}
    </ul>
  );
}
