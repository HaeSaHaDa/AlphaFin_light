"use client";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function DisclosureFilterBar({ value, onChange }: Props) {
  return (
    <input
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="공시 유형/키워드 필터"
      className="h-8 w-full rounded-md border border-border bg-card px-2 text-xs"
    />
  );
}
