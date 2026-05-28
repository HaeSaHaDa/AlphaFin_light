/** 분석 실행 후 trace·종목을 sessionStorage에 유지 (서브페이지 검색 연동) */
const KEY = "alphafin_runtime_session";

export interface RuntimeSession {
  traceId: string;
  ticker: string;
  companyName: string;
  runtimeQuery: string;
  updatedAt: number;
}

export function saveRuntimeSession(session: Omit<RuntimeSession, "updatedAt">) {
  if (typeof window === "undefined") return;
  const payload: RuntimeSession = { ...session, updatedAt: Date.now() };
  sessionStorage.setItem(KEY, JSON.stringify(payload));
}

export function loadRuntimeSession(): RuntimeSession | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = sessionStorage.getItem(KEY);
    if (!raw) return null;
    const data = JSON.parse(raw) as RuntimeSession;
    if (!data.traceId) return null;
    return data;
  } catch {
    return null;
  }
}

export function clearRuntimeSession() {
  if (typeof window === "undefined") return;
  sessionStorage.removeItem(KEY);
}
