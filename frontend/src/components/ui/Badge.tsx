import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "success" | "error" | "outline"
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
        {
          "border-transparent bg-primary text-surface hover:bg-primary/80": variant === "default",
          "border-transparent bg-[#D1FAE5] text-[#065F46]": variant === "success",
          "border-transparent bg-error-bg text-error": variant === "error",
          "text-text-main": variant === "outline",
        },
        className
      )}
      {...props}
    />
  )
}
