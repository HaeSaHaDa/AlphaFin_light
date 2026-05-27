import * as React from "react";
import { cn } from "@/lib/utils";

const Alert = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { variant?: "default" | "destructive" }
>(({ className, variant = "default", ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(
      "relative w-full rounded-lg border px-4 py-3 text-sm",
      variant === "destructive"
        ? "border-red-500/50 bg-red-500/10 text-red-200"
        : "border-border bg-muted/50 text-foreground",
      className,
    )}
    {...props}
  />
));
Alert.displayName = "Alert";

export { Alert };
