"use client";

import type { RiskExposurePayload } from "@/types/market-graph";

export function RiskExposurePanel({ data }: { data: RiskExposurePayload | null }) {
  if (!data?.risks?.length) {
    return <p className="text-xs text-muted-foreground">리스크 노출 정보 없음</p>;
  }
  return (
    <div className="space-y-1.5">
      {data.risks.slice(0, 4).map((r) => (
        <div key={`${r.risk}-${r.confidence}`} className="rounded border border-border/70 p-2 text-xs">
          <p className="font-medium">{r.risk}</p>
          <p className="text-muted-foreground">
            {r.exposure_level} · {r.impact} · conf {Math.round(r.confidence * 100)}%
          </p>
        </div>
      ))}
    </div>
  );
}
