"use client";

import type { CompanySearchItem } from "@/services/api";

interface CompanyDropdownProps {
  items: CompanySearchItem[];
  loading?: boolean;
  error?: string | null;
  visible: boolean;
  onSelect: (item: CompanySearchItem) => void;
}

export function CompanyDropdown({
  items,
  loading,
  error,
  visible,
  onSelect,
}: CompanyDropdownProps) {
  if (!visible) return null;

  return (
    <ul
      className="absolute left-0 right-0 top-[calc(100%+4px)] z-[200] max-h-56 w-full overflow-auto rounded-md border border-border bg-card py-1 text-card-foreground shadow-xl ring-1 ring-border"
      role="listbox"
    >
      {loading && (
        <li className="px-3 py-2 text-xs text-muted-foreground">검색 중…</li>
      )}
      {!loading && error && (
        <li className="px-3 py-2 text-xs text-destructive">{error}</li>
      )}
      {!loading && !error && items.length === 0 && (
        <li className="px-3 py-2 text-xs text-muted-foreground">
          검색 결과 없음
        </li>
      )}
      {items.map((item) => (
        <li key={item.ticker}>
          <button
            type="button"
            className="flex w-full flex-col px-3 py-2 text-left text-sm hover:bg-muted"
            onMouseDown={(e) => e.preventDefault()}
            onClick={() => onSelect(item)}
          >
            <span className="font-medium">
              {item.company_name}{" "}
              <span className="font-mono text-xs text-muted-foreground">
                {item.ticker}
              </span>
            </span>
            {item.sector && (
              <span className="text-xs text-muted-foreground">{item.sector}</span>
            )}
          </button>
        </li>
      ))}
    </ul>
  );
}
