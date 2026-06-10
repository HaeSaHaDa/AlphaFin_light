export const NAVIGATION_RESPONSIBILITY = {
  header: [
    "종목 표시",
    "Runtime 상태",
    "trace 상태",
    "사이드바 토글",
    "발표 모드 전환",
  ],
  sidebar: ["전역 화면 이동", "현재 route 강조"],
  detailLocal: ["현재 화면 내부 탭", "섹션 스크롤 이동"],
} as const;

export function isGlobalNavigationOwner(
  area: "header" | "sidebar" | "detail-local",
): boolean {
  return area === "sidebar";
}
