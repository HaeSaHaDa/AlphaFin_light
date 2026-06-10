"use client";

import { Presentation } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { usePresentationMode } from "@/hooks/use-presentation-mode";
import { cn } from "@/lib/utils";

export function PresentationModeToggle() {
  const { enabled, loading, toggling, error, toggle } = usePresentationMode();

  return (
    <div className="flex flex-wrap items-center gap-2">
      <Button
        type="button"
        variant={enabled ? "default" : "outline"}
        size="sm"
        disabled={loading || toggling}
        onClick={() => toggle()}
        className={cn(
          "gap-1.5",
          enabled && "bg-amber-600 hover:bg-amber-600/90 text-white",
        )}
        title={
          enabled
            ? "발표 모드 ON — 신규 embedding 생성이 차단됩니다"
            : "발표 모드 OFF — 클릭하여 캐시 전용 모드로 전환"
        }
      >
        <Presentation className="h-3.5 w-3.5" />
        {toggling ? "전환 중…" : enabled ? "발표 모드 ON" : "발표 모드"}
      </Button>
      {enabled && !loading && (
        <Badge variant="secondary" className="text-[10px] font-normal">
          embedding 생성 차단
        </Badge>
      )}
      {error && (
        <span className="max-w-[140px] truncate text-[10px] text-destructive">
          {error}
        </span>
      )}
    </div>
  );
}
