"use client";

import { useCallback, useEffect, useState } from "react";
import {
  disablePresentationMode,
  enablePresentationMode,
  getCacheStatus,
} from "@/services/api";

export function usePresentationMode() {
  const [enabled, setEnabled] = useState(false);
  const [loading, setLoading] = useState(true);
  const [toggling, setToggling] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const status = await getCacheStatus();
      setEnabled(Boolean(status.presentation_mode));
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "상태 조회 실패");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const toggle = useCallback(async () => {
    setToggling(true);
    setError(null);
    try {
      if (enabled) {
        await disablePresentationMode();
        setEnabled(false);
      } else {
        await enablePresentationMode();
        setEnabled(true);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "모드 전환 실패");
    } finally {
      setToggling(false);
    }
  }, [enabled]);

  return { enabled, loading, toggling, error, toggle, refresh };
}
