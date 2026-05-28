"use client";

import { SidebarMenu } from "@/components/navigation/SidebarMenu";
import { RuntimeQuickActions } from "@/components/navigation/RuntimeQuickActions";
import { useRuntimeShell } from "./RuntimeShellProvider";

export function RuntimeSidebar() {
  const { sidebarCollapsed } = useRuntimeShell();
  return (
    <aside
      className={
        sidebarCollapsed
          ? "runtime-shell-sidebar hidden md:block md:w-14"
          : "runtime-shell-sidebar w-56"
      }
    >
      <div className="space-y-3">
        <RuntimeQuickActions />
        {!sidebarCollapsed && <SidebarMenu />}
      </div>
    </aside>
  );
}
