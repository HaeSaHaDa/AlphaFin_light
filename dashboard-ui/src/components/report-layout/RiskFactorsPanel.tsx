interface RiskFactorsPanelProps {
  risks: string[];
  bearishFactors?: string[];
}

export function RiskFactorsPanel({ risks, bearishFactors = [] }: RiskFactorsPanelProps) {
  const items = [...risks, ...bearishFactors].filter(Boolean);
  const unique = [...new Set(items)];

  return (
    <div className="rounded-xl border border-red-500/20 bg-card/60 p-5 h-full">
      <h3 className="text-sm font-semibold text-red-400">리스크</h3>
      <p className="mt-1 text-xs text-muted-foreground">
        주의가 필요한 요인과 하락 압력
      </p>
      {unique.length === 0 ? (
        <p className="mt-4 text-sm text-muted-foreground">데이터 없음</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {unique.map((r, i) => (
            <li key={i} className="flex gap-2 text-sm leading-relaxed">
              <span className="text-red-400">!</span>
              <span>{r}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
