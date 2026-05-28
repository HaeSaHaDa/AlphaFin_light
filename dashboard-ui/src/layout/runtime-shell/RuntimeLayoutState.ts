export interface RuntimeLayoutState {
  sidebarCollapsed: boolean;
  currentSection: string;
  searchQuery: string;
}

export const DEFAULT_LAYOUT_STATE: RuntimeLayoutState = {
  sidebarCollapsed: false,
  currentSection: "summary",
  searchQuery: "",
};

export const RUNTIME_LAYOUT_KEY = "alphafin_runtime_layout_state";
