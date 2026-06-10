"use client";

import { useEffect, useState } from "react";
import { Skeleton } from "@/components/ui/skeleton";
import { DashboardSectionCard } from "@/components/ui-cleanup/DashboardSectionCard";
import { getRuntimeEvidence } from "@/services/api";
import type { RuntimeEvidencePayload } from "@/types/runtime-evidence";
import { DisclosureRuntimeBadge } from "./DisclosureRuntimeBadge";
import { RuntimeSourceBreakdown } from "./RuntimeSourceBreakdown";
import { UnifiedEvidenceViewer } from "./UnifiedEvidenceViewer";

interface Props {
  traceId: string | null;
  ticker?: string | null;
}

export function RuntimeEvidencePanel({ traceId, ticker }: Props) {
  const [data, setData] = useState<RuntimeEvidencePayload | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "ok" | "error">("idle");

  useEffect(() => {
    const id = traceId?.trim();
    if (!id) {
      setData(null);
      setStatus("idle");
      return;
    }
    setStatus("loading");
    getRuntimeEvidence(id)
      .then((payload) => {
        setData(payload);
        setStatus("ok");
      })
      .catch(() => setStatus("error"));
  }, [traceId, ticker]);

  return (
    <DashboardSectionCard
      id="section-runtime-evidence"
      title="분석 근거"
      subtitle="뉴스 + 공시 통합 retrieval · 공식 문서 우선"
      accent="evidence"
      badge={
        data ? (
          <DisclosureRuntimeBadge
            hasDisclosure={data.has_disclosure}
            disclosureCount={data.source_breakdown?.DISCLOSURE}
          />
        ) : undefined
      }
    >
      {status === "loading" && <Skeleton className="h-28 w-full rounded-xl" />}
      {status === "idle" && (
        <p className="text-sm text-muted-foreground">
          분석 실행 후 통합 근거가 표시됩니다.
        </p>
      )}
      {status === "error" && (
        <p className="text-sm text-muted-foreground">
          Runtime evidence를 불러올 수 없습니다.
        </p>
      )}
      {status === "ok" && data && (
        <>
          <RuntimeSourceBreakdown breakdown={data.source_breakdown} />
          {data.reasoning_context.length > 0 && (
            <div className="mt-3 rounded-lg border border-border/50 bg-muted/10 p-3">
              <p className="text-[11px] font-medium text-muted-foreground">
                Reasoning 요약
              </p>
              <ul className="mt-2 list-inside list-disc text-xs leading-relaxed">
                {data.reasoning_context.slice(0, 6).map((line, i) => (
                  <li key={i}>{line}</li>
                ))}
              </ul>
            </div>
          )}
          <div className="mt-4">
            <UnifiedEvidenceViewer items={data.merged_evidence} />
          </div>
        </>
      )}
    </DashboardSectionCard>
  );
}
