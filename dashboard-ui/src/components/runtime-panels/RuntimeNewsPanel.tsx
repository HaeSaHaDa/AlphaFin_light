"use client";

import { RelatedNewsPanel } from "@/components/report-layout/RelatedNewsPanel";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { LoadStatus, RetrievalData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  retrieval: RetrievalData | null;
}

export function RuntimeNewsPanel({ traceId, status, retrieval }: Props) {
  const news = (retrieval?.chunks ?? []).filter(
    (chunk) => chunk.document_type === "news_article",
  );

  return (
    <RuntimePanelShell
      traceId={traceId}
      status={status}
      title="News"
      emptyMessage="분석에 사용된 뉴스가 없습니다."
    >
      {retrieval?.freshness && (
        <div className="mb-4 grid gap-2 text-xs sm:grid-cols-2">
          {(["news", "disclosure"] as const).map((source) => {
            const meta = retrieval.freshness?.[source];
            return (
              <div
                key={source}
                className="rounded-lg border border-border/60 bg-muted/20 px-3 py-2"
              >
                <div className="font-medium">
                  {source === "news" ? "News" : "Disclosure"} Updated
                </div>
                <div className="mt-1 text-muted-foreground">
                  기준 {meta?.data_as_of || "확인 불가"}
                </div>
                <div className="text-muted-foreground">
                  수집 {meta?.last_collected_at || "확인 불가"} · Cache{" "}
                  {meta?.cache_status || "UNKNOWN"}
                </div>
              </div>
            );
          })}
        </div>
      )}
      {news.length === 0 ? (
        <div className="rounded-xl border border-border bg-card/60 p-5 text-sm text-muted-foreground">
          현재 분석에서 참조한 뉴스 기사가 없습니다.
        </div>
      ) : (
        <RelatedNewsPanel chunks={news} />
      )}
    </RuntimePanelShell>
  );
}
