import Link from "next/link";
import { Button } from "@/components/ui/button";
import { StockChainViewer } from "@/components/stock-chain/stock-chain-viewer";
import type { LoadStatus, StockChainData } from "@/types/dashboard";
import { DashboardSection } from "./DashboardSection";

interface MarketImpactPanelProps {
  data: StockChainData | null;
  status: LoadStatus;
  traceId?: string | null;
}

export function MarketImpactPanel({
  data,
  status,
  traceId,
}: MarketImpactPanelProps) {
  const href = traceId
    ? `/event-graph?trace_id=${encodeURIComponent(traceId)}`
    : "/event-graph";

  return (
    <DashboardSection
      title="시장 연결 구조"
      description="기업·산업·이벤트 간 영향 흐름 — NVIDIA → HBM → 삼성전자 등"
    >
      <div className="mb-4 flex flex-wrap justify-end gap-2">
        <Button variant="outline" size="sm" asChild>
          <Link href={href}>전체 그래프 보기</Link>
        </Button>
      </div>
      <StockChainViewer data={data} status={status} />
    </DashboardSection>
  );
}
