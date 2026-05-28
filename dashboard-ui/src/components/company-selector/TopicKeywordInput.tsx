"use client";

import { Input } from "@/components/ui/input";

interface TopicKeywordInputProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function TopicKeywordInput({
  value,
  onChange,
  disabled,
}: TopicKeywordInputProps) {
  return (
    <div className="space-y-1">
      <label className="text-xs text-muted-foreground">분석 키워드</label>
      <Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="예: MLCC 전장부품 반도체"
        disabled={disabled}
      />
      <p className="text-[11px] text-muted-foreground">
        종목과 분리된 주제 키워드입니다. 공백으로 구분합니다.
      </p>
    </div>
  );
}
