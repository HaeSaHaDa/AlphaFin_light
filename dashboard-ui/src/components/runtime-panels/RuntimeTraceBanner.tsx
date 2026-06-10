"use client";

import Link from "next/link";
import { useActiveTrace } from "@/hooks/use-active-trace";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";

export function RuntimeTraceBanner() {
  const { traceId, ticker, companyName, runtimeQuery } = useActiveTrace();

  if (!traceId) {
    return (
      <div className="rounded-lg border border-dashed border-amber-500/40 bg-amber-500/10 px-4 py-3 text-sm">
        <p className="font-medium text-amber-100">검색·분석이 연결되지 않았습니다</p>
        <p className="mt-1 text-xs text-amber-100/80">
          <Link href="/" className="underline">
            Dashboard
          </Link>
          에서 종목을 선택하고 <strong>분석 실행</strong>한 뒤 이 페이지를 이용하세요.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-primary/30 bg-primary/5 px-4 py-2 text-xs">
      <span className="font-medium text-foreground">
        {companyName || "종목"} {ticker && `(${ticker})`}
      </span>
      {runtimeQuery && (
        <span className="ml-2 text-muted-foreground">· {runtimeQuery}</span>
      )}
      <span className="ml-2 font-mono text-muted-foreground">trace: {traceId}</span>
      <Link
        href={traceQueryHref("/", traceId)}
        className="ml-3 text-primary underline"
      >
        Dashboard
      </Link>
    </div>
  );
}
