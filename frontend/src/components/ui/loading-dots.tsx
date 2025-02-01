"use client";

import { cn } from "@/lib/utils";

interface LoadingDotsProps {
  className?: string;
}

export function LoadingDots({ className }: LoadingDotsProps) {
  return (
    <div className={cn("flex space-x-1", className)} role="presentation">
      <div className="w-2 h-2 rounded-full bg-current animate-[loading_0.8s_ease-in-out_infinite]" role="presentation" />
      <div className="w-2 h-2 rounded-full bg-current animate-[loading_0.8s_ease-in-out_0.2s_infinite]" role="presentation" />
      <div className="w-2 h-2 rounded-full bg-current animate-[loading_0.8s_ease-in-out_0.4s_infinite]" role="presentation" />
    </div>
  );
} 