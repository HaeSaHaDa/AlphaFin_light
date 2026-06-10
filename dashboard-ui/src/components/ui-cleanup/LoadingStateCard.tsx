"use client";

import { Skeleton } from "@/components/ui/skeleton";

interface Props {
  message?: string;
  steps?: string[];
}

const DEFAULT_STEPS = [
  "뉴스 Retrieval 수행 중",
  "공시 Retrieval 수행 중",
  "Event Consolidation 수행 중",
];

export function LoadingStateCard({
  message = "Runtime 분석 진행 중…",
  steps = DEFAULT_STEPS,
}: Props) {
  return (
    <div className="dash-loading-state space-y-4">
      <p className="text-sm font-medium text-primary">{message}</p>
      <ul className="space-y-1 text-xs text-muted-foreground">
        {steps.map((s) => (
          <li key={s} className="flex items-center gap-2">
            <span className="h-1 w-1 animate-pulse rounded-full bg-primary" />
            {s}
          </li>
        ))}
      </ul>
      <div className="dashboard-grid-3">
        <Skeleton className="h-36 rounded-xl" />
        <Skeleton className="h-36 rounded-xl" />
        <Skeleton className="h-36 rounded-xl" />
      </div>
    </div>
  );
}
