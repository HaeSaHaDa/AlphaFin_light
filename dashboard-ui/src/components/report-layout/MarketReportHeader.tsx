interface MarketReportHeaderProps {
  query?: string;
  traceId?: string | null;
}

export function MarketReportHeader({ query, traceId }: MarketReportHeaderProps) {
  return (
    <header className="rounded-xl border border-primary/20 bg-gradient-to-br from-primary/10 to-card/60 p-6 md:p-8">
      <p className="text-xs font-medium uppercase tracking-widest text-primary">
        AlphaFin LTE
      </p>
      <h1 className="mt-2 text-2xl font-bold tracking-tight md:text-3xl">
        AI 시장 분석 리포트
      </h1>
      <p className="mt-2 max-w-2xl text-sm text-muted-foreground md:text-base">
        AI가 참고한 자료와 시장 연결 구조를 바탕으로 정리한 분석 요약입니다.
        아래에서 현재 관점, 상승 요인, 리스크를 확인할 수 있습니다.
      </p>
      {query && (
        <p className="mt-4 text-sm font-medium">
          분석 질문: <span className="text-foreground">{query}</span>
        </p>
      )}
      {traceId && (
        <p className="mt-1 font-mono text-xs text-muted-foreground">
          trace: {traceId}
        </p>
      )}
    </header>
  );
}
