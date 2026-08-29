import * as React from "react"
import { AlertCircle, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "error" | "success" | "info";
  title: string;
  description?: string;
}

export function Alert({ className, variant = "info", title, description, ...props }: AlertProps) {
  return (
    <div
      className={cn(
        "relative w-full rounded-2xl border p-4 shadow-sm flex items-start space-x-4",
        {
          "bg-error-bg border-error/20 text-error": variant === "error",
          "bg-[#F0FDF4] border-[#10B981]/20 text-[#065F46]": variant === "success",
          "bg-gray-50 border-gray-200 text-text-main": variant === "info",
        },
        className
      )}
      {...props}
    >
      {variant === "error" && <AlertCircle className="h-5 w-5 mt-0.5" />}
      {variant === "success" && <CheckCircle2 className="h-5 w-5 mt-0.5" />}
      {variant === "info" && <AlertCircle className="h-5 w-5 mt-0.5" />}
      
      <div className="flex-1">
        <h5 className="font-semibold leading-none tracking-tight">{title}</h5>
        {description && (
          <div className="text-sm opacity-90 mt-2 leading-relaxed">
            {description}
          </div>
        )}
      </div>
    </div>
  )
}
