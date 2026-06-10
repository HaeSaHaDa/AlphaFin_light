"use client";

import { Button, type ButtonProps } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function SecondaryActionButton({
  className,
  variant = "outline",
  size = "sm",
  ...props
}: ButtonProps) {
  return (
    <Button
      type="button"
      variant={variant}
      size={size}
      className={cn("dash-btn-secondary", className)}
      {...props}
    />
  );
}
