"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { resolveCompany, searchAndIngest } from "@/services/api";
import type { CompanyResolveData, IngestionRunSummary } from "@/types/company";

function needsIngestion(stats: CompanyResolveData["stats"], cacheReady: boolean) {
  return (
    !cacheReady ||
    stats.pending_embedding_count > 0 ||
    stats.embedding_count < 3 ||
    stats.disclosure_count < 3
  );
}

export function useSearchTrigger(
  query: string,
  enabled: boolean,
  onUpdate?: (payload: {
    company: CompanyResolveData;
    ingestion: IngestionRunSummary | null;
  }) => void,
) {
  const [resolving, setResolving] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [preview, setPreview] = useState<CompanyResolveData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const lastIngestKey = useRef("");

  const runIngestOnly = useCallback(
    async (q: string) => {
      setIngesting(true);
      setError(null);
      try {
        const resp = await searchAndIngest(q, { runEngine: false });
        if (resp.company) {
          setPreview(resp.company);
          onUpdate?.({
            company: resp.company,
            ingestion: resp.ingestion,
          });
        }
        return resp;
      } catch (e) {
        setError(e instanceof Error ? e.message : "수집 실패");
        return null;
      } finally {
        setIngesting(false);
      }
    },
    [onUpdate],
  );

  useEffect(() => {
    if (!enabled) return;
    const text = query.trim();
    if (text.length < 2) {
      setPreview(null);
      setError(null);
      return;
    }

    const timer = setTimeout(async () => {
      setResolving(true);
      setError(null);
      try {
        const company = await resolveCompany(text, true);
        setPreview(company);

        const key = `${company.ticker}-${company.stats.embedding_count}`;
        if (
          needsIngestion(company.stats, company.cache_ready) &&
          lastIngestKey.current !== key
        ) {
          lastIngestKey.current = key;
          await runIngestOnly(text);
        }
      } catch {
        setPreview(null);
        setError("회사를 식별할 수 없습니다. 회사명을 포함해 주세요.");
      } finally {
        setResolving(false);
      }
    }, 600);

    return () => clearTimeout(timer);
  }, [query, enabled, runIngestOnly]);

  const resetIngestKey = useCallback(() => {
    lastIngestKey.current = "";
  }, []);

  return {
    preview,
    resolving,
    ingesting,
    error,
    runIngestOnly,
    resetIngestKey,
  };
}
