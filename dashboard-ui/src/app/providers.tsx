"use client";

import { Suspense, type ReactNode } from "react";
import { RuntimeQueryProvider } from "@/runtime-state/runtime-query-context";
import { RuntimeShellProvider } from "@/layout/runtime-shell/RuntimeShellProvider";

export function AppProviders({ children }: { children: ReactNode }) {
  return (
    <Suspense fallback={null}>
      <RuntimeQueryProvider>
        <RuntimeShellProvider>{children}</RuntimeShellProvider>
      </RuntimeQueryProvider>
    </Suspense>
  );
}
