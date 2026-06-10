"use client";

import { useRuntimeTicker } from "@/hooks/use-runtime-ticker";

export function GlobalTickerSelector() {
  const { ticker, companyName } = useRuntimeTicker();

  return (
    <div className="min-w-[180px]">
      <p className="text-[11px] text-muted-foreground">현재 종목</p>
      <p className="truncate text-sm font-semibold">
        {companyName || "종목 미선택"}
        {ticker ? (
          <span className="ml-2 font-mono text-primary">({ticker})</span>
        ) : null}
      </p>
    </div>
  );
}
