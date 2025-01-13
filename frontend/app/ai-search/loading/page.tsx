'use client'

import { Suspense } from 'react'
import { useSearchParams } from 'next/navigation'

function LoadingContent() {
  const searchParams = useSearchParams()
  const query = searchParams?.get('q') || ''

  return (
    <main className="min-h-screen bg-white flex flex-col items-center justify-center px-4">
      <div className="w-16 h-16 border-4 border-[#0098EA] border-t-transparent rounded-full animate-spin mb-4" />
      <h1 className="text-2xl font-semibold text-center">
        Searching for &quot;{query}&quot;...
      </h1>
    </main>
  )
}

export default function LoadingPage() {
  return (
    <Suspense fallback={
      <main className="min-h-screen bg-white flex flex-col items-center justify-center px-4">
        <div className="w-16 h-16 border-4 border-[#0098EA] border-t-transparent rounded-full animate-spin mb-4" />
        <h1 className="text-2xl font-semibold text-center">Loading...</h1>
      </main>
    }>
      <LoadingContent />
    </Suspense>
  )
} 