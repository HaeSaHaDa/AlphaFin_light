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
import { usePathname } from "next/navigation";
import {
  DEFAULT_LAYOUT_STATE,
  RUNTIME_LAYOUT_KEY,
  type RuntimeLayoutState,
} from "./RuntimeLayoutState";
import { normalizeSectionKey } from "@/navigation/section-key";
import { sectionIdToKey } from "@/navigation/section-key";

interface RuntimeShellContextValue extends RuntimeLayoutState {
  setSidebarCollapsed: (v: boolean) => void;
  setCurrentSection: (v: string) => void;
  toggleSidebar: () => void;
}

const RuntimeShellContext = createContext<RuntimeShellContextValue | null>(null);

export function RuntimeShellProvider({ children }: { children: ReactNode }) {
  const pathname = usePathname();
  const [state, setState] = useState<RuntimeLayoutState>(DEFAULT_LAYOUT_STATE);

  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      const raw = sessionStorage.getItem(RUNTIME_LAYOUT_KEY);
      const parsed = raw
        ? (JSON.parse(raw) as RuntimeLayoutState)
        : DEFAULT_LAYOUT_STATE;
      const hashSection = window.location.hash
        ? sectionIdToKey(window.location.hash)
        : null;
      setState({
        sidebarCollapsed: Boolean(parsed.sidebarCollapsed),
        currentSection:
          hashSection ??
          normalizeSectionKey(parsed.currentSection || "summary"),
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
    setState((prev) =>
      prev.sidebarCollapsed === v ? prev : { ...prev, sidebarCollapsed: v },
    );
  }, []);
  const setCurrentSection = useCallback((v: string) => {
    const nextKey = normalizeSectionKey(v);
    setState((prev) =>
      prev.currentSection === nextKey
        ? prev
        : { ...prev, currentSection: nextKey },
    );
  }, []);
  useEffect(() => {
    if (pathname !== "/" || typeof window === "undefined") return;
    setCurrentSection(
      window.location.hash
        ? sectionIdToKey(window.location.hash)
        : "summary",
    );
  }, [pathname, setCurrentSection]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const syncHash = () => {
      if (pathname !== "/") return;
      setCurrentSection(
        window.location.hash
          ? sectionIdToKey(window.location.hash)
          : "summary",
      );
    };
    window.addEventListener("hashchange", syncHash);
    window.addEventListener("popstate", syncHash);
    return () => {
      window.removeEventListener("hashchange", syncHash);
      window.removeEventListener("popstate", syncHash);
    };
  }, [pathname, setCurrentSection]);

  const toggleSidebar = useCallback(() => {
    setState((prev) => ({ ...prev, sidebarCollapsed: !prev.sidebarCollapsed }));
  }, []);

  const value = useMemo<RuntimeShellContextValue>(
    () => ({
      ...state,
      setSidebarCollapsed,
      setCurrentSection,
      toggleSidebar,
    }),
    [state, setSidebarCollapsed, setCurrentSection, toggleSidebar],
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
