"use client";

import { useEffect, useRef, useState } from "react";
import { searchCompany, type CompanySearchItem } from "@/services/api";

const DEBOUNCE_MS = 300;

export function useCompanySearch(query: string, enabled = true) {
  const requestIdRef = useRef(0);
  const [results, setResults] = useState<CompanySearchItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) {
      requestIdRef.current += 1;
      setLoading(false);
      return;
    }
    const q = query.trim();
    if (q.length < 1) {
      requestIdRef.current += 1;
      setResults([]);
      setLoading(false);
      setError(null);
      return;
    }

    const timer = setTimeout(async () => {
      const requestId = ++requestIdRef.current;
      setLoading(true);
      setError(null);
      try {
        const hits = await searchCompany(q);
        if (requestId !== requestIdRef.current) return;
        setResults(hits);
      } catch (e) {
        if (requestId !== requestIdRef.current) return;
        setResults([]);
        setError(e instanceof Error ? e.message : "검색 실패");
      } finally {
        if (requestId === requestIdRef.current) setLoading(false);
      }
    }, DEBOUNCE_MS);

    return () => {
      clearTimeout(timer);
      requestIdRef.current += 1;
    };
  }, [query, enabled]);

  return { results, loading, error };
}
