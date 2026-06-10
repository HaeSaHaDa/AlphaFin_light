"use client";

import { RuntimeBreadcrumb } from "@/components/navigation-cleanup/RuntimeBreadcrumb";
import { GlobalTickerSelector } from "@/components/runtime-header/GlobalTickerSelector";
import { GlobalTraceStatus } from "@/components/runtime-header/GlobalTraceStatus";
import { GlobalRuntimeActions } from "@/components/runtime-header/GlobalRuntimeActions";
import { GlobalRuntimeSearch } from "@/components/runtime-header/GlobalRuntimeSearch";
import { PresentationModeToggle } from "@/components/layout/presentation-mode-toggle";

export function RuntimeHeader() {
  return (
    <header className="runtime-shell-header">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <RuntimeBreadcrumb />
        <div className="flex flex-wrap items-center gap-2">
          <PresentationModeToggle />
          <GlobalTraceStatus />
        </div>
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        <GlobalTickerSelector />
        <GlobalRuntimeSearch />
        <GlobalRuntimeActions />
      </div>
    </header>
  );
}
