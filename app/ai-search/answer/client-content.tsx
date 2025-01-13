'use client'

import * as React from 'react'
import Image from 'next/image'
import { useSearchParams } from 'next/navigation'
import BottomNav from '../../../components/bottom-nav'
import ResultTabs from '../../../components/result-tabs'
import ChatInput from '../../../components/chat-input'

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

const sources: Source[] = [
  {
    id: 1,
    title: 'Source_post_name_1',
    creator: {
      name: 'Creator_name1',
      image: '/placeholder.svg?height=40&width=40'
    }
  },
  {
    id: 2,
    title: 'Source_post_name_2',
    creator: {
      name: 'Creator_name2',
      image: '/placeholder.svg?height=40&width=40'
    }
  }
]

const creators: Creator[] = [
  {
    id: 1,
    name: 'Creator_name1',
    image: '/placeholder.svg?height=48&width=48',
    answer: "I'd recommend to focus on email personalization. Here's several..."
  },
  {
    id: 2,
    name: 'Alex Hormozi',
    image: '/placeholder.svg?height=48&width=48',
    answer: "Make the best offer. Here's how I'd do it. First, develop a system..."
  },
  {
    id: 3,
    name: '@Alleyne',
    image: '/placeholder.svg?height=48&width=48',
    answer: 'Use AI-tools for effectiveness. Here is the list from my course...'
  }
]

export default function ClientContent() {
  const [activeTab, setActiveTab] = React.useState<'summary' | 'authors'>('summary')
  const searchParams = useSearchParams()
  const query = searchParams?.get('q') || ''

  const handleSendMessage = (message: string) => {
    // Handle follow-up message
    console.log('Follow-up:', message)
  }

  return (
    <main className="min-h-screen bg-white pb-20">
      <div className="px-4 py-6">
        <h1 className="text-[32px] font-bold leading-tight mb-6 font-['Inter']">
          {query}
        </h1>

        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 font-['Inter']">
            <svg width="20" height="20" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="30" cy="9.99998" r="9.99998" fill="#435A6B"/>
              <circle cx="30" cy="50.0002" r="9.99998" fill="#435A6B"/>
              <circle cx="49.9993" cy="29.9996" r="9.99998" transform="rotate(90 49.9993 29.9996)" fill="#435A6B"/>
              <circle cx="10" cy="29.9996" r="9.99998" transform="rotate(90 10 29.9996)" fill="#435A6B"/>
            </svg>
            Sources
          </h2>
          <div className="flex gap-4 overflow-x-auto pb-4">
            {sources.map((source) => (
              <div
                key={source.id}
                className="flex-shrink-0 w-[200px] rounded-xl border border-gray-100 p-4"
              >
                <h3 className="text-gray-900 mb-3 font-['Inter'] font-medium">{source.title}</h3>
                <div className="flex items-center gap-2">
                  <Image
                    src={source.creator.image}
                    alt={source.creator.name}
                    width={32}
                    height={32}
                    className="rounded-full"
                  />
                  <span className="text-gray-500 font-['Inter'] font-semibold">{source.creator.name}</span>
                </div>
              </div>
            ))}
            <div className="flex-shrink-0 w-[200px] rounded-xl border border-gray-100 p-4">
              <div className="flex gap-1">
                {[1,2,3,4,5].map((i) => (
                  <Image
                    key={i}
                    src="/placeholder.svg?height=32&width=32"
                    alt="Creator"
                    width={32}
                    height={32}
                    className="rounded-full -ml-2 first:ml-0 border-2 border-white"
                  />
                ))}
              </div>
              <span className="text-[#0098EA] font-medium mt-2 block font-['Inter'] font-semibold">
                Show all
              </span>
            </div>
          </div>
        </div>

        <ResultTabs activeTab={activeTab} onTabChange={setActiveTab} />

        <div className="mt-6">
          {activeTab === 'summary' ? (
            <div className="space-y-6">
              <h2 className="text-xl font-bold font-['Inter']">
                Output title
              </h2>
              <div className="space-y-4">
                <p className="font-['Inter'] font-medium">Output result</p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {creators.map((creator) => (
                <div
                  key={creator.id}
                  className="p-4 bg-gray-50 rounded-xl"
                >
                  <div className="flex items-center gap-3 mb-2">
                    <Image
                      src={creator.image}
                      alt={creator.name}
                      width={48}
                      height={48}
                      className="rounded-full"
                    />
                    <span className="font-semibold font-['Inter']">{creator.name}</span>
                  </div>
                  <p className="text-gray-600 font-['Inter']">{creator.answer}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="fixed bottom-[82px] left-0 right-0 px-4 py-3 bg-white">
        <ChatInput 
          onSendMessage={handleSendMessage}
          placeholder="Ask follow-up"
        />
      </div>

      <BottomNav currentPage="ai-search" />
    </main>
  )
} 