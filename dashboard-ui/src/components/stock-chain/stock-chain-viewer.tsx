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
        NVIDIA → HBM → 삼성전자 → DRAM
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
  const preferred = ["NVIDIA", "HBM", "삼성전자", "DRAM", "GPU"];
  const picked: StockChainLink[] = [];
  const used = new Set<string>();

  for (const name of preferred) {
    const link = all.find(
      (l) =>
        l.source === name ||
        l.target === name ||
        l.source.includes(name) ||
        l.target.includes(name),
    );
    if (link && !used.has(`${link.source}-${link.target}`)) {
      picked.push(link);
      used.add(`${link.source}-${link.target}`);
    }
  }

  if (picked.length >= 2) return picked.slice(0, 4);
  return all
    .filter((l) => (l.impact_score ?? 0) >= 0.75)
    .slice(0, 4);
}
