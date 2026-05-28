"use client";

import { ReflectionViewer } from "@/components/reflection/reflection-viewer";
import { RuntimePanelShell } from "./RuntimePanelShell";
import type { LoadStatus, ReflectionData } from "@/types/dashboard";

interface Props {
  traceId: string | null;
  status: LoadStatus;
  reflection: ReflectionData | null;
}

export function RuntimeReflectionPanel({ traceId, status, reflection }: Props) {
  return (
    <RuntimePanelShell traceId={traceId} status={status} title="Reflection">
      <ReflectionViewer data={reflection} status={status} />
    </RuntimePanelShell>
  );
}
