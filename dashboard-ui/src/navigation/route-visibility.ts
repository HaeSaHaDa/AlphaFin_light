export function shouldRenderSidebar(pathname: string): boolean {
  return Boolean(pathname);
}

export function shouldRenderDetailLocalNavigation(pathname: string): boolean {
  return pathname === "/";
}
