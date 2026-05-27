import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { LoadStatus } from "@/types/dashboard";

interface PanelShellProps {
  title: string;
  subtitle?: string;
  status: LoadStatus;
  empty?: boolean;
  emptyMessage?: string;
  children: React.ReactNode;
  className?: string;
}

export function PanelShell({
  title,
  subtitle,
  status,
  empty,
  emptyMessage = "데이터 없음",
  children,
  className,
}: PanelShellProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {subtitle && (
          <p className="text-xs text-muted-foreground">{subtitle}</p>
        )}
      </CardHeader>
      <CardContent className="max-h-[320px] overflow-y-auto">
        {status === "loading" && (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-16 w-full" />
          </div>
        )}
        {status !== "loading" && empty && (
          <p className="text-sm text-muted-foreground">{emptyMessage}</p>
        )}
        {status !== "loading" && !empty && children}
      </CardContent>
    </Card>
  );
}
