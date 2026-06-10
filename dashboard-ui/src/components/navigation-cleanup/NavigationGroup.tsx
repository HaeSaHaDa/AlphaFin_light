"use client";

export function NavigationGroup({
  title,
  children,
}: {
  title: string;
  children: React.ReactNode;
}) {
  return (
    <section aria-label={title}>
      <p className="px-2 pb-1 text-[11px] text-muted-foreground">{title}</p>
      <div className="space-y-1">{children}</div>
    </section>
  );
}
