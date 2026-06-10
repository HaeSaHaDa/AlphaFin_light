"use client";

import { useEffect, useMemo, useState } from "react";
import {
  collectDisclosure,
  getDisclosureByTicker,
  getDisclosureEvidence,
  getDisclosureTimeline,
} from "@/services/api";
import type {
  DisclosureData,
  DisclosureEvidenceData,
  DisclosureTimelineData,
} from "@/types/dashboard";
import { DisclosureSummaryCard } from "./DisclosureSummaryCard";
import { DisclosureFilterBar } from "./DisclosureFilterBar";
import { DisclosureViewer } from "./DisclosureViewer";
import { DisclosureTimeline } from "./DisclosureTimeline";
import { DisclosureEvidencePanel } from "./DisclosureEvidencePanel";
import { DashboardSectionCard } from "@/components/ui-cleanup/DashboardSectionCard";
import { InformationPriorityBadge } from "@/components/ui-cleanup/InformationPriorityBadge";

interface Props {
  ticker: string | null;
  traceId: string | null;
}

export function DisclosurePanel({ ticker, traceId }: Props) {
  const [data, setData] = useState<DisclosureData | null>(null);
  const [timeline, setTimeline] = useState<DisclosureTimelineData | null>(null);
  const [evidence, setEvidence] = useState<DisclosureEvidenceData | null>(null);
  const [filter, setFilter] = useState("");

  useEffect(() => {
    const t = (ticker || "").trim();
    if (!t) return;
    let cancelled = false;

    const refresh = async () => {
      const [nextData, nextTimeline] = await Promise.all([
        getDisclosureByTicker(t).catch(() => null),
        getDisclosureTimeline(t).catch(() => null),
      ]);
      if (!cancelled) {
        setData(nextData);
        setTimeline(nextTimeline);
      }
    };

    void (async () => {
      await refresh();
      await collectDisclosure(t, false, 365).catch(() => null);
      await refresh();
    })();

    return () => {
      cancelled = true;
    };
  }, [ticker]);

  useEffect(() => {
    const id = (traceId || "").trim();
    if (!id) return;
    getDisclosureEvidence(id).then(setEvidence).catch(() => setEvidence(null));
  }, [traceId]);

  if (!ticker) {
    return (
      <DashboardSectionCard
        id="section-disclosure"
        title="공시 (OpenDART)"
        subtitle="공식 문서 · 뉴스와 구분된 영역"
        accent="disclosure"
      >
        <p className="text-sm text-muted-foreground">
          종목을 선택하고 분석을 실행하면 공시가 수집·표시됩니다.
        </p>
      </DashboardSectionCard>
    );
  }

  return (
    <DashboardSectionCard
      id="section-disclosure"
      title="공시 (OpenDART)"
      subtitle="공식 문서 · 뉴스와 구분된 영역"
      accent="disclosure"
      badge={
        <InformationPriorityBadge label="DISCLOSURE" accent="disclosure" />
      }
    >
      <div className="space-y-3">
        <DisclosureSummaryCard data={data} />
        <DisclosureFilterBar value={filter} onChange={setFilter} />
        <div className="grid gap-3 lg:grid-cols-2">
          <DisclosureViewer data={data} filter={filter} />
          <DisclosureTimeline data={timeline} />
        </div>
        <DisclosureEvidencePanel data={evidence} />
      </div>
    </DashboardSectionCard>
  );
}
