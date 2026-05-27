import Link from "next/link";
import { Activity } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

interface DashboardNavProps {
  traceId: string | null;
  apiBase: string;
  showAnalysisLink?: boolean;
}

export function DashboardNav({
  traceId,
  apiBase,
  showAnalysisLink = true,
}: DashboardNavProps) {
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
        {showAnalysisLink && (
          <>
            <Button variant="outline" size="sm" asChild>
              <Link href="/analysis">Analysis</Link>
            </Button>
            <Button variant="outline" size="sm" asChild>
              <Link href="/event-graph">Event Graph</Link>
            </Button>
            <Button variant="outline" size="sm" asChild>
              <Link href="/memory-timeline">시장 기억</Link>
            </Button>
          </>
        )}
        <Badge variant="secondary">API: {apiBase}</Badge>
        {traceId && (
          <Badge variant="outline">trace: {traceId}</Badge>
        )}
      </div>
    </header>
  );
}
