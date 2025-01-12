'use client'

import { useState } from 'react'
import { Link2, CheckCircle2, DoorClosedIcon as CloseIcon } from 'lucide-react'
import Image from 'next/image'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

interface SocialLink {
  id: string
  platform: string
  username?: string
  url?: string
  isConnected: boolean
  icon: string
}

interface SocialItemProps {
  social: SocialLink
  onConnect: (id: string, url: string) => void
}

export default function SocialItem({ social, onConnect }: SocialItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [url, setUrl] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (url) {
      onConnect(social.id, url)
      setIsEditing(false)
    }
  }

  const truncateUrl = (url: string) => {
    if (!url) return ''
    return url.length > 15 ? '...' + url.slice(-15) : url
  }

  if (isEditing) {
    return (
      <div className="bg-white rounded-xl border border-gray-100 p-4">
        <div className="flex items-center gap-3 mb-3">
          <div className="w-8 h-8 relative">
            <Image
              src={social.icon}
              alt={social.platform}
              width={32}
              height={32}
              className="object-contain"
            />
          </div>
          <span className="font-semibold">{social.platform}</span>
          <button
            onClick={() => setIsEditing(false)}
            className="ml-auto text-gray-400 hover:text-gray-600"
          >
            <CloseIcon className="w-5 h-5" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            type="url"
            placeholder="Paste link here"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1"
          />
          <Button type="submit" variant="ghost" size="icon">
            <Link2 className="w-5 h-5" />
          </Button>
        </form>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl border border-gray-100 p-4">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 relative">
          <Image
            src={social.icon}
            alt={social.platform}
            width={32}
            height={32}
            className="object-contain"
          />
        </div>
        <span className="font-semibold">{social.platform}</span>
        {social.isConnected ? (
          <>
            <span className="text-gray-500 ml-auto">
              {truncateUrl(social.url || '')}
            </span>
            <CheckCircle2 className="w-5 h-5 text-[#0098EA] flex-shrink-0" />
          </>
        ) : (
          <button
            onClick={() => setIsEditing(true)}
            className="ml-auto w-10 h-10 bg-[#F1F5F9] rounded-xl flex items-center justify-center text-[#0098EA]"
          >
            <Link2 className="w-5 h-5" />
          </button>
        )}
      </div>
    </div>
  )
}

