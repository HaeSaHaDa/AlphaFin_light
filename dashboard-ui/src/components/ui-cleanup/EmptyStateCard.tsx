"use client";

interface Props {
  title?: string;
  message?: string;
}

export function EmptyStateCard({
  title = "Runtime Analysis",
  message = "검색 후 Runtime Analysis가 생성됩니다.",
}: Props) {
  return (
    <div className="dash-empty-state">
      <p className="text-sm font-medium text-foreground">{title}</p>
      <p className="mt-2 text-sm text-muted-foreground">{message}</p>
    </div>
  );
}
