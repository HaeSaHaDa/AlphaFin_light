"use client";

interface Props {
  hasDisclosure: boolean;
  collectStatus?: string;
  disclosureCount?: number;
}

export function DisclosureRuntimeBadge({
  hasDisclosure,
  collectStatus,
  disclosureCount = 0,
}: Props) {
  if (!hasDisclosure && !collectStatus) return null;
  const tone = hasDisclosure
    ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-400"
    : "border-amber-500/40 bg-amber-500/10 text-amber-300";

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-md border px-2 py-0.5 text-[11px] font-medium ${tone}`}
    >
      {hasDisclosure ? "공시 Runtime 연동" : "공시 수집"}
      {disclosureCount > 0 && <span>· {disclosureCount}건</span>}
      {collectStatus && (
        <span className="opacity-70">({collectStatus})</span>
      )}
    </span>
  );
}
