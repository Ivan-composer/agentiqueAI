'use client'

import { Suspense } from 'react'
import ClientContent from './client-content'
import BottomNav from '@/components/bottom-nav'

export default function AnswerPage() {
  return (
    <main className="min-h-screen bg-white pb-20">
      <Suspense fallback={
        <div className="px-4 py-6">
          <div className="w-16 h-16 border-4 border-[#0098EA] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <h1 className="text-2xl font-semibold text-center">Loading results...</h1>
        </div>
      }>
        <ClientContent />
      </Suspense>
      <BottomNav />
    </main>
  )
} 