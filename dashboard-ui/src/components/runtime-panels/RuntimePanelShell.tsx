"use client";

import { Skeleton } from "@/components/ui/skeleton";
import type { LoadStatus } from "@/types/dashboard";

interface RuntimePanelShellProps {
  traceId: string | null;
  status: LoadStatus;
  title: string;
  emptyMessage?: string;
  children: React.ReactNode;
}

export function RuntimePanelShell({
  traceId,
  status,
  title,
  emptyMessage = "데이터를 불러오지 못했습니다.",
  children,
}: RuntimePanelShellProps) {
  if (!traceId) {
    return (
      <div className="rounded-xl border border-dashed border-border p-5 text-sm text-muted-foreground">
        {title}: trace_id가 없습니다. 종목을 선택하고 분석을 실행하세요.
      </div>
    );
  }

  if (status === "loading") {
    return <Skeleton className="h-40 w-full rounded-xl" />;
  }

  if (status === "error") {
    return (
      <div className="rounded-xl border border-destructive/40 bg-destructive/10 p-5 text-sm">
        {emptyMessage}
      </div>
    );
  }

  return <>{children}</>;
}
