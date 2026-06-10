export interface RuntimeLayoutState {
  sidebarCollapsed: boolean;
  currentSection: string;
}

export const DEFAULT_LAYOUT_STATE: RuntimeLayoutState = {
  sidebarCollapsed: false,
  currentSection: "summary",
};

export const RUNTIME_LAYOUT_KEY = "alphafin_runtime_layout_state";
