"use client";

import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";

export function GlobalRuntimeSearch() {
  const { searchQuery, setSearchQuery } = useRuntimeShell();
  return (
    <label className="min-w-[220px]">
      <span className="sr-only">Runtime Search</span>
      <input
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Runtime 검색 (ticker, keyword, trace)"
        className="h-8 w-full rounded-md border border-border bg-card px-2 text-xs outline-none ring-0 placeholder:text-muted-foreground"
      />
    </label>
  );
}
