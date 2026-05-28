"use client";

import { RuntimeHeader } from "./RuntimeHeader";
import { RuntimeSidebar } from "./RuntimeSidebar";
import { RuntimeWorkspace } from "./RuntimeWorkspace";
import { RuntimeFooter } from "./RuntimeFooter";

export function RuntimeShellLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="runtime-shell-root">
      <RuntimeHeader />
      <div className="runtime-shell-body">
        <RuntimeSidebar />
        <RuntimeWorkspace>{children}</RuntimeWorkspace>
      </div>
      <RuntimeFooter />
    </div>
  );
}
