'use client'

import Image from 'next/image'
import Link from 'next/link'
import { Settings, LogOut } from 'lucide-react'
import BottomNav from '../bottom-nav'

interface Creator {
  id: number
  name: string
  image: string
}

// Mock user data
const user = {
  username: 'John Doe',
  role: 'Premium User',
  balance: 100,
  creators: [
    {
      id: 1,
      name: 'AI Expert',
      image: '/placeholder.svg?height=100&width=100'
    },
    {
      id: 2,
      name: 'Growth Hacker',
      image: '/placeholder.svg?height=100&width=100'
    }
  ]
}

export default function ProfilePage() {
  return (
    <main className="min-h-screen bg-white pb-20">
      <div className="px-4 py-6">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-2xl font-bold">Profile</h1>
          <div className="flex items-center gap-4">
            <Link href="/settings">
              <Settings className="w-6 h-6 text-gray-600" />
            </Link>
            <button>
              <LogOut className="w-6 h-6 text-gray-600" />
            </button>
          </div>
        </div>

        {/* User Info */}
        <div className="flex items-center gap-4 mb-8">
          <div className="relative w-20 h-20">
            <Image
              src="/placeholder.svg?height=100&width=100"
              alt={user.username}
              fill
              className="rounded-full object-cover"
            />
          </div>
          <div>
            <h2 className="text-xl font-semibold">{user.username}</h2>
            <p className="text-gray-600">{user.role}</p>
          </div>
        </div>

        {/* Balance */}
        <div className="bg-gradient-to-r from-[#08C6C9] to-[#0098EA] rounded-xl p-6 text-white mb-8">
          <p className="text-sm opacity-90 mb-1">Available Balance</p>
          <p className="text-2xl font-bold">${user.balance}</p>
        </div>

        {/* My AI Spirits */}
        <section>
          <h3 className="text-lg font-semibold mb-4">My AI Spirits</h3>
          <div className="grid gap-4">
            {user.creators.map((creator) => (
              <Link
                key={creator.id}
                href={`/creator/${creator.id}`}
                className="flex items-center gap-3 p-4 rounded-xl border border-gray-100"
              >
                <Image
                  src={creator.image}
                  alt={creator.name}
                  width={48}
                  height={48}
                  className="rounded-full"
                />
                <div>
                  <h4 className="font-medium">{creator.name}</h4>
                  <p className="text-sm text-gray-600">AI Creator</p>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </div>

      <BottomNav currentPage="profile" />
    </main>
  )
} 