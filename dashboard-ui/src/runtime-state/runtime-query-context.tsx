"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useSearchParams } from "next/navigation";
import { ApiError, runQuery } from "@/services/api";
import type { CompanyResolveData } from "@/types/company";
import type { LoadStatus } from "@/types/dashboard";
import {
  applyPanelBundle,
  beginPanelLoad,
  resetRuntimeForNewQuery,
} from "./dashboard-runtime-sync";
import { loadRuntimePanels } from "./runtime-panel-loader";
import {
  createInitialRuntimeState,
  type RuntimeTraceState,
} from "./runtime-trace-store";
import { loadRuntimeSession, saveRuntimeSession } from "./runtime-session";

interface RuntimeQueryContextValue extends RuntimeTraceState {
  companyContext: CompanyResolveData | null;
  engineRunning: boolean;
  runQuerySelected: (payload: {
    ticker: string;
    company: string;
    keywords: string[];
  }) => Promise<void>;
  loadByTraceId: (traceId: string) => Promise<void>;
}

const RuntimeQueryContext = createContext<RuntimeQueryContextValue | null>(
  null,
);

export function RuntimeQueryProvider({ children }: { children: ReactNode }) {
  const searchParams = useSearchParams();
  const [state, setState] = useState<RuntimeTraceState>(createInitialRuntimeState);
  const [companyContext, setCompanyContext] =
    useState<CompanyResolveData | null>(null);
  const [engineRunning, setEngineRunning] = useState(false);

  const loadPanels = useCallback(async (traceId: string, runtimeQuery?: string) => {
    setState((s) => beginPanelLoad(s));
    try {
      const bundle = await loadRuntimePanels(traceId);
      setState((s) =>
        applyPanelBundle(s, {
          traceId: bundle.traceId,
          data: bundle.data,
          signal: bundle.signal,
          runtimeQuery,
        }),
      );
    } catch (e) {
      const msg =
        e instanceof ApiError
          ? `패널 로드 오류 (${e.status}): ${e.message}`
          : e instanceof Error
            ? e.message
            : "패널 로드 실패";
      setState((s) => ({
        ...s,
        phase: "error",
        panelStatus: "error",
        loadingMessage: null,
        error: msg,
      }));
    }
  }, []);

  const loadByTraceId = useCallback(
    async (traceId: string) => {
      const id = traceId.trim();
      if (!id) return;
      setEngineRunning(false);
      setState((s) => ({
        ...s,
        traceId: id,
        error: null,
        warning: null,
      }));
      await loadPanels(id);
    },
    [loadPanels],
  );

  const urlTraceId = searchParams.get("trace_id")?.trim() || null;

  useEffect(() => {
    if (!state.traceId || (!state.selectedTicker && !state.companyName)) return;
    saveRuntimeSession({
      traceId: state.traceId,
      ticker: state.selectedTicker ?? "",
      companyName: state.companyName ?? "",
      runtimeQuery: state.runtimeQuery ?? "",
    });
  }, [
    state.traceId,
    state.selectedTicker,
    state.companyName,
    state.runtimeQuery,
  ]);

  useEffect(() => {
    const session = loadRuntimeSession();
    const targetTraceId = urlTraceId || session?.traceId || null;
    if (!targetTraceId) return;
    const sessionMatches = session?.traceId === targetTraceId;
    setState((s) => {
      if (s.traceId === targetTraceId && s.panelStatus !== "idle") return s;
      return {
        ...s,
        traceId: targetTraceId,
        selectedTicker: sessionMatches ? session?.ticker || null : null,
        companyName: sessionMatches ? session?.companyName || null : null,
        runtimeQuery: sessionMatches ? session?.runtimeQuery || null : null,
      };
    });
    void loadPanels(
      targetTraceId,
      sessionMatches ? session?.runtimeQuery : undefined,
    );
  }, [urlTraceId, loadPanels]);

  const runQuerySelected = useCallback(
    async (payload: {
      ticker: string;
      company: string;
      keywords: string[];
    }) => {
      setCompanyContext(null);
      setEngineRunning(true);
      setState((s) =>
        resetRuntimeForNewQuery(s, payload.ticker, payload.company),
      );

      try {
        const resp = await runQuery({
          ticker: payload.ticker,
          company: payload.company,
          keywords: payload.keywords,
          run_engine: true,
        });
        setEngineRunning(false);
        if (resp.company) setCompanyContext(resp.company);

        if (!resp.trace_id) {
          setState((s) => ({
            ...s,
            phase: "error",
            panelStatus: "error",
            loadingMessage: null,
            error: "trace_id가 생성되지 않았습니다.",
          }));
          return;
        }

        saveRuntimeSession({
          traceId: resp.trace_id,
          ticker: payload.ticker,
          companyName: payload.company,
          runtimeQuery: resp.runtime_query ?? "",
        });

        if (resp.status === "partial") {
          setState((s) => ({
            ...s,
            warning:
              "데이터는 수집했으나 분석용 문서가 부족합니다. 잠시 후 다시 실행해 주세요.",
          }));
        }

        await loadPanels(resp.trace_id, resp.runtime_query);
      } catch (e) {
        setEngineRunning(false);
        const msg =
          e instanceof ApiError
            ? `분석 오류 (${e.status}): ${e.message}`
            : e instanceof Error
              ? e.message
              : "분석 실패";
        setState((s) => ({
          ...s,
          phase: "error",
          panelStatus: "error",
          loadingMessage: null,
          error: msg,
        }));
      }
    },
    [loadPanels],
  );

  const value = useMemo<RuntimeQueryContextValue>(
    () => ({
      ...state,
      companyContext,
      engineRunning,
      runQuerySelected,
      loadByTraceId,
    }),
    [state, companyContext, engineRunning, runQuerySelected, loadByTraceId],
  );

  return (
    <RuntimeQueryContext.Provider value={value}>
      {children}
    </RuntimeQueryContext.Provider>
  );
}

export function useRuntimeQuery(): RuntimeQueryContextValue {
  const ctx = useContext(RuntimeQueryContext);
  if (!ctx) {
    throw new Error("useRuntimeQuery는 RuntimeQueryProvider 내부에서 사용하세요");
  }
  return ctx;
}

/** 하위 호환: use-dashboard-data */
export function useDashboardRuntime() {
  const r = useRuntimeQuery();
  return {
    data: r.data,
    status: r.panelStatus as LoadStatus,
    error: r.error,
    warning: r.warning,
    traceId: r.traceId,
    engineRunning: r.engineRunning,
    companyContext: r.companyContext,
    selectedTicker: r.selectedTicker,
    companyName: r.companyName,
    runQuerySelected: r.runQuerySelected,
    loadByTraceId: r.loadByTraceId,
    loadingMessage: r.loadingMessage,
    signal: r.signal,
    phase: r.phase,
  };
}
