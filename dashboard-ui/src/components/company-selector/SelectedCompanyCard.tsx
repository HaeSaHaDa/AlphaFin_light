"use client";

import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { CompanySearchItem } from "@/services/api";

interface SelectedCompanyCardProps {
  company: CompanySearchItem | null;
  keywords: string[];
  onClear?: () => void;
}

export function SelectedCompanyCard({
  company,
  keywords,
  onClear,
}: SelectedCompanyCardProps) {
  if (!company) {
    return (
      <p className="rounded-md border border-dashed border-border px-3 py-2 text-xs text-muted-foreground">
        자동완성에서 종목을 선택하면 ticker가 확정됩니다.
      </p>
    );
  }

  return (
    <div className="flex items-start justify-between gap-2 rounded-md border border-primary/40 bg-primary/5 px-3 py-2">
      <div className="text-sm">
        <p className="font-medium">
          {company.company_name}{" "}
          <span className="font-mono text-xs text-primary">{company.ticker}</span>
        </p>
        {company.sector && (
          <p className="text-xs text-muted-foreground">{company.sector}</p>
        )}
        {keywords.length > 0 && (
          <p className="mt-1 text-xs text-muted-foreground">
            키워드: {keywords.join(", ")}
          </p>
        )}
      </div>
      {onClear && (
        <Button type="button" variant="ghost" size="sm" onClick={onClear}>
          <X className="h-4 w-4" />
        </Button>
      )}
    </div>
  );
}
