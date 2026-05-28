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
import {
  DEFAULT_LAYOUT_STATE,
  RUNTIME_LAYOUT_KEY,
  type RuntimeLayoutState,
} from "./RuntimeLayoutState";

interface RuntimeShellContextValue extends RuntimeLayoutState {
  setSidebarCollapsed: (v: boolean) => void;
  setCurrentSection: (v: string) => void;
  setSearchQuery: (v: string) => void;
  toggleSidebar: () => void;
}

const RuntimeShellContext = createContext<RuntimeShellContextValue | null>(null);

export function RuntimeShellProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<RuntimeLayoutState>(DEFAULT_LAYOUT_STATE);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      const raw = sessionStorage.getItem(RUNTIME_LAYOUT_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw) as RuntimeLayoutState;
      setState({
        sidebarCollapsed: Boolean(parsed.sidebarCollapsed),
        currentSection: parsed.currentSection || "summary",
        searchQuery: parsed.searchQuery || "",
      });
    } catch {
      // ignore parse errors
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    sessionStorage.setItem(RUNTIME_LAYOUT_KEY, JSON.stringify(state));
  }, [state]);

  const setSidebarCollapsed = useCallback((v: boolean) => {
    setState((prev) => ({ ...prev, sidebarCollapsed: v }));
  }, []);
  const setCurrentSection = useCallback((v: string) => {
    setState((prev) => ({ ...prev, currentSection: v }));
  }, []);
  const setSearchQuery = useCallback((v: string) => {
    setState((prev) => ({ ...prev, searchQuery: v }));
  }, []);
  const toggleSidebar = useCallback(() => {
    setState((prev) => ({ ...prev, sidebarCollapsed: !prev.sidebarCollapsed }));
  }, []);

  const value = useMemo<RuntimeShellContextValue>(
    () => ({
      ...state,
      setSidebarCollapsed,
      setCurrentSection,
      setSearchQuery,
      toggleSidebar,
    }),
    [state, setSidebarCollapsed, setCurrentSection, setSearchQuery, toggleSidebar],
  );

  return (
    <RuntimeShellContext.Provider value={value}>
      {children}
    </RuntimeShellContext.Provider>
  );
}

export function useRuntimeShell() {
  const ctx = useContext(RuntimeShellContext);
  if (!ctx) {
    throw new Error("useRuntimeShell must be used inside RuntimeShellProvider");
  }
  return ctx;
}
