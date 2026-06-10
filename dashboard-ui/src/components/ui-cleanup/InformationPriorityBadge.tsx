"use client";

import { badgeForAccent } from "@/ui/dashboard-variants";
import type { DashboardColorKey } from "@/ui/dashboard-color-system";

interface Props {
  label: string;
  accent?: DashboardColorKey;
}

export function InformationPriorityBadge({
  label,
  accent = "neutral",
}: Props) {
  return <span className={badgeForAccent(accent)}>{label}</span>;
}
