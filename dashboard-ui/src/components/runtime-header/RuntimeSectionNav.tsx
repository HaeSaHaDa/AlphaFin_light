"use client";

export interface RuntimeSection {
  id: string;
  label: string;
}

const DEFAULT_SECTIONS: RuntimeSection[] = [
  { id: "section-summary", label: "요약" },
  { id: "section-news", label: "뉴스" },
  { id: "section-graph", label: "그래프" },
  { id: "section-memory", label: "메모리" },
  { id: "section-evaluation", label: "평가" },
  { id: "section-reflection", label: "Reflection" },
  { id: "section-retrieval", label: "Retrieval" },
];

export function scrollToSection(sectionId: string) {
  const el = document.getElementById(sectionId);
  if (!el) return;
  const top = el.getBoundingClientRect().top + window.scrollY - 72;
  window.scrollTo({ top, behavior: "smooth" });
}

interface Props {
  sections?: RuntimeSection[];
}

export function RuntimeSectionNav({ sections = DEFAULT_SECTIONS }: Props) {
  return (
    <nav className="flex flex-wrap gap-1" aria-label="Dashboard sections">
      {sections.map((s) => (
        <button
          key={s.id}
          type="button"
          onClick={() => scrollToSection(s.id)}
          className="rounded-md border border-border/80 bg-card/80 px-2.5 py-1 text-xs text-muted-foreground transition-colors hover:border-primary/50 hover:text-foreground"
        >
          {s.label}
        </button>
      ))}
    </nav>
  );
}
