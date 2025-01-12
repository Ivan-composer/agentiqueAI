import Image from 'next/image'
import Link from 'next/link'
import { Plus } from 'lucide-react'
import BottomNav from '@/components/bottom-nav'
import QuestItem from '@/components/quest-item'
import TokenIcon from '@/components/token-icon'

interface Creator {
  id: number
  name: string
  image: string
}

interface User {
  username: string
  role: string
  balance: number
  creators: Creator[]
}

// Mock data - in real app would come from API
const mockUser: User = {
  username: '@user',
  role: 'Creator and contributer',
  balance: 1337,
  creators: [] // Empty for now to show "Create AI-Spirit" button
}

const quests = [
  {
    id: 1,
    name: 'Quest name 1',
    reward: 500
  },
  {
    id: 2,
    name: 'Quest name 2',
    reward: 1400
  },
  {
    id: 3,
    name: 'Quest name 3',
    reward: 1400
  }
]

export default function ProfilePage() {
  return (
    <main className="min-h-screen bg-white pb-20">
      {/* Profile Header */}
      <div className="px-4 pt-8 pb-6">
        <div className="flex flex-col items-center">
          <div className="w-24 h-24 bg-gray-200 rounded-full mb-4" />
          <h1 className="text-2xl font-bold mb-1 font-['Inter']">{mockUser.username}</h1>
          <p className="text-gray-600 font-['Inter'] font-medium">{mockUser.role}</p>
        </div>
      </div>

      {/* Creators Section */}
      <div className="px-4 mb-8">
        {mockUser.creators.length > 0 ? (
          <div className="flex gap-2 overflow-x-auto">
            {mockUser.creators.map((creator) => (
              <div key={creator.id} className="flex-shrink-0">
                {/* Creator pills would go here */}
              </div>
            ))}
          </div>
        ) : (
          <Link
            href="/create-agent"
            className="flex items-center justify-center gap-2 w-full bg-[#0098EA] text-white py-4 rounded-lg text-lg font-semibold"
          >
            <Plus className="w-6 h-6" />
            Create AI-Agent
          </Link>
        )}
      </div>

      {/* Balance Section */}
      <div className="px-4 mb-6">
        <h2 className="text-2xl font-bold mb-4 font-['Inter']">Balance</h2>
        <div className="flex items-center gap-3 mb-6">
          <TokenIcon className="w-8 h-8" />
          <span className="text-3xl font-bold font-['Inter']">{mockUser.balance}</span>
        </div>

        {/* Balance Actions */}
        <div className="flex gap-4">
          <button
            disabled
            className="flex-1 py-4 bg-[#F1F5F9] rounded-lg font-['Inter'] font-semibold text-[#0098EA]"
          >
            Earn
          </button>
          <button className="flex-1 py-4 bg-[#0098EA] text-white rounded-lg font-['Inter'] font-semibold">
            Purchase
          </button>
        </div>
      </div>

      {/* Quests Section */}
      <div className="px-4">
        <div className="space-y-4">
          {quests.map((quest) => (
            <QuestItem
              key={quest.id}
              name={quest.name}
              reward={quest.reward}
            />
          ))}
        </div>
      </div>

      <BottomNav />
    </main>
  )
}

