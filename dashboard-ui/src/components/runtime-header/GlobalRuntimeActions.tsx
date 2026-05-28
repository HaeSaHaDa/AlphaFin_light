"use client";

import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";

export function GlobalRuntimeActions() {
  const { sidebarCollapsed, toggleSidebar } = useRuntimeShell();
  return (
    <button
      type="button"
      onClick={toggleSidebar}
      className="rounded-md border border-border px-2 py-1 text-[11px] text-muted-foreground hover:text-foreground"
    >
      {sidebarCollapsed ? "사이드바 열기" : "사이드바 접기"}
    </button>
  );
}
