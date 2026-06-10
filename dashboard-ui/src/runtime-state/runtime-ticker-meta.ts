import { parseCompanyName } from "@/lib/ticker-centric-chain";
import type { DashboardData } from "@/types/dashboard";

export interface RuntimeTickerMeta {
  selectedTicker: string | null;
  companyName: string | null;
  runtimeQuery: string | null;
}

/** 패널 데이터·기존 선택에서 종목 메타 추출 */
export function extractTickerMetaFromDashboard(
  data: DashboardData,
  runtimeQuery?: string | null,
  prev?: { selectedTicker?: string | null; companyName?: string | null },
): RuntimeTickerMeta {
  const ticker =
    data.retrieval?.ticker?.trim() ||
    data.stockChain?.ticker?.trim() ||
    prev?.selectedTicker?.trim() ||
    "";
  const query =
    runtimeQuery?.trim() ||
    data.evaluation?.query?.trim() ||
    data.retrieval?.query?.trim() ||
    data.reflection?.query?.trim() ||
    "";
  const parsedName = ticker ? parseCompanyName(query, ticker) : "";
  const companyName =
    parsedName ||
    prev?.companyName?.trim() ||
    null;

  return {
    selectedTicker: ticker || null,
    companyName,
    runtimeQuery: query || null,
  };
}
