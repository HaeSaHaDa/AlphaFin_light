"use client";

import { useSearchParams } from "next/navigation";

export function RuntimeFooter() {
  const params = useSearchParams();
  const traceId = params.get("trace_id");
  return (
    <footer className="runtime-shell-footer">
      <p className="text-[11px] text-muted-foreground">
        Runtime Footer Status · {traceId ? `trace=${traceId}` : "trace 미지정"}
      </p>
    </footer>
  );
}
