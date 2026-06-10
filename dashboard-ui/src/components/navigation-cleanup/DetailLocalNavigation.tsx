"use client";

import { usePathname } from "next/navigation";
import { buildLocalNavigation } from "@/navigation/local-navigation-map";
import { shouldRenderDetailLocalNavigation } from "@/navigation/route-visibility";
import { scrollToSection } from "@/components/runtime-header/RuntimeSectionNav";
import { cn } from "@/lib/utils";
import { useRuntimeShell } from "@/layout/runtime-shell/RuntimeShellProvider";
import { useEffect, useMemo } from "react";
import { sectionIdToKey } from "@/navigation/section-key";

export function DetailLocalNavigation() {
  const pathname = usePathname();
  const { currentSection, setCurrentSection } = useRuntimeShell();
  const items = useMemo(() => buildLocalNavigation(pathname), [pathname]);
  const visible =
    shouldRenderDetailLocalNavigation(pathname) && items.length > 0;

  useEffect(() => {
    if (!visible) return;
    const scrollContainer = document.querySelector<HTMLElement>(
      ".runtime-shell-workspace",
    );
    if (!scrollContainer) return;
    const hashId = window.location.hash.replace("#", "");
    if (items.some((item) => item.href === `#${hashId}`)) {
      setCurrentSection(sectionIdToKey(hashId));
      requestAnimationFrame(() => scrollToSection(hashId));
    }
    const onScroll = () => {
      const atPageBottom =
        scrollContainer.scrollTop + scrollContainer.clientHeight >=
        scrollContainer.scrollHeight - 4;
      if (atPageBottom) {
        const lastVisible = [...items]
          .reverse()
          .find((item) => document.getElementById(item.href.replace("#", "")));
        if (lastVisible) {
          setCurrentSection(sectionIdToKey(lastVisible.href));
          return;
        }
      }
      let active = "summary";
      const threshold = scrollContainer.getBoundingClientRect().top + 120;
      for (const item of items) {
        const id = item.href.replace("#", "");
        const el = document.getElementById(id);
        if (!el) continue;
        if (el.getBoundingClientRect().top <= threshold) {
          active = sectionIdToKey(id);
        }
      }
      setCurrentSection(active);
    };
    scrollContainer.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
    return () => {
      scrollContainer.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
    };
  }, [visible, items, setCurrentSection]);

  if (!visible) return null;

  return (
    <div>
      <p className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">
        Dashboard sections
      </p>
      <nav className="flex flex-wrap gap-1" aria-label="Detail navigation">
        {items.map((item) => (
          <button
            key={item.key}
            type="button"
            onClick={() => {
              setCurrentSection(sectionIdToKey(item.href));
              scrollToSection(item.href.replace("#", ""));
            }}
            className={cn(
              currentSection === sectionIdToKey(item.href)
                ? "dash-section-nav-btn-active"
                : "dash-section-nav-btn",
            )}
          >
            {item.label}
          </button>
        ))}
      </nav>
    </div>
  );
}
