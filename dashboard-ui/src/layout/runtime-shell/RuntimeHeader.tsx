"use client";

import { RuntimeBreadcrumb } from "@/components/navigation/RuntimeBreadcrumb";
import { RuntimePageTabs } from "@/components/navigation/RuntimePageTabs";
import { GlobalTickerSelector } from "@/components/runtime-header/GlobalTickerSelector";
import { GlobalRuntimeSearch } from "@/components/runtime-header/GlobalRuntimeSearch";
import { GlobalTraceStatus } from "@/components/runtime-header/GlobalTraceStatus";
import { GlobalSectionNav } from "@/components/runtime-header/GlobalSectionNav";
import { GlobalRuntimeActions } from "@/components/runtime-header/GlobalRuntimeActions";

export function RuntimeHeader() {
  return (
    <header className="runtime-shell-header">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <RuntimeBreadcrumb />
        <GlobalTraceStatus />
      </div>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        <GlobalTickerSelector />
        <GlobalRuntimeSearch />
        <GlobalRuntimeActions />
      </div>
      <div className="mt-2 flex flex-wrap items-center justify-between gap-2">
        <RuntimePageTabs />
        <GlobalSectionNav />
      </div>
    </header>
  );
}
