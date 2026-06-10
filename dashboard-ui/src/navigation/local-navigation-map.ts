export interface LocalNavigationItem {
  key: string;
  label: string;
  href: string;
}

const EMPTY_LOCAL_NAV: LocalNavigationItem[] = [];

export function buildLocalNavigation(pathname: string): LocalNavigationItem[] {
  if (pathname === "/") {
    return [
      { key: "summary", label: "요약", href: "#section-summary" },
      { key: "news", label: "뉴스", href: "#section-news" },
      { key: "events", label: "이벤트", href: "#section-events" },
      { key: "evidence", label: "근거", href: "#section-runtime-evidence" },
      { key: "disclosure", label: "공시", href: "#section-disclosure" },
    ];
  }
  return EMPTY_LOCAL_NAV;
}
