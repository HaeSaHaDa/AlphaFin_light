interface BullishFactorsPanelProps {
  factors: string[];
}

export function BullishFactorsPanel({ factors }: BullishFactorsPanelProps) {
  return (
    <div className="rounded-xl border border-green-500/20 bg-card/60 p-5 h-full">
      <h3 className="text-sm font-semibold text-green-400">상승 요인</h3>
      <p className="mt-1 text-xs text-muted-foreground">
        AI가 긍정적으로 평가한 핵심 근거
      </p>
      {factors.length === 0 ? (
        <p className="mt-4 text-sm text-muted-foreground">데이터 없음</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {factors.map((f, i) => (
            <li key={i} className="flex gap-2 text-sm leading-relaxed">
              <span className="text-green-400">+</span>
              <span>{f}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
