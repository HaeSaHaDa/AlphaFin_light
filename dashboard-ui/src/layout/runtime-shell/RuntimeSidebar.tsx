"use client";

import { GlobalNavigation } from "@/components/navigation-cleanup/GlobalNavigation";
import { SidebarNavigation } from "@/components/navigation-cleanup/SidebarNavigation";
import { useRuntimeTicker } from "@/hooks/use-runtime-ticker";
import { useRuntimeShell } from "./RuntimeShellProvider";

export function RuntimeSidebar() {
  const { sidebarCollapsed } = useRuntimeShell();
  const { traceId } = useRuntimeTicker();
  return (
    <>
      <div className="px-2 py-2 md:hidden">
        <SidebarNavigation traceId={traceId} />
      </div>
      <aside
        className={
          sidebarCollapsed
            ? "runtime-shell-sidebar hidden md:block md:w-14"
            : "runtime-shell-sidebar hidden w-56 md:block"
        }
      >
        {!sidebarCollapsed && (
          <p className="mb-2 px-2 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
            Pages
          </p>
        )}
        <GlobalNavigation traceId={traceId} compact={sidebarCollapsed} />
      </aside>
    </>
  );
}
