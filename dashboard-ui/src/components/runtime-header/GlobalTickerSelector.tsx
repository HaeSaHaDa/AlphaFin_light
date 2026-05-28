"use client";

import { useEffect, useState } from "react";
import { loadRuntimeSession } from "@/runtime-state/runtime-session";
import type { RuntimeSession } from "@/runtime-state/runtime-session";

export function GlobalTickerSelector() {
  const [session, setSession] = useState<RuntimeSession | null>(null);

  useEffect(() => {
    setSession(loadRuntimeSession());
  }, []);

  return (
    <div className="min-w-[180px]">
      <p className="text-[11px] text-muted-foreground">현재 종목</p>
      <p className="truncate text-sm font-semibold">
        {session?.companyName || "종목 미선택"}
        {session?.ticker ? (
          <span className="ml-2 font-mono text-primary">({session.ticker})</span>
        ) : null}
      </p>
    </div>
  );
}
