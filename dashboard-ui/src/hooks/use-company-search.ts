"use client";

import { useEffect, useState } from "react";
import { searchCompany, type CompanySearchItem } from "@/services/api";

const DEBOUNCE_MS = 300;

export function useCompanySearch(query: string, enabled = true) {
  const [results, setResults] = useState<CompanySearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) return;
    const q = query.trim();
    if (q.length < 1) {
      setResults([]);
      setError(null);
      return;
    }

    const timer = setTimeout(async () => {
      setLoading(true);
      setError(null);
      try {
        const hits = await searchCompany(q);
        setResults(hits);
      } catch (e) {
        setResults([]);
        setError(e instanceof Error ? e.message : "검색 실패");
      } finally {
        setLoading(false);
      }
    }, DEBOUNCE_MS);

    return () => clearTimeout(timer);
  }, [query, enabled]);

  return { results, loading, error };
}
