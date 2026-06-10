"use client";

import { useEffect, useState } from "react";
import { Menu } from "lucide-react";
import { GlobalNavigation } from "./GlobalNavigation";
import { NavigationDivider } from "./NavigationDivider";
import { NavigationGroup } from "./NavigationGroup";

export function SidebarNavigation({ traceId }: { traceId: string | null }) {
  const [openMobile, setOpenMobile] = useState(false);

  useEffect(() => {
    if (!openMobile) return;
    const onEsc = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpenMobile(false);
    };
    window.addEventListener("keydown", onEsc);
    return () => window.removeEventListener("keydown", onEsc);
  }, [openMobile]);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpenMobile(true)}
        className="rounded-md border border-border px-2 py-1 text-[11px] text-muted-foreground md:hidden"
      >
        <span className="inline-flex items-center gap-1">
          <Menu className="h-3.5 w-3.5" />
          메뉴
        </span>
      </button>

      <div className="hidden md:block">
        <NavigationGroup title="Pages">
          <GlobalNavigation traceId={traceId} />
        </NavigationGroup>
      </div>

      {openMobile && (
        <div className="fixed inset-0 z-[300] md:hidden">
          <button
            type="button"
            className="absolute inset-0 bg-black/50"
            onClick={() => setOpenMobile(false)}
            aria-label="메뉴 닫기"
          />
          <aside className="absolute left-0 top-0 h-full w-64 border-r border-border bg-background p-3">
            <div className="mb-2 flex items-center justify-between">
              <p className="text-xs font-medium text-muted-foreground">Navigation</p>
              <button
                type="button"
                onClick={() => setOpenMobile(false)}
                className="rounded border border-border px-2 py-0.5 text-xs"
              >
                닫기
              </button>
            </div>
            <NavigationDivider />
            <NavigationGroup title="Pages">
              <GlobalNavigation
                traceId={traceId}
                onNavigate={() => setOpenMobile(false)}
              />
            </NavigationGroup>
          </aside>
        </div>
      )}
    </>
  );
}
