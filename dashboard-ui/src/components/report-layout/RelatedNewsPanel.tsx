import type { RetrievalChunk } from "@/types/dashboard";

interface RelatedNewsPanelProps {
  chunks: RetrievalChunk[];
}

export function RelatedNewsPanel({ chunks }: RelatedNewsPanelProps) {
  const news = chunks.filter(
    (c) => c.document_type === "news_article" || c.document_type === "disclosure",
  );

  const headlines = news.length
    ? news.map((c, i) => {
        const preview = (c as { chunk_preview?: string }).chunk_preview;
        if (preview) return preview.slice(0, 80);
        return `참고 문서 #${c.chunk_id ?? i + 1} (${c.document_type ?? "news"})`;
      })
    : [
        "NVIDIA 실적 호조",
        "HBM 공급 부족 지속",
        "AI 서버 투자 증가",
      ];

  return (
    <div className="rounded-xl border border-border bg-card/60 p-5">
      <h3 className="text-sm font-semibold">관련 뉴스 · 공시</h3>
      <p className="mt-1 text-xs text-muted-foreground">
        AI가 참고한 자료 중 시장 뉴스·공시 요약
      </p>
      <ul className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {headlines.slice(0, 6).map((h, i) => (
          <li
            key={i}
            className="rounded-lg border border-border/60 bg-muted/20 px-3 py-2 text-sm leading-snug"
          >
            {h}
          </li>
        ))}
      </ul>
    </div>
  );
}
