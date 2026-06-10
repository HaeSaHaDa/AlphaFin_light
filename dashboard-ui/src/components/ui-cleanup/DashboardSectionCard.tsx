"use client";

import type { ReactNode } from "react";
import { panelAccentClass } from "@/ui/dashboard-variants";
import type { DashboardColorKey } from "@/ui/dashboard-color-system";
import { sectionTitleClass } from "@/ui/dashboard-variants";
import { cn } from "@/lib/utils";

interface Props {
  id?: string;
  title: string;
  subtitle?: string;
  accent?: DashboardColorKey;
  badge?: ReactNode;
  children: ReactNode;
  className?: string;
}

export function DashboardSectionCard({
  id,
  title,
  subtitle,
  accent,
  badge,
  children,
  className,
}: Props) {
  return (
    <section
      id={id}
      className={cn(panelAccentClass(accent), "scroll-mt-24", className)}
    >
      <div className="mb-4 flex flex-wrap items-end justify-between gap-2 border-b border-border/50 pb-3">
        <div>
          <h2 className={sectionTitleClass()}>{title}</h2>
          {subtitle && (
            <p className="mt-1 text-xs text-muted-foreground">{subtitle}</p>
          )}
        </div>
        {badge}
      </div>
      {children}
    </section>
  );
}
