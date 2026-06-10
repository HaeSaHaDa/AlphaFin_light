"use client";

interface Props {
  companyName: string;
  ticker: string;
  traceId?: string | null;
}

export function SelectedTickerInfo({ companyName, ticker, traceId }: Props) {
  if (!ticker && !companyName) {
    return (
      <span className="text-sm text-muted-foreground">종목을 선택하세요</span>
    );
  }
  return (
    <div className="min-w-0">
      <p className="dash-ticker-anchor truncate">
        {companyName || "—"}
        {ticker && <span className="dash-ticker-code">{ticker}</span>}
      </p>
      {traceId && (
        <p className="dash-trace-hint mt-0.5 truncate" title={traceId}>
          session ···{traceId.slice(-10)}
        </p>
      )}
    </div>
  );
}
