import * as React from "react"
import { cn } from "@/lib/utils"

interface ScoreGaugeProps {
  score: number;
  className?: string;
}

export function ScoreGauge({ score, className }: ScoreGaugeProps) {
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  let color = "text-error";
  if (score >= 80) color = "text-success";
  else if (score >= 50) color = "text-orange-500";

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <svg className="transform -rotate-90 w-24 h-24">
        <circle
          className="text-gray-200"
          strokeWidth="8"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
        <circle
          className={cn("transition-all duration-1000 ease-in-out", color)}
          strokeWidth="8"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="48"
          cy="48"
        />
      </svg>
      <span className="absolute text-xl font-bold text-text-main">{score}</span>
    </div>
  )
}
