"use client";

import type { ReactNode } from "react";
import { Input } from "@/components/ui/input";

interface CompanySearchInputProps {
  value: string;
  onChange: (value: string) => void;
  onFocus?: () => void;
  disabled?: boolean;
  placeholder?: string;
  /** 자동완성 목록 — 입력창 바로 아래에 겹쳐 표시 */
  dropdown?: ReactNode;
}

export function CompanySearchInput({
  value,
  onChange,
  onFocus,
  disabled,
  placeholder = "종목명 또는 ticker (예: 삼성전기, 009150)",
  dropdown,
}: CompanySearchInputProps) {
  return (
    <div className="space-y-1">
      <label className="text-xs text-muted-foreground">종목 선택</label>
      <div className="relative z-[100]">
        <Input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={onFocus}
          placeholder={placeholder}
          disabled={disabled}
          autoComplete="off"
        />
        {dropdown}
      </div>
    </div>
  );
}