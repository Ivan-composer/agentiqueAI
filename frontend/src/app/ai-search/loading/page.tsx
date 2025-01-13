'use client'

import { useSearchParams } from 'next/navigation'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Skeleton } from "@/components/ui/skeleton"
import BottomNav from '../../bottom-nav'

export default function LoadingPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const query = searchParams?.get('q') || ''

  useEffect(() => {
    // Simulate API call delay
    const timer = setTimeout(() => {
      router.push(`/ai-search/answer?q=${encodeURIComponent(query)}`)
    }, 2000)

    return () => clearTimeout(timer)
  }, [query, router])

  return (
    <main className="min-h-screen bg-white pb-20">
      <div className="px-4 py-6">
        <h1 className="text-[32px] font-bold leading-tight mb-6">
          {query}
        </h1>

        <div className="mb-6">
          <h2 className="text-lg font-medium mb-4 flex items-center gap-2">
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-75" />
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-150" />
            <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse delay-300" />
            Finding relevant creators...
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-4">
            <div className="flex-shrink-0 w-[200px] rounded-xl border border-gray-100 p-4">
              <Skeleton className="h-4 w-3/4 mb-4" />
              <div className="flex items-center gap-2">
                <Skeleton className="h-8 w-8 rounded-full" />
                <Skeleton className="h-4 w-24" />
              </div>
            </div>
            <div className="flex-shrink-0 w-[200px] rounded-xl border border-gray-100 p-4">
              <Skeleton className="h-4 w-3/4 mb-4" />
              <div className="flex items-center gap-2">
                <Skeleton className="h-8 w-8 rounded-full" />
                <Skeleton className="h-4 w-24" />
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-4 mt-6">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-4/6" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-5/6" />
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-4/6" />
        </div>
      </div>

      <BottomNav />
    </main>
  )
} 