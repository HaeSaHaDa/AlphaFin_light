export function MemoryLegend() {
  const layers = [
    { label: "단기 기억", color: "bg-blue-500/70", border: "border-blue-400" },
    { label: "중기 기억", color: "bg-yellow-500/70", border: "border-yellow-400" },
    { label: "장기 기억", color: "bg-purple-500/70", border: "border-purple-400" },
  ];

  const badges = [
    { label: "승격됨", color: "text-green-400", dot: "bg-green-400" },
    { label: "소멸됨", color: "text-red-400", dot: "bg-red-400" },
    { label: "활성", color: "text-cyan-400", dot: "bg-cyan-400" },
  ];

  return (
    <div className="flex flex-wrap items-center gap-4 rounded-lg border border-border bg-card/50 px-4 py-2 text-xs">
      <span className="font-medium text-muted-foreground">범례</span>
      {layers.map((l) => (
        <div key={l.label} className="flex items-center gap-1.5">
          <span className={`inline-block h-3 w-3 rounded-sm border ${l.color} ${l.border}`} />
          <span>{l.label}</span>
        </div>
      ))}
      <span className="text-border">|</span>
      {badges.map((b) => (
        <div key={b.label} className="flex items-center gap-1.5">
          <span className={`inline-block h-2 w-2 rounded-full ${b.dot}`} />
          <span className={b.color}>{b.label}</span>
        </div>
      ))}
    </div>
  );
}
