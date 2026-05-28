"use client";

interface Props {
  companyName: string;
  ticker: string;
  traceId?: string | null;
}

export function SelectedTickerInfo({ companyName, ticker, traceId }: Props) {
  if (!ticker && !companyName) {
    return (
      <span className="text-sm text-muted-foreground">종목 미선택</span>
    );
  }
  return (
    <div className="min-w-0">
      <p className="truncate text-sm font-semibold text-foreground">
        {companyName || "—"}
        {ticker && (
          <span className="ml-2 font-mono text-primary">({ticker})</span>
        )}
      </p>
      {traceId && (
        <p className="truncate font-mono text-[10px] text-muted-foreground">
          trace: {traceId}
        </p>
      )}
    </div>
  );
}
