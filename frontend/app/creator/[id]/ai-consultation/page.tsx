'use client'

import { useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowLeft, CheckCircle2 } from 'lucide-react'
import ChatInput from '@/components/chat-input'
import ChatMessage from '@/components/chat-message'
import BottomNav from '@/components/bottom-nav'

interface Message {
  id: string
  content: string
  role: 'user' | 'assistant'
}

// This would come from an API in a real app
function getCreatorData(id: string) {
  return {
    id,
    name: `Creator ${id}`,
    imageUrl: `/placeholder.svg?height=100&width=100`
  }
}

export default function AIChatPage({ params }: { params: { id: string } }) {
  const creator = getCreatorData(params.id)
  const [messages, setMessages] = useState<Message[]>([])

  const handleSendMessage = (content: string) => {
    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user'
    }
    setMessages(prev => [...prev, userMessage])

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Test answer',
        role: 'assistant'
      }
      setMessages(prev => [...prev, aiMessage])
    }, 1000)
  }

  return (
    <main className="min-h-screen bg-white flex flex-col">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white px-4 py-3 border-b">
        <div className="flex items-center">
          <Link href={`/creator/${params.id}`} className="text-[#0098EA]">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex-1 text-center">
            <h1 className="text-2xl font-bold">
              <span className="text-[#0098EA]">AI-chat</span>
              <span className="text-black"> with</span>
            </h1>
            <div className="flex items-center justify-center gap-2 mt-1">
              <div className="relative">
                <Image
                  src={creator.imageUrl}
                  alt={creator.name}
                  width={32}
                  height={32}
                  className="rounded-full"
                />
                <CheckCircle2 className="absolute -bottom-1 -right-1 w-4 h-4 text-[#0098EA]" />
              </div>
              <span className="text-lg font-medium">{creator.name}</span>
            </div>
          </div>
          <div className="w-6" /> {/* Spacer for alignment */}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 pb-24">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full">
            <div className="relative mb-4">
              <Image
                src={creator.imageUrl}
                alt={creator.name}
                width={64}
                height={64}
                className="rounded-full"
              />
              <CheckCircle2 className="absolute -bottom-1 -right-1 w-6 h-6 text-[#0098EA]" />
            </div>
            <h2 className="text-2xl font-bold mb-2">
              <span className="text-[#0098EA]">AI-chat</span>
              <span className="text-black"> with</span>
            </h2>
            <div className="flex items-center gap-2">
              <span className="text-xl font-medium">{creator.name}</span>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} creator={creator} />
            ))}
          </div>
        )}
      </div>

      {/* Chat Input */}
      <div className="fixed bottom-[82px] left-0 right-0 bg-white px-4 py-3">
        <ChatInput 
          onSendMessage={handleSendMessage}
          placeholder={messages.length === 0 ? "Ask for anything" : "Ask follow-up"}
        />
      </div>

      <BottomNav />
    </main>
  )
}

