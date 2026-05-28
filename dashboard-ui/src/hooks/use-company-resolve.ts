"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { resolveCompany } from "@/services/api";
import type { CompanyResolveData } from "@/types/company";

export function useCompanyResolve(query: string, enabled = true) {
  const [data, setData] = useState<CompanyResolveData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const fetchResolve = useCallback(async (q: string) => {
    const text = q.trim();
    if (text.length < 2) {
      setData(null);
      setError(null);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const result = await resolveCompany(text, true);
      setData(result);
    } catch {
      setData(null);
      setError("회사를 식별할 수 없습니다. 회사명을 포함해 주세요.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!enabled) return;
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = setTimeout(() => fetchResolve(query), 450);
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, [query, enabled, fetchResolve]);

  return { data, loading, error, refresh: () => fetchResolve(query) };
}
