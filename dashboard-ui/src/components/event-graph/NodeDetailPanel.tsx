"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { GraphEntity } from "@/types/event-graph";
import { entityColor } from "@/lib/event-graph/transform";

interface NodeDetailPanelProps {
  entity: GraphEntity | null;
  connectedCount: number;
}

export function NodeDetailPanel({ entity, connectedCount }: NodeDetailPanelProps) {
  if (!entity) {
    return (
      <Card className="h-full border-dashed">
        <CardHeader>
          <CardTitle className="text-sm">Node Detail</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-xs text-muted-foreground">
            그래프에서 노드를 클릭하면 상세 정보가 표시됩니다.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full border-primary/30">
      <CardHeader>
        <CardTitle className="text-sm">Node Detail</CardTitle>
      </CardHeader>
      <CardContent className="space-y-2 text-sm">
        <p className="text-lg font-semibold">{entity.name}</p>
        <Badge
          variant="outline"
          style={{ borderColor: entityColor(entity.entity_type) }}
        >
          {entity.entity_type}
        </Badge>
        {entity.ticker && (
          <p className="text-xs text-muted-foreground">
            Ticker: <span className="font-mono text-foreground">{entity.ticker}</span>
          </p>
        )}
        {entity.event_type && (
          <p className="text-xs text-muted-foreground">
            Event: {entity.event_type}
          </p>
        )}
        <p className="text-xs text-muted-foreground">
          연결 수: {connectedCount}
        </p>
        {entity.created_at && (
          <p className="text-[10px] text-muted-foreground">{entity.created_at}</p>
        )}
      </CardContent>
    </Card>
  );
}
