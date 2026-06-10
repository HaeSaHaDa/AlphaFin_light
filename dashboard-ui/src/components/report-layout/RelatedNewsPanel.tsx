import type { RetrievalChunk } from "@/types/dashboard";

interface RelatedNewsPanelProps {
  chunks: RetrievalChunk[];
}

export function RelatedNewsPanel({ chunks }: RelatedNewsPanelProps) {
  const news = chunks.filter((chunk) => chunk.document_type === "news_article");

  return (
    <div className="rounded-xl border border-border bg-card/60 p-5">
      <h3 className="text-sm font-semibold">관련 뉴스</h3>
      <p className="mt-1 text-xs text-muted-foreground">
        분석에 실제로 사용된 뉴스 기사입니다.
      </p>
      {news.length === 0 && (
        <p className="mt-3 text-sm text-muted-foreground">
          이 분석에서 참조한 뉴스 기사가 없습니다.
        </p>
      )}
      <ul className="mt-4 grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        {news.slice(0, 6).map((article, index) => (
          <li
            key={`${article.chunk_id ?? index}-${article.url ?? article.title ?? index}`}
            className="rounded-lg border border-border/60 bg-muted/20 px-4 py-3"
          >
            {article.url ? (
              <a
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="text-sm font-medium leading-snug hover:text-primary hover:underline"
              >
                {article.title || "제목 없는 뉴스"}
              </a>
            ) : (
              <p className="text-sm font-medium leading-snug">
                {article.title || "제목 없는 뉴스"}
              </p>
            )}
            <div className="mt-2 flex flex-wrap gap-x-2 text-xs text-muted-foreground">
              {article.source && <span>{article.source}</span>}
              {article.published_at && <span>{article.published_at}</span>}
            </div>
            {article.text && (
              <p className="mt-2 line-clamp-3 text-xs leading-relaxed text-muted-foreground">
                {article.text}
              </p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
