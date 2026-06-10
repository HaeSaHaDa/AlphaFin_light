"use client";

import { Button, type ButtonProps } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function PrimaryActionButton({
  className,
  ...props
}: ButtonProps) {
  return (
    <Button
      type="button"
      className={cn("dash-btn-primary font-semibold shadow-sm", className)}
      {...props}
    />
  );
}
