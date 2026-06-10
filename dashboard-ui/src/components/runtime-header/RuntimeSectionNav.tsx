"use client";

import { useEffect, useState } from "react";
import { getDashboardSectionNav } from "@/ui/visual-priority";
import { cn } from "@/lib/utils";

export function scrollToSection(sectionId: string) {
  const el = document.getElementById(sectionId);
  if (!el) return;
  const nextHash = `#${sectionId}`;
  if (window.location.hash !== nextHash) {
    window.history.pushState(null, "", nextHash);
  }
  el.scrollIntoView({ behavior: "smooth", block: "start" });
}

export function RuntimeSectionNav() {
  const sections = getDashboardSectionNav();
  const [activeId, setActiveId] = useState(sections[0]?.id ?? "");

  useEffect(() => {
    const onScroll = () => {
      let current = sections[0]?.id ?? "";
      for (const s of sections) {
        const el = document.getElementById(s.id);
        if (!el) continue;
        if (el.getBoundingClientRect().top <= 120) {
          current = s.id;
        }
      }
      setActiveId(current);
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
    return () => window.removeEventListener("scroll", onScroll);
  }, [sections]);

  return (
    <nav className="flex flex-wrap gap-1" aria-label="Dashboard sections">
      {sections.map((s) => {
        const active = activeId === s.id;
        return (
          <button
            key={s.id}
            type="button"
            onClick={() => scrollToSection(s.id)}
            className={cn(
              active ? "dash-section-nav-btn-active" : "dash-section-nav-btn",
            )}
          >
            {s.label}
          </button>
        );
      })}
    </nav>
  );
}
