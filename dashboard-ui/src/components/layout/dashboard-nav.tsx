import { Activity } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface DashboardNavProps {
  traceId: string | null;
  apiBase: string;
}

/** 서브 페이지 제목·상태 (페이지 이동은 헤더 탭·사이드바 사용) */
export function DashboardNav({ traceId, apiBase }: DashboardNavProps) {
  return (
    <header className="flex flex-wrap items-center justify-between gap-3 border-b border-border pb-4">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/20 text-primary">
          <Activity className="h-5 w-5" />
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-tight">
            AlphaFin LTE Dashboard
          </h1>
          <p className="text-xs text-muted-foreground">
            Financial AI Engine · 발표용 시각화
          </p>
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-2 text-xs">
        <Badge variant="secondary">API: {apiBase}</Badge>
        {traceId ? (
          <Badge variant="outline">trace: {traceId}</Badge>
        ) : null}
      </div>
    </header>
  );
}
