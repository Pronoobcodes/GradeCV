import * as React from "react"
import { cn } from "@/lib/utils"

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline'
  size?: 'default' | 'sm' | 'lg'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-full font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background",
          {
            "bg-primary text-surface hover:bg-gray-800": variant === "primary",
            "bg-primary-blue text-white hover:bg-blue-700": variant === "secondary",
            "hover:bg-gray-100 hover:text-text-main text-text-muted": variant === "ghost",
            "border border-gray-200 hover:bg-gray-100 text-text-main": variant === "outline",
            "h-10 py-2 px-4": size === "default",
            "h-9 px-3 rounded-md text-sm": size === "sm",
            "h-12 px-8 rounded-full text-lg": size === "lg",
          },
          className
        )}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
