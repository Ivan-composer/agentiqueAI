import { MoreHorizontal } from 'lucide-react'
import Image from 'next/image'
import Link from 'next/link'

interface CreatorCardProps {
  variant: 'small' | 'large'
  id: number
  imageUrl: string
  name: string
  description: string
}

export default function CreatorCard({
  variant,
  id,
  imageUrl,
  name,
  description
}: CreatorCardProps) {
  const content = (
    <>
      <div className="relative aspect-square mb-2">
        <Image
          src={imageUrl}
          alt={name}
          fill
          className="object-cover rounded-xl"
        />
      </div>
      <div className="flex items-start justify-between">
        <div>
          <h3 className="font-semibold text-black">{name}</h3>
          <p className="text-sm text-gray-600">{description}</p>
        </div>
        <button className="p-1 hover:bg-gray-100 rounded-full">
          <MoreHorizontal className="w-5 h-5 text-gray-600" />
        </button>
      </div>
    </>
  )

  if (variant === 'small') {
    return (
      <Link href={`/creator/${id}`} className="flex-shrink-0 w-[200px]">
        {content}
      </Link>
    )
  }

  return (
    <Link href={`/creator/${id}`} className="flex-shrink-0 w-[300px]">
      {content}
    </Link>
  )
}

