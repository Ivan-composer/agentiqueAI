'use client'

import { useState } from 'react'
import { Link2, Plus, ArrowLeft } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'
import SocialItem from '@/components/social-item'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import BottomNav from '@/components/bottom-nav'

interface SocialLink {
  id: string
  platform: string
  username?: string
  url?: string
  isConnected: boolean
  icon: string
}

export default function CreateSpiritPage() {
  const router = useRouter()
  const [socialLinks, setSocialLinks] = useState<SocialLink[]>([
    {
      id: 'telegram',
      platform: 'Telegram',
      isConnected: false,
      icon: '/telegram.svg'
    },
    {
      id: 'linkedin',
      platform: 'Linkedin',
      isConnected: false,
      icon: '/linkedin.svg'
    },
    {
      id: 'x',
      platform: 'X',
      isConnected: false,
      icon: '/x.svg'
    },
    {
      id: 'youtube',
      platform: 'YouTube',
      isConnected: false,
      icon: '/youtube.svg'
    }
  ])

  const handleConnect = (id: string, url: string) => {
    setSocialLinks(prev =>
      prev.map(link =>
        link.id === id
          ? { ...link, url, isConnected: true }
          : link
      )
    )
  }

  const handleSubmit = () => {
    router.push('/create-spirit/loading')
  }

  return (
    <main className="min-h-screen bg-white pb-20">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-white px-4 py-3">
        <div className="flex items-center">
          <Link href="/explore" className="text-[#0098EA]">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <div className="flex-1" />
        </div>
      </div>

      <div className="px-4 py-6">
        <div className="max-w-md mx-auto">
          <h1 className="text-[32px] font-bold text-center mb-2">
            Connect accounts
          </h1>
          <h2 className="text-xl text-center text-gray-600 mb-8">
            To train your <span className="text-[#0098EA]">AI-Spirit</span> on
          </h2>

          <div className="space-y-4 mb-8">
            {socialLinks.map((social) => (
              <SocialItem
                key={social.id}
                social={social}
                onConnect={handleConnect}
              />
            ))}
            
            <button className="w-full bg-[#F1F5F9] rounded-xl p-4 flex items-center justify-center gap-2 text-[#0098EA] font-medium">
              <Plus className="w-5 h-5" />
              Add more
            </button>
          </div>

          <Button
            onClick={handleSubmit}
            className="w-full bg-[#0098EA] hover:bg-[#0088d4] text-white py-6 text-lg font-semibold rounded-xl"
          >
            Submit
          </Button>
        </div>
      </div>

      <BottomNav />
    </main>
  )
}

