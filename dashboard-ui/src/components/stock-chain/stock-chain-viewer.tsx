"use client";

import { PanelShell } from "@/components/layout/panel-shell";
import { Badge } from "@/components/ui/badge";
import type { LoadStatus, StockChainData, StockChainLink } from "@/types/dashboard";

interface StockChainViewerProps {
  data: StockChainData | null;
  status: LoadStatus;
}

export function StockChainViewer({ data, status }: StockChainViewerProps) {
  const links = pickDisplayLinks(data);

  return (
    <PanelShell
      title="Stock Chain"
      subtitle="Propagation graph"
      status={status}
      empty={!data}
      className="min-h-[280px]"
    >
      {data && (
        <div className="space-y-3">
          <div className="flex flex-wrap gap-2 text-xs">
            {(data.center_name || data.center_ticker) && (
              <Badge variant="default" className="font-medium">
                중심: {data.center_name || "—"}
                {data.center_ticker ? ` / ${data.center_ticker}` : ""}
              </Badge>
            )}
            <Badge variant="secondary">
              entities:{" "}
              {(data.summary?.entity_count as number) ??
                data.chain?.entities?.length ??
                0}
            </Badge>
            <Badge variant="outline">
              links:{" "}
              {(data.summary?.link_count as number) ??
                data.chain?.links?.length ??
                0}
            </Badge>
          </div>
          <ChainGraph links={links} />
        </div>
      )}
    </PanelShell>
  );
}

function ChainGraph({ links }: { links: StockChainLink[] }) {
  if (!links.length) {
    return (
      <p className="text-center text-xs text-muted-foreground">
        이 trace에 대한 Stock Chain 연결이 없습니다. 분석 실행 후 다시 확인하세요.
      </p>
    );
  }
  return (
    <div className="flex flex-col items-center gap-1 py-2">
      {links.map((link, i) => (
        <div
          key={`${link.source}-${link.target}-${i}`}
          className="flex w-full flex-col items-center"
        >
          <div
            className={
              i === 0
                ? "max-w-[220px] rounded-lg border border-primary/40 bg-primary/10 px-4 py-2 text-center text-sm font-medium"
                : "max-w-[220px] rounded-lg border border-border bg-muted/40 px-4 py-2 text-center text-sm"
            }
          >
            {link.source}
          </div>
          <div className="py-1 text-center text-[10px] text-muted-foreground">
            ↓ {link.relation_type ?? "propagation"}
            {link.impact_score != null && (
              <span className="ml-1 text-emerald-400/90">
                {(link.impact_score * 100).toFixed(0)}%
              </span>
            )}
          </div>
        </div>
      ))}
      <div className="max-w-[220px] rounded-lg border border-border bg-muted/40 px-4 py-2 text-center text-sm">
        {links[links.length - 1].target}
      </div>
    </div>
  );
}

function pickDisplayLinks(data: StockChainData | null): StockChainLink[] {
  const all = data?.chain?.links ?? [];
  if (!all.length) return [];

  const entities = data?.chain?.entities ?? [];
  const center =
    entities.find((e) => e.is_center)?.name ||
    data?.center_name ||
    entities.find((e) => e.ticker === data?.ticker?.trim())?.name ||
    "";

  const links = center
    ? all.filter((l) => l.source === center || l.target === center)
    : all;

  return [...links]
    .sort((a, b) => (b.impact_score ?? 0) - (a.impact_score ?? 0))
    .slice(0, 6);
}
