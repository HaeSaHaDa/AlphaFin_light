export function normalizeSectionKey(raw: string): string {
  const key = (raw || "").trim().replace("section-", "");
  if (!key) return "summary";
  if (key === "runtime-evidence") return "evidence";
  if (key === "eval") return "evaluation";
  return key;
}

export function sectionIdToKey(sectionId: string): string {
  return normalizeSectionKey(sectionId.replace("#", ""));
}
