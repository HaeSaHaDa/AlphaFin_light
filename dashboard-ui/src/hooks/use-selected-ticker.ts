"use client";

import { useCallback, useState } from "react";
import type { CompanySearchItem } from "@/services/api";

export function useSelectedTicker() {
  const [selected, setSelected] = useState<CompanySearchItem | null>(null);
  const [keywords, setKeywords] = useState("");

  const selectCompany = useCallback((item: CompanySearchItem) => {
    setSelected(item);
  }, []);

  const clearSelection = useCallback(() => {
    setSelected(null);
  }, []);

  const parseKeywords = useCallback((): string[] => {
    return keywords
      .split(/[\s,]+/)
      .map((k) => k.trim())
      .filter(Boolean);
  }, [keywords]);

  return {
    selectedTicker: selected?.ticker ?? null,
    selectedCompany: selected,
    keywords,
    setKeywords,
    selectCompany,
    clearSelection,
    parseKeywords,
  };
}
