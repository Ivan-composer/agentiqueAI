import Image from 'next/image'
import Link from 'next/link'
import { ArrowLeft, MessageCircle, Video } from 'lucide-react'
import BottomNav from '@/components/bottom-nav'

// This is a mock function to get creator data. In a real app, you'd fetch this from an API or database.
function getCreatorData(id: string) {
  return {
    id,
    name: `Creator ${id}`,
    description: 'AI Expert & Consultant',
    imageUrl: `/placeholder.svg?height=200&width=200`
  }
}

export default function CreatorPage({ params }: { params: { id: string } }) {
  const creator = getCreatorData(params.id)

  return (
    <main className="min-h-screen bg-white text-black pb-20">
      <div className="relative p-4">
        <Link href="/explore" className="absolute top-4 left-4 flex items-center text-[#0098EA]">
          <ArrowLeft className="w-6 h-6 mr-2" />
          Back
        </Link>
        <div className="pt-16 flex flex-col items-center text-center">
          <Image
            src={creator.imageUrl}
            alt={creator.name}
            width={120}
            height={120}
            className="rounded-full mb-4"
          />
          <h1 className="text-2xl font-bold mb-2">{creator.name}</h1>
          <p className="text-gray-600 mb-6">{creator.description}</p>
        </div>
      </div>

      <div className="px-4 space-y-4">
        <Link href={`/creator/${creator.id}/ai-consultation`} className="flex items-center justify-center gap-4 w-full bg-[#0098EA] text-white py-4 rounded-lg text-lg font-semibold">
          <MessageCircle className="w-6 h-6" />
          AI Consultation
        </Link>
        <Link href={`/creator/${creator.id}/live-consultation`} className="flex items-center justify-center gap-4 w-full bg-white border-2 border-[#0098EA] text-[#0098EA] py-4 rounded-lg text-lg font-semibold">
          <Video className="w-6 h-6" />
          Live Consultation
        </Link>
      </div>
      <BottomNav />
    </main>
  )
}

