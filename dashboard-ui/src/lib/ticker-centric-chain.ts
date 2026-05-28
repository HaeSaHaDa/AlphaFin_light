/**
 * selectedTicker 중심 Stock Chain / Event Graph (backend ticker_centric_chain.py 와 동일 규칙)
 */
import type { StockChainData } from "@/types/dashboard";
import type { GraphEntity, GraphLink } from "@/types/event-graph";

export interface TickerCentricChain {
  entities: GraphEntity[];
  links: GraphLink[];
  centerName: string;
  centerTicker: string;
}

export function parseCompanyName(query: string, ticker: string): string {
  let q = (query || "").trim();
  const t = (ticker || "").trim();
  if (t) {
    q = q.replace(new RegExp(`\\b${t}\\b`, "g"), "").trim();
  }
  const parts = q.split(/\s+/).filter((p) => p && !/^\d+$/.test(p));
  return parts[0] ?? "";
}

function isConflictingCompany(
  entity: { entity_type?: string; ticker?: string | null },
  selectedTicker: string,
): boolean {
  if (!selectedTicker) return false;
  if (entity.entity_type !== "company") return false;
  const et = (entity.ticker || "").trim();
  return Boolean(et && et !== selectedTicker);
}

function bfsFromCenter(
  centerName: string,
  links: { source: string; target: string }[],
  maxDepth = 2,
): Set<string> {
  const adj = new Map<string, Set<string>>();
  for (const ln of links) {
    if (!ln.source || !ln.target) continue;
    if (!adj.has(ln.source)) adj.set(ln.source, new Set());
    if (!adj.has(ln.target)) adj.set(ln.target, new Set());
    adj.get(ln.source)!.add(ln.target);
    adj.get(ln.target)!.add(ln.source);
  }
  const visited = new Set<string>([centerName]);
  let frontier = new Set<string>([centerName]);
  for (let d = 0; d < maxDepth; d++) {
    const next = new Set<string>();
    for (const node of frontier) {
      for (const nb of adj.get(node) ?? []) {
        if (!visited.has(nb)) {
          visited.add(nb);
          next.add(nb);
        }
      }
    }
    frontier = next;
    if (!frontier.size) break;
  }
  return visited;
}

function chainFromRetrievalChunks(
  centerName: string,
  ticker: string,
  chunks: Array<{ document_type?: string; chunk_id?: number; score?: number }>,
): TickerCentricChain {
  const entities: GraphEntity[] = [
    {
      id: centerName,
      name: centerName,
      entity_type: "company",
      ticker,
      is_center: true,
    } as GraphEntity,
  ];
  const links: GraphLink[] = [];
  const seen = new Set<string>();
  chunks.slice(0, 6).forEach((ch, i) => {
    const doc = ch.document_type || "document";
    const label = `${doc} #${ch.chunk_id ?? i + 1}`;
    if (seen.has(label)) return;
    seen.add(label);
    entities.push({
      id: label,
      name: label,
      entity_type: "market_event",
      ticker: null,
    } as GraphEntity);
    links.push({
      id: `r-${i}`,
      source: centerName,
      target: label,
      relation_type: "retrieval",
      impact_score: ch.score ?? 0.5,
    });
  });
  return { entities, links, centerName, centerTicker: ticker };
}

export function buildTickerCentricChain(
  data: StockChainData,
  retrievalChunks?: Array<{
    document_type?: string;
    chunk_id?: number;
    score?: number;
    ticker?: string;
  }>,
): TickerCentricChain {
  const ticker = (data.ticker || "").trim();
  const centerName = parseCompanyName(data.query || "", ticker) || ticker;
  const rawEntities = data.chain?.entities ?? [];
  const rawLinks = data.chain?.links ?? [];

  let entities = rawEntities
    .filter((e) => !isConflictingCompany(e, ticker))
    .map((e) => ({
      ...e,
      id: e.name,
    })) as GraphEntity[];

  let links = rawLinks.map((l, i) => ({
    ...l,
    id: `e-${i}-${l.source}-${l.target}`,
  })) as GraphLink[];

  let centerEnt = entities.find(
    (e) => e.ticker === ticker || e.name === centerName,
  );
  if (!centerEnt) {
    centerEnt = {
      id: centerName,
      name: centerName,
      entity_type: "company",
      ticker,
      is_center: true,
    } as GraphEntity;
    entities = [centerEnt, ...entities];
  } else {
    entities = entities.map((e) => ({
      ...e,
      is_center: e.name === centerEnt!.name,
    })) as GraphEntity[];
  }

  const bfsRoot = centerEnt!.name;
  if (links.length) {
    const reachable = bfsFromCenter(
      bfsRoot,
      links.map((l) => ({ source: l.source, target: l.target })),
    );
    reachable.add(bfsRoot);
    entities = entities.filter((e) => reachable.has(e.name));
    const names = new Set(entities.map((e) => e.name));
    links = links.filter(
      (l) => names.has(l.source) && names.has(l.target),
    );
  }

  if (!links.length && retrievalChunks?.length) {
    return chainFromRetrievalChunks(centerName, ticker, retrievalChunks);
  }

  if (!links.length && !entities.length) {
    return chainFromRetrievalChunks(centerName, ticker, retrievalChunks ?? []);
  }

  return {
    entities,
    links,
    centerName: centerEnt!.name,
    centerTicker: ticker,
  };
}
