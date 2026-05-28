"use client";

import Link from "next/link";
import { usePathname, useSearchParams } from "next/navigation";
import { SidebarSection } from "./SidebarSection";
import { traceQueryHref } from "@/runtime-state/runtime-trace-store";

const MENU = [
  { key: "dashboard", label: "Dashboard", href: "/" },
  { key: "news", label: "News", href: "/analysis" },
  { key: "graph", label: "Graph", href: "/event-graph" },
  { key: "memory", label: "Memory", href: "/memory-timeline" },
  { key: "evaluation", label: "Evaluation", href: "/signal-evaluation" },
  { key: "disclosure", label: "Disclosure", href: "/analysis" },
  { key: "retrieval", label: "Retrieval", href: "/analysis" },
  { key: "settings", label: "Settings", href: "/analysis" },
];

export function SidebarMenu() {
  const pathname = usePathname();
  const params = useSearchParams();
  const traceId = params.get("trace_id");

  return (
    <SidebarSection title="Runtime Menu">
      {MENU.map((item) => {
        const active = pathname === item.href;
        return (
          <Link
            key={item.key}
            href={traceQueryHref(item.href, traceId)}
            className={
              active
                ? "block rounded-md border border-primary/50 bg-primary/10 px-2 py-1.5 text-xs text-primary transition-colors"
                : "block rounded-md border border-transparent px-2 py-1.5 text-xs text-muted-foreground transition-colors hover:border-border hover:bg-muted/40 hover:text-foreground"
            }
          >
            {item.label}
          </Link>
        );
      })}
    </SidebarSection>
  );
}
