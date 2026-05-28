import type { RetrievalData, StockChainData } from "@/types/dashboard";
import type { MarketGraphNode, MarketGraphEdge } from "@/types/market-graph";
import { buildTickerCentricChain } from "@/lib/ticker-centric-chain";

/** Stock chain + retrieval analysis → 관계 후보 (클라이언트 보조). */
export function extractCompanyRelations(
  stockChain: StockChainData | null,
  retrieval: RetrievalData | null,
): { nodes: MarketGraphNode[]; edges: MarketGraphEdge[] } {
  if (!stockChain) return { nodes: [], edges: [] };

  const chunks = retrieval?.chunks ?? [];
  const centered = buildTickerCentricChain(stockChain, chunks);
  const centerName =
    stockChain.center_name || centered.centerName;

  const nodes: MarketGraphNode[] = centered.entities.map((e) => ({
    id: e.id,
    label: e.name,
    category: mapEntityCategory(e.entity_type, Boolean(e.is_center)),
    ticker: e.ticker,
    is_center: e.is_center,
    relevance: e.is_center ? 1 : 0.65,
    description: "",
  }));

  const edges: MarketGraphEdge[] = centered.links.map((l) => ({
    id: l.id,
    source: l.source,
    target: l.target,
    edge_type: mapRelationType(l.relation_type),
    relevance: l.impact_score ?? 0.6,
    reason: l.relation_type,
  }));

  const analysis = retrieval?.analysis as Record<string, unknown> | undefined;
  extractRiskRelations(analysis, centerName).forEach((r) => {
    nodes.push(r.node);
    edges.push(r.edge);
  });

  return { nodes, edges };
}

function mapEntityCategory(
  entityType?: string,
  isCenter?: boolean,
): MarketGraphNode["category"] {
  if (isCenter) return "company";
  switch (entityType) {
    case "company":
      return "competitor";
    case "industry":
      return "sector";
    case "product":
    case "supply_chain":
      return "product";
    case "price_change":
      return "macro";
    default:
      return "theme";
  }
}

function mapRelationType(raw?: string): MarketGraphEdge["edge_type"] {
  const k = (raw || "").toLowerCase();
  if (k.includes("supply")) return "SUPPLIES";
  if (k.includes("compet")) return "COMPETES_WITH";
  if (k.includes("risk")) return "EXPOSED_TO";
  if (k.includes("depend")) return "DEPENDS_ON";
  if (k.includes("benefit")) return "BENEFITS_FROM";
  if (k.includes("demand") || k.includes("impact")) return "AFFECTED_BY";
  return "RELATED_TO";
}

export function extractRiskRelations(
  analysis: Record<string, unknown> | undefined,
  centerName: string,
): Array<{ node: MarketGraphNode; edge: MarketGraphEdge }> {
  const out: Array<{ node: MarketGraphNode; edge: MarketGraphEdge }> = [];
  const risks = (analysis?.risks as string[]) ?? [];
  risks.slice(0, 5).forEach((text, i) => {
    if (!text?.trim()) return;
    const id = `risk-local-${i}`;
    out.push({
      node: {
        id,
        label: text.slice(0, 60),
        category: "risk",
        relevance: 0.75,
        description: `${centerName} 리스크 요인`,
      },
      edge: {
        id: `${centerName}->${id}`,
        source: centerName,
        target: id,
        edge_type: "EXPOSED_TO",
        relevance: 0.75,
        reason: "분석 risks",
      },
    });
  });
  return out;
}
