/** selectedTicker 확정 선택 메타 */
export interface SelectedTickerState {
  ticker: string;
  companyName: string;
  keywords: string[];
}

export function formatSelectedLabel(sel: SelectedTickerState): string {
  const kw = sel.keywords.length ? ` · ${sel.keywords.join(" ")}` : "";
  return `${sel.companyName} ${sel.ticker}${kw}`;
}
