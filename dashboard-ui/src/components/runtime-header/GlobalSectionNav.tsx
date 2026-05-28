"use client";

import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";

const SECTIONS = [
  { key: "summary", id: "section-summary", label: "요약" },
  { key: "news", id: "section-news", label: "뉴스" },
  { key: "graph", id: "section-graph", label: "그래프" },
  { key: "memory", id: "section-memory", label: "메모리" },
  { key: "evaluation", id: "section-evaluation", label: "평가" },
];

export function GlobalSectionNav() {
  const { currentSection, setCurrentSection } = useRuntimeShell();
  return (
    <nav className="flex flex-wrap gap-1">
      {SECTIONS.map((s) => (
        <button
          key={s.key}
          type="button"
          className={
            currentSection === s.key
              ? "rounded-md border border-primary/50 bg-primary/10 px-2 py-1 text-[11px] text-primary"
              : "rounded-md border border-border/70 px-2 py-1 text-[11px] text-muted-foreground hover:text-foreground"
          }
          onClick={() => {
            setCurrentSection(s.key);
            const el = document.getElementById(s.id);
            if (!el) return;
            el.scrollIntoView({ behavior: "smooth", block: "start" });
          }}
        >
          {s.label}
        </button>
      ))}
    </nav>
  );
}
