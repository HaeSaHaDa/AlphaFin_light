"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { GLOBAL_NAVIGATION_MAP } from "@/navigation/global-navigation-map";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";
import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";
import { scrollToSection } from "@/components/runtime-header/RuntimeSectionNav";

function buildHref(path: string, traceId: string | null): string {
  return traceQueryHref(path, traceId);
}

function resolveActiveKey(pathname: string): string {
  if (pathname === "/") return "dashboard";
  if (pathname === "/analysis") return "retrieval";
  if (pathname === "/event-graph") return "graph";
  if (pathname === "/memory-timeline") return "memory";
  if (pathname === "/signal-evaluation") return "evaluation";
  return "";
}

export function GlobalNavigation({
  traceId,
  compact = false,
  onNavigate,
}: {
  traceId: string | null;
  compact?: boolean;
  onNavigate?: () => void;
}) {
  const pathname = usePathname();
  const { setCurrentSection } = useRuntimeShell();
  const activeKey = resolveActiveKey(pathname);
  return (
    <nav className="space-y-1" aria-label="Global navigation">
      {GLOBAL_NAVIGATION_MAP.map((item) => {
        const isDashboard = item.key === "dashboard";
        const active = item.key === activeKey;
        return (
          <Link
            key={item.key}
            href={buildHref(item.href, traceId)}
            onClick={(e) => {
              if (isDashboard) {
                setCurrentSection("summary");
                if (pathname === "/") {
                  e.preventDefault();
                  scrollToSection("section-summary");
                }
              }
              onNavigate?.();
            }}
            className={cn(
              active ? "dash-sidebar-link-active" : "dash-sidebar-link",
              compact && "px-1.5 py-1 text-[10px]",
            )}
          >
            {compact ? item.shortLabel : item.label}
          </Link>
        );
      })}
    </nav>
  );
}
