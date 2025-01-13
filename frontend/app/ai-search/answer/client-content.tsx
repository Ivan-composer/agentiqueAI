'use client'

import { useState } from 'react'
import { useSearchParams } from 'next/navigation'
import Image from 'next/image'
import { Input } from "@/components/ui/input"

interface Source {
  id: number
  title: string
  creator: {
    name: string
    image: string
  }
}

interface Creator {
  id: number
  name: string
  image: string
  answer: string
}

// Mock data
const sources: Source[] = [
  {
    id: 1,
    title: 'How to grow your business with AI',
    creator: {
      name: 'AI Expert',
      image: '/placeholder.svg?height=100&width=100'
    }
  },
  {
    id: 2,
    title: 'Marketing strategies for startups',
    creator: {
      name: 'Growth Hacker',
      image: '/placeholder.svg?height=100&width=100'
    }
  }
]

const creators: Creator[] = [
  {
    id: 1,
    name: 'AI Expert',
    image: '/placeholder.svg?height=100&width=100',
    answer: 'Here are some key strategies for growing your business with AI...'
  },
  {
    id: 2,
    name: 'Growth Hacker',
    image: '/placeholder.svg?height=100&width=100',
    answer: 'Based on my experience, the most effective marketing strategies for startups are...'
  }
]

export default function ClientContent() {
  const [activeTab, setActiveTab] = useState<'summary' | 'authors'>('summary')
  const searchParams = useSearchParams()
  const query = searchParams?.get('q') || ''

  const handleSendMessage = (message: string) => {
    console.log('Sending message:', message)
  }

  return (
    <div className="px-4 py-6">
      <h1 className="text-[32px] font-bold leading-tight mb-6">
        {query}
      </h1>

      <div className="mb-6">
        <h2 className="text-lg font-medium mb-4">Sources</h2>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {sources.map((source) => (
            <div key={source.id} className="flex-shrink-0 w-[200px] rounded-xl border border-gray-100 p-4">
              <p className="text-sm font-medium mb-4">{source.title}</p>
              <div className="flex items-center gap-2">
                <Image
                  src={source.creator.image}
                  alt={source.creator.name}
                  width={32}
                  height={32}
                  className="rounded-full"
                />
                <span className="text-sm text-gray-600">{source.creator.name}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-gray-100 mb-6">
        <button
          onClick={() => setActiveTab('summary')}
          className={`pb-4 text-sm font-medium ${
            activeTab === 'summary'
              ? 'text-[#0098EA] border-b-2 border-[#0098EA]'
              : 'text-gray-600'
          }`}
        >
          Summary
        </button>
        <button
          onClick={() => setActiveTab('authors')}
          className={`pb-4 text-sm font-medium ${
            activeTab === 'authors'
              ? 'text-[#0098EA] border-b-2 border-[#0098EA]'
              : 'text-gray-600'
          }`}
        >
          Authors
        </button>
      </div>

      {/* Content */}
      {activeTab === 'summary' ? (
        <div className="space-y-4">
          {creators.map((creator) => (
            <div key={creator.id} className="flex gap-3">
              <Image
                src={creator.image}
                alt={creator.name}
                width={40}
                height={40}
                className="rounded-full flex-shrink-0"
              />
              <div>
                <h3 className="font-medium text-sm mb-1">{creator.name}</h3>
                <p className="text-gray-600">{creator.answer}</p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid gap-4">
          {creators.map((creator) => (
            <div key={creator.id} className="flex items-center gap-3">
              <Image
                src={creator.image}
                alt={creator.name}
                width={48}
                height={48}
                className="rounded-full"
              />
              <div>
                <h3 className="font-medium">{creator.name}</h3>
                <p className="text-sm text-gray-600">AI Creator</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Chat Input */}
      <div className="fixed bottom-20 left-4 right-4">
        <form
          onSubmit={(e) => {
            e.preventDefault()
            const input = e.currentTarget.elements.namedItem('message') as HTMLInputElement
            if (input.value.trim()) {
              handleSendMessage(input.value)
              input.value = ''
            }
          }}
          className="relative"
        >
          <input
            type="text"
            name="message"
            placeholder="Ask a follow-up question..."
            className="w-full bg-white border border-gray-200 rounded-full py-3 pl-4 pr-12 shadow-lg"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 bg-[#0098EA] text-white p-2 rounded-full"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </form>
      </div>
    </div>
  )
} 